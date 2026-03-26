"""
数据层 - SQLite 初始化与 CRUD
"""
import sqlite3
import os
import json
from datetime import datetime
from contextlib import contextmanager

# 数据库路径: 项目根目录下 data/acm_trainer.db
_PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(_PROJECT_ROOT, "data", "acm_trainer.db")


@contextmanager
def db_connection():
    """获取数据库连接（上下文管理器，自动提交/回滚）"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """建表 + 字段迁移"""
    with db_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS problems (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                difficulty TEXT DEFAULT 'Medium' CHECK(difficulty IN ('Easy', 'Medium', 'Hard')),
                tags TEXT DEFAULT '[]',
                source TEXT DEFAULT '',
                source_url TEXT DEFAULT '',
                template_code TEXT DEFAULT '',
                created_at TEXT DEFAULT (datetime('now', 'localtime')),
                updated_at TEXT DEFAULT (datetime('now', 'localtime'))
            );
            CREATE TABLE IF NOT EXISTS test_cases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                problem_id INTEGER NOT NULL,
                input TEXT NOT NULL DEFAULT '',
                expected_output TEXT NOT NULL DEFAULT '',
                is_sample INTEGER DEFAULT 1,
                order_num INTEGER DEFAULT 0,
                FOREIGN KEY (problem_id) REFERENCES problems(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                problem_id INTEGER NOT NULL,
                code TEXT NOT NULL,
                language TEXT DEFAULT 'python',
                status TEXT DEFAULT 'pending',
                time_ms REAL DEFAULT 0,
                memory_kb REAL DEFAULT 0,
                passed_cases INTEGER DEFAULT 0,
                total_cases INTEGER DEFAULT 0,
                detail TEXT DEFAULT '[]',
                submitted_at TEXT DEFAULT (datetime('now', 'localtime')),
                FOREIGN KEY (problem_id) REFERENCES problems(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS daily_problems (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                problem_id INTEGER NOT NULL,
                date TEXT NOT NULL UNIQUE,
                is_completed INTEGER DEFAULT 0,
                FOREIGN KEY (problem_id) REFERENCES problems(id) ON DELETE CASCADE
            );
            CREATE INDEX IF NOT EXISTS idx_submissions_problem ON submissions(problem_id);
            CREATE INDEX IF NOT EXISTS idx_submissions_status ON submissions(status);
            CREATE INDEX IF NOT EXISTS idx_test_cases_problem ON test_cases(problem_id);
            CREATE INDEX IF NOT EXISTS idx_daily_date ON daily_problems(date);
        """)
        # 增量迁移：静默添加新列
        for col in ('lc_template', 'lc_wrapper', 'lc_input_fmt'):
            try:
                conn.execute(f"ALTER TABLE problems ADD COLUMN {col} TEXT DEFAULT ''")
            except Exception:
                pass
        try:
            conn.execute("ALTER TABLE submissions ADD COLUMN mode TEXT DEFAULT 'acm'")
        except Exception:
            pass


# ==================== 通用行转 dict ====================

def _row_to_problem(row):
    """将数据库行转为题目 dict，解析 tags JSON"""
    p = dict(row)
    p['tags'] = json.loads(p['tags'])
    return p


# ==================== 题目 CRUD ====================

