"""
统计 Blueprint：做题统计、标签、每日一题
"""
from flask import Blueprint, jsonify
from backend import database as db
from backend.daily import get_today_problem, refresh_daily, mark_daily_completed

bp = Blueprint('stats', __name__)


@bp.route('/api/daily', methods=['GET'])
def daily():
    result = get_today_problem()
    if not result:
        return jsonify({'error': '题库为空，请先添加题目'}), 404
    return jsonify(result)


@bp.route('/api/daily/refresh', methods=['POST'])
def daily_refresh():
    result = refresh_daily()
    if not result:
        return jsonify({'error': '题库为空'}), 404
    return jsonify(result)


@bp.route('/api/daily/complete', methods=['POST'])
def daily_complete():
    mark_daily_completed()
    return jsonify({'message': '已标记完成'})


@bp.route('/api/stats', methods=['GET'])
def stats():
    return jsonify(db.get_statistics())


@bp.route('/api/tags', methods=['GET'])
def tags():
    all_tags = set()
    for p in db.list_problems():
        all_tags.update(p['tags'])
    return jsonify(sorted(all_tags))
