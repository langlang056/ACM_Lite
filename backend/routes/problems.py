"""
题目管理 Blueprint：题目 CRUD、测试用例、导入导出
"""
from flask import Blueprint, request, jsonify
from backend import database as db

bp = Blueprint('problems', __name__)


@bp.route('/api/problems', methods=['GET'])
def list_problems():
    problems = db.list_problems(
        difficulty=request.args.get('difficulty'),
        tag=request.args.get('tag'),
        source=request.args.get('source'),
        keyword=request.args.get('keyword'),
    )
    for p in problems:
        p['best_status'] = db.get_problem_best_status(p['id'])
    return jsonify(problems)


@bp.route('/api/problems', methods=['POST'])
def create_problem():
    data = request.json
    pid = db.create_problem(
        title=data['title'],
        description=data.get('description', ''),
        difficulty=data.get('difficulty', 'Medium'),
        tags=data.get('tags', []),
        source=data.get('source', ''),
        source_url=data.get('source_url', ''),
        template_code=data.get('template_code', ''),
        lc_template=data.get('lc_template', ''),
        lc_wrapper=data.get('lc_wrapper', ''),
        lc_input_fmt=data.get('lc_input_fmt', ''),
    )
    for tc in data.get('test_cases', []):
        db.add_test_case(pid, tc.get('input', ''), tc.get('expected_output', ''))
    return jsonify({'id': pid, 'message': '题目创建成功'})


@bp.route('/api/problems/<int:pid>', methods=['GET'])
def get_problem(pid):
    problem = db.get_problem(pid)
    if not problem:
        return jsonify({'error': '题目不存在'}), 404
    problem['test_cases'] = db.get_test_cases(pid)
    problem['best_status'] = db.get_problem_best_status(pid)
    return jsonify(problem)


@bp.route('/api/problems/<int:pid>', methods=['PUT'])
def update_problem(pid):
    db.update_problem(pid, **request.json)
    return jsonify({'message': '更新成功'})


@bp.route('/api/problems/<int:pid>', methods=['DELETE'])
def delete_problem(pid):
    db.delete_problem(pid)
    return jsonify({'message': '删除成功'})


# ---- 测试用例 ----

@bp.route('/api/problems/<int:pid>/testcases', methods=['GET'])
def get_testcases(pid):
    return jsonify(db.get_test_cases(pid))


@bp.route('/api/problems/<int:pid>/testcases', methods=['POST'])
def add_testcase(pid):
    data = request.json
    if isinstance(data, list):
        db.batch_add_test_cases(pid, data)
        return jsonify({'message': f'批量添加 {len(data)} 个用例'})
    tc_id = db.add_test_case(pid, data.get('input', ''), data.get('expected_output', ''))
    return jsonify({'id': tc_id, 'message': '添加成功'})


@bp.route('/api/testcases/<int:tc_id>', methods=['PUT'])
def update_testcase(tc_id):
    db.update_test_case(tc_id, **request.json)
    return jsonify({'message': '更新成功'})


@bp.route('/api/testcases/<int:tc_id>', methods=['DELETE'])
def delete_testcase(tc_id):
    db.delete_test_case(tc_id)
    return jsonify({'message': '删除成功'})


# ---- 导入导出 ----

@bp.route('/api/export', methods=['GET'])
def export_problems():
    return jsonify(db.export_all())


@bp.route('/api/import', methods=['POST'])
def import_problems():
    data = request.json
    if not isinstance(data, list):
        return jsonify({'error': '数据格式错误，需要是题目数组'}), 400
    count = db.import_problems(data)
    return jsonify({'message': f'成功导入 {count} 道题目'})