def create_problem(title, description="", difficulty="Medium", tags=None,
                   source="", source_url="", template_code="",
                   lc_template="", lc_wrapper="", lc_input_fmt=""):
    tags_json = json.dumps(tags or [], ensure_ascii=False)
    with db_connection() as conn:
        cur = conn.execute(
            """INSERT INTO problems (title, description, difficulty, tags, source, source_url,
               template_code, lc_template, lc_wrapper, lc_input_fmt)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (title, description, difficulty, tags_json, source, source_url,
             template_code, lc_template, lc_wrapper, lc_input_fmt)
        )
        return cur.lastrowid


def get_problem(problem_id):
    with db_connection() as conn:
        row = conn.execute("SELECT * FROM problems WHERE id = ?", (problem_id,)).fetchone()
        return _row_to_problem(row) if row else None


def list_problems(difficulty=None, tag=None, source=None, keyword=None):
    query = "SELECT * FROM problems WHERE 1=1"
    params = []
    if difficulty:
        query += " AND difficulty = ?"
        params.append(difficulty)
    if source:
        query += " AND source LIKE ?"
        params.append(f"%{source}%")
    if keyword:
        query += " AND (title LIKE ? OR description LIKE ?)"
        params.extend([f"%{keyword}%", f"%{keyword}%"])
    if tag:
        query += " AND tags LIKE ?"
        params.append(f'%"{tag}"%')
    query += " ORDER BY id DESC"
    with db_connection() as conn:
        return [_row_to_problem(r) for r in conn.execute(query, params).fetchall()]


def update_problem(problem_id, **kwargs):
    allowed = {'title', 'description', 'difficulty', 'tags', 'source', 'source_url',
               'template_code', 'lc_template', 'lc_wrapper', 'lc_input_fmt'}
    updates = {k: v for k, v in kwargs.items() if k in allowed}
    if 'tags' in updates:
        updates['tags'] = json.dumps(updates['tags'], ensure_ascii=False)
    if not updates:
        return
    updates['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    set_clause = ", ".join(f"{k} = ?" for k in updates)
    with db_connection() as conn:
        conn.execute(f"UPDATE problems SET {set_clause} WHERE id = ?",
                     list(updates.values()) + [problem_id])


def delete_problem(problem_id):
    with db_connection() as conn:
        conn.execute("DELETE FROM problems WHERE id = ?", (problem_id,))


# ==================== 测试用例 CRUD ====================

def _next_order(conn, problem_id):
    return conn.execute(
        "SELECT COALESCE(MAX(order_num), 0) + 1 FROM test_cases WHERE problem_id = ?",
        (problem_id,)
    ).fetchone()[0]


def add_test_case(problem_id, input_data, expected_output, is_sample=True):
    with db_connection() as conn:
        cur = conn.execute(
            "INSERT INTO test_cases (problem_id, input, expected_output, is_sample, order_num) VALUES (?, ?, ?, ?, ?)",
            (problem_id, input_data, expected_output, int(is_sample), _next_order(conn, problem_id))
        )
        return cur.lastrowid


def get_test_cases(problem_id):
    with db_connection() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT * FROM test_cases WHERE problem_id = ? ORDER BY order_num", (problem_id,)
        ).fetchall()]


def update_test_case(tc_id, **kwargs):
    allowed = {'input': 'input', 'expected_output': 'expected_output',
               'is_sample': 'is_sample', 'input_data': 'input'}
    updates = {}
    for k, col in allowed.items():
        if k in kwargs and kwargs[k] is not None:
            updates[col] = int(kwargs[k]) if col == 'is_sample' else kwargs[k]
    if not updates:
        return
    set_clause = ", ".join(f"{k} = ?" for k in updates)
    with db_connection() as conn:
        conn.execute(f"UPDATE test_cases SET {set_clause} WHERE id = ?",
                     list(updates.values()) + [tc_id])


def delete_test_case(tc_id):
    with db_connection() as conn:
        conn.execute("DELETE FROM test_cases WHERE id = ?", (tc_id,))


def batch_add_test_cases(problem_id, cases):
    """批量添加测试用例"""
    with db_connection() as conn:
        start = _next_order(conn, problem_id)
        for i, c in enumerate(cases):
            conn.execute(
                "INSERT INTO test_cases (problem_id, input, expected_output, is_sample, order_num) VALUES (?, ?, ?, ?, ?)",
                (problem_id, c.get('input', ''), c.get('expected_output', ''),
                 int(c.get('is_sample', True)), start + i)
            )


# ==================== 提交记录 ====================

def create_submission(problem_id, code, status, time_ms=0, memory_kb=0,
                      passed_cases=0, total_cases=0, detail=None, mode='acm'):
    detail_json = json.dumps(detail or [], ensure_ascii=False)
    with db_connection() as conn:
        return conn.execute(
            """INSERT INTO submissions (problem_id, code, status, time_ms, memory_kb,
               passed_cases, total_cases, detail, mode) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (problem_id, code, status, time_ms, memory_kb, passed_cases, total_cases, detail_json, mode)
        ).lastrowid


