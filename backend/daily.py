"""
每日一题 - 智能抽题逻辑
策略优先级:
  1. 做错过 >= 2 次的题（薄弱题优先复习）
  2. 超过 7 天没复习的已通过题
  3. 从未做过的题
  4. 随机一题兜底
"""
import random
from datetime import date, datetime, timedelta
from backend.database import db_connection, get_problem


def get_today_problem():
    """获取今日一题，如果已设置过则返回已有的"""
    today = date.today().isoformat()

    with db_connection() as conn:
        row = conn.execute(
            "SELECT * FROM daily_problems WHERE date = ?", (today,)
        ).fetchone()

        if row:
            problem = get_problem(row['problem_id'])
            if problem:
                return {
                    'daily_id': row['id'],
                    'problem': problem,
                    'is_completed': bool(row['is_completed']),
                    'date': today
                }

    # 需要新选一道题
    problem_id = pick_problem()
    if not problem_id:
        return None

    with db_connection() as conn:
        conn.execute(
            "INSERT INTO daily_problems (problem_id, date) VALUES (?, ?)",
            (problem_id, today)
        )

    problem = get_problem(problem_id)
    return {
        'daily_id': None,
        'problem': problem,
        'is_completed': False,
        'date': today
    }


def pick_problem():
    """智能选题"""
    with db_connection() as conn:
        all_ids = [r[0] for r in conn.execute("SELECT id FROM problems").fetchall()]
        if not all_ids:
            return None

        # 最近 30 天已做过每日一题的题目，避免短期重复
        recent_daily_ids = set(
            r[0] for r in conn.execute(
                "SELECT problem_id FROM daily_problems WHERE date >= ?",
                ((date.today() - timedelta(days=30)).isoformat(),)
            ).fetchall()
        )

        # 策略1: 做错过 >= 2 次的题
        weak_ids = [r[0] for r in conn.execute("""
            SELECT problem_id FROM submissions
            WHERE status != 'Accepted'
            GROUP BY problem_id
            HAVING COUNT(*) >= 2
        """).fetchall()]
        candidates = [pid for pid in weak_ids if pid not in recent_daily_ids]
        if candidates:
            return random.choice(candidates)

        # 策略2: 超过 7 天没复习的已通过题
        stale_ids = [r[0] for r in conn.execute("""
            SELECT s.problem_id FROM submissions s
            WHERE s.status = 'Accepted'
            GROUP BY s.problem_id
            HAVING MAX(s.submitted_at) < datetime('now', '-7 days', 'localtime')
        """).fetchall()]
        candidates = [pid for pid in stale_ids if pid not in recent_daily_ids]
        if candidates:
            return random.choice(candidates)

        # 策略3: 从未做过的题
        attempted_ids = set(
            r[0] for r in conn.execute(
                "SELECT DISTINCT problem_id FROM submissions"
            ).fetchall()
        )
        unsolved = [pid for pid in all_ids if pid not in attempted_ids and pid not in recent_daily_ids]
        if unsolved:
            return random.choice(unsolved)

        # 策略4: 兜底随机
        remaining = [pid for pid in all_ids if pid not in recent_daily_ids]
        if remaining:
            return random.choice(remaining)

        return random.choice(all_ids)


def refresh_daily():
    """强制刷新今日一题（换一道）"""
    today = date.today().isoformat()

    with db_connection() as conn:
        conn.execute("DELETE FROM daily_problems WHERE date = ?", (today,))

    return get_today_problem()


def mark_daily_completed(daily_date=None):
    """标记每日一题为已完成"""
    today = daily_date if isinstance(daily_date, str) else date.today().isoformat()
    with db_connection() as conn:
        conn.execute(
            "UPDATE daily_problems SET is_completed = 1 WHERE date = ?",
            (today,)
        )
