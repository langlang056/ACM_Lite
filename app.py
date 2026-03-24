"""
ACM Trainer - Flask 后端
启动: python app.py [-p 端口]
"""
import os
import sys
from dataclasses import asdict
from flask import Flask, render_template, request, jsonify

sys.path.insert(0, os.path.dirname(__file__))

import database as db
from judge import judge
from daily import get_today_problem, refresh_daily, mark_daily_completed

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


def _get_wrapper(pid, mode):
    """核心代码模式下获取适配器代码"""
    if mode != 'core':
        return ''
    problem = db.get_problem(pid)
    return problem.get('lc_wrapper', '') if problem else ''


# ==================== 页面 ====================

@app.route('/')
def index():
    return render_template('index.html')


# ==================== 题目 API ====================

@app.route('/api/problems', methods=['GET'])
def api_list_problems():
    problems = db.list_problems(
        difficulty=request.args.get('difficulty'),
        tag=request.args.get('tag'),
        source=request.args.get('source'),
        keyword=request.args.get('keyword'),
    )
    for p in problems:
        p['best_status'] = db.get_problem_best_status(p['id'])
    return jsonify(problems)


@app.route('/api/problems', methods=['POST'])
def api_create_problem():
    data = request.json
    pid = db.create_problem(
        title=data['title'],
        description=data.get('description', ''),
        difficulty=data.get('difficulty', 'Medium'),
        tags=data.get('tags', []),
        source=data.get('source', ''),
        source_url=data.get('source_url', ''),
        template_code=data.get('template_code', ''),
    )
    for tc in data.get('test_cases', []):
        db.add_test_case(pid, tc.get('input', ''), tc.get('expected_output', ''),
                         tc.get('is_sample', True))
    return jsonify({'id': pid, 'message': '题目创建成功'})


@app.route('/api/problems/<int:pid>', methods=['GET'])
def api_get_problem(pid):
    problem = db.get_problem(pid)
    if not problem:
        return jsonify({'error': '题目不存在'}), 404
    problem['test_cases'] = db.get_test_cases(pid)
    problem['best_status'] = db.get_problem_best_status(pid)
    return jsonify(problem)


@app.route('/api/problems/<int:pid>', methods=['PUT'])
def api_update_problem(pid):
    db.update_problem(pid, **request.json)
    return jsonify({'message': '更新成功'})


@app.route('/api/problems/<int:pid>', methods=['DELETE'])
def api_delete_problem(pid):
    db.delete_problem(pid)
    return jsonify({'message': '删除成功'})


# ==================== 测试用例 API ====================

@app.route('/api/problems/<int:pid>/testcases', methods=['GET'])
def api_get_testcases(pid):
    return jsonify(db.get_test_cases(pid))


@app.route('/api/problems/<int:pid>/testcases', methods=['POST'])
def api_add_testcase(pid):
    data = request.json
    if isinstance(data, list):
        db.batch_add_test_cases(pid, data)
        return jsonify({'message': f'批量添加 {len(data)} 个用例'})
    tc_id = db.add_test_case(pid, data.get('input', ''), data.get('expected_output', ''),
                              data.get('is_sample', True))
    return jsonify({'id': tc_id, 'message': '添加成功'})


@app.route('/api/testcases/<int:tc_id>', methods=['PUT'])
def api_update_testcase(tc_id):
    db.update_test_case(tc_id, **request.json)
    return jsonify({'message': '更新成功'})


@app.route('/api/testcases/<int:tc_id>', methods=['DELETE'])
def api_delete_testcase(tc_id):
    db.delete_test_case(tc_id)
    return jsonify({'message': '删除成功'})


# ==================== 判题 API ====================

@app.route('/api/submit/<int:pid>', methods=['POST'])
def api_submit(pid):
    """正式提交：判题并保存记录"""
    data = request.json
    code = data.get('code', '')
    mode = data.get('mode', 'acm')

    if not code.strip():
        return jsonify({'error': '代码不能为空'}), 400

    test_cases = db.get_test_cases(pid)
    if not test_cases:
        return jsonify({'error': '该题没有测试用例'}), 400

    result = judge(code, test_cases, timeout=data.get('timeout', 5.0),
                   mode=mode, lc_wrapper=_get_wrapper(pid, mode))

    db.create_submission(
        problem_id=pid, code=code, status=result.status,
        time_ms=result.total_time_ms,
        passed_cases=result.passed_cases, total_cases=result.total_cases,
        detail=result.detail, mode=mode,
    )
    return jsonify(asdict(result))


@app.route('/api/run/<int:pid>', methods=['POST'])
def api_run(pid):
    """调试运行：不保存记录"""
    data = request.json
    code = data.get('code', '')
    custom_input = data.get('custom_input')
    mode = data.get('mode', 'acm')

    if not code.strip():
        return jsonify({'error': '代码不能为空'}), 400

    if custom_input is not None:
        test_cases = [{'id': 0, 'input': custom_input, 'expected_output': ''}]
    else:
        test_cases = db.get_test_cases(pid)
        if not test_cases:
            return jsonify({'error': '该题没有测试用例'}), 400

    result = judge(code, test_cases, timeout=data.get('timeout', 5.0),
                   mode=mode, lc_wrapper=_get_wrapper(pid, mode))
    return jsonify(asdict(result))


# ==================== 提交历史 ====================

@app.route('/api/submissions', methods=['GET'])
def api_submissions():
    return jsonify(db.get_submissions(
        problem_id=request.args.get('problem_id', type=int),
        limit=request.args.get('limit', 50, type=int),
    ))


# ==================== 每日一题 ====================

@app.route('/api/daily', methods=['GET'])
def api_daily():
    result = get_today_problem()
    if not result:
        return jsonify({'error': '题库为空，请先添加题目'}), 404
    return jsonify(result)


@app.route('/api/daily/refresh', methods=['POST'])
def api_daily_refresh():
    result = refresh_daily()
    if not result:
        return jsonify({'error': '题库为空'}), 404
    return jsonify(result)


@app.route('/api/daily/complete', methods=['POST'])
def api_daily_complete():
    mark_daily_completed()
    return jsonify({'message': '已标记完成'})


# ==================== 统计 / 标签 / 导入导出 ====================

@app.route('/api/stats', methods=['GET'])
def api_stats():
    return jsonify(db.get_statistics())


@app.route('/api/tags', methods=['GET'])
def api_tags():
    tags = set()
    for p in db.list_problems():
        tags.update(p['tags'])
    return jsonify(sorted(tags))


@app.route('/api/export', methods=['GET'])
def api_export():
    return jsonify(db.export_all())


@app.route('/api/import', methods=['POST'])
def api_import():
    data = request.json
    if not isinstance(data, list):
        return jsonify({'error': '数据格式错误，需要是题目数组'}), 400
    count = db.import_problems(data)
    return jsonify({'message': f'成功导入 {count} 道题目'})


# ==================== 启动 ====================

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=8080, help='端口 (默认 8080)')
    args = parser.parse_args()

    db.init_db()

    from seed_data import seed
    n = seed()
    if n > 0:
        print(f"  已插入 {n} 道示例题目")

    print(f"\n{'=' * 50}")
    print(f"  ACM Trainer 已启动!")
    print(f"  访问: http://localhost:{args.port}")
    print(f"{'=' * 50}\n")
    app.run(host='0.0.0.0', port=args.port, debug=True)