def get_submissions(problem_id=None, limit=50):
    query = "SELECT * FROM submissions"
    params = []
    if problem_id:
        query += " WHERE problem_id = ?"
        params.append(problem_id)
    query += " ORDER BY submitted_at DESC LIMIT ?"
    params.append(limit)
    with db_connection() as conn:
        result = []
        for row in conn.execute(query, params).fetchall():
            s = dict(row)
            s['detail'] = json.loads(s['detail'])
            result.append(s)
        return result


def get_problem_best_status(problem_id):
    """获取题目最佳提交状态（AC 优先）"""
    with db_connection() as conn:
        row = conn.execute(
            """SELECT status FROM submissions WHERE problem_id = ?
               ORDER BY CASE status WHEN 'Accepted' THEN 0 ELSE 1 END, submitted_at DESC
               LIMIT 1""",
            (problem_id,)
        ).fetchone()
        return row['status'] if row else None


# ==================== 统计 ====================

def get_statistics():
    """返回做题统计数据（全部用 SQL 聚合，避免 Python 循环）"""
    with db_connection() as conn:
        total = conn.execute("SELECT COUNT(*) FROM problems").fetchone()[0]

        diff_counts = {}
        for r in conn.execute("SELECT difficulty, COUNT(*) as cnt FROM problems GROUP BY difficulty"):
            diff_counts[r['difficulty']] = r['cnt']

        ac_count = conn.execute(
            "SELECT COUNT(DISTINCT problem_id) FROM submissions WHERE status = 'Accepted'"
        ).fetchone()[0]

        total_submissions = conn.execute("SELECT COUNT(*) FROM submissions").fetchone()[0]

        ac_by_diff = {}
        for r in conn.execute("""
            SELECT p.difficulty, COUNT(DISTINCT s.problem_id) as cnt
            FROM submissions s JOIN problems p ON s.problem_id = p.id
            WHERE s.status = 'Accepted' GROUP BY p.difficulty
        """):
            ac_by_diff[r['difficulty']] = r['cnt']

        daily_activity = [dict(r) for r in conn.execute("""
            SELECT DATE(submitted_at) as day, COUNT(*) as cnt,
                   SUM(CASE WHEN status = 'Accepted' THEN 1 ELSE 0 END) as ac_cnt
            FROM submissions WHERE submitted_at >= datetime('now', '-30 days', 'localtime')
            GROUP BY DATE(submitted_at) ORDER BY day
        """)]

        # 标签统计需遍历 JSON 字段
        tag_stats = {}
        for r in conn.execute("SELECT tags FROM problems"):
            for t in json.loads(r['tags']):
                tag_stats[t] = tag_stats.get(t, 0) + 1

        return {
            'total_problems': total, 'difficulty_counts': diff_counts,
            'ac_count': ac_count, 'ac_by_difficulty': ac_by_diff,
            'total_submissions': total_submissions,
            'daily_activity': daily_activity, 'tag_stats': tag_stats,
        }


# ==================== 导入导出 ====================

def export_all():
    problems = list_problems()
    for p in problems:
        p['test_cases'] = get_test_cases(p['id'])
    return problems


def import_problems(data):
    count = 0
    for p in data:
        pid = create_problem(
            title=p['title'], description=p.get('description', ''),
            difficulty=p.get('difficulty', 'Medium'), tags=p.get('tags', []),
            source=p.get('source', ''), source_url=p.get('source_url', ''),
            template_code=p.get('template_code', ''),
        )
        for tc in p.get('test_cases', []):
            add_test_case(pid, tc.get('input', ''), tc.get('expected_output', ''))
        count += 1
    return count
