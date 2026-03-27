"""
判题 Blueprint：代码运行、提交、提交历史
"""
from dataclasses import asdict
from flask import Blueprint, request, jsonify
from backend import database as db
from backend.judge import judge as run_judge

bp = Blueprint('judge', __name__)


def _execute(pid, code, mode, custom_input=None, timeout=5.0):
    """统一判题入口"""
    if not code.strip():
        return None, ('代码不能为空', 400)

    if custom_input is not None:
        test_cases = [{'id': 0, 'input': custom_input, 'expected_output': ''}]
    else:
        test_cases = db.get_test_cases(pid)
        if not test_cases:
            return None, ('该题没有测试用例', 400)

    lc_wrapper = ''
    if mode == 'core':
        p = db.get_problem(pid)
        lc_wrapper = p.get('lc_wrapper', '') if p else ''

    result = run_judge(code, test_cases, timeout=timeout, mode=mode, lc_wrapper=lc_wrapper)
    return result, None


@bp.route('/api/submit/<int:pid>', methods=['POST'])
def submit(pid):
    """正式提交：判题 + 保存记录"""
    data = request.json
    code, mode = data.get('code', ''), data.get('mode', 'acm')

    result, err = _execute(pid, code, mode, timeout=data.get('timeout', 5.0))
    if err:
        return jsonify({'error': err[0]}), err[1]

    db.create_submission(
        problem_id=pid, code=code, status=result.status,
        time_ms=result.total_time_ms,
        passed_cases=result.passed_cases, total_cases=result.total_cases,
        detail=result.detail, mode=mode,
    )
    return jsonify(asdict(result))


@bp.route('/api/run/<int:pid>', methods=['POST'])
def run(pid):
    """调试运行：不保存记录"""
    data = request.json
    code, mode = data.get('code', ''), data.get('mode', 'acm')

    result, err = _execute(pid, code, mode,
                           custom_input=data.get('custom_input'),
                           timeout=data.get('timeout', 5.0))
    if err:
        return jsonify({'error': err[0]}), err[1]
    return jsonify(asdict(result))


@bp.route('/api/submissions', methods=['GET'])
def submissions():
    return jsonify(db.get_submissions(
        problem_id=request.args.get('problem_id', type=int),
        limit=request.args.get('limit', 50, type=int),
    ))
