"""
示例题目数据加载器 - 从 data/problems_seed.json 读取题目，首次运行自动插入
"""
import json
import os
from backend import database as db

_SEED_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'problems_seed.json')


def _load_problems():
    with open(_SEED_FILE, encoding='utf-8') as f:
        return json.load(f)


def seed():
    """插入种子数据（按标题去重，支持增量添加新题 + 补充缺失字段）"""
    problems = _load_problems()
    existing = {p['title']: p for p in db.list_problems()}
    count = 0
    for p in problems:
        if p['title'] in existing:
            ep = existing[p['title']]
            updates = {}
            if not ep.get('lc_template') and p.get('lc_template'):
                updates['lc_template'] = p['lc_template']
                updates['lc_wrapper'] = p.get('lc_wrapper', '')
            if not ep.get('lc_input_fmt') and p.get('lc_input_fmt'):
                updates['lc_input_fmt'] = p['lc_input_fmt']
            if updates:
                db.update_problem(ep['id'], **updates)
            continue
        pid = db.create_problem(
            title=p['title'],
            description=p['description'],
            difficulty=p['difficulty'],
            tags=p['tags'],
            source=p['source'],
            source_url=p['source_url'],
            template_code=p['template_code'],
            lc_template=p.get('lc_template', ''),
            lc_wrapper=p.get('lc_wrapper', ''),
            lc_input_fmt=p.get('lc_input_fmt', ''),
        )
        for tc in p['test_cases']:
            db.add_test_case(pid, tc['input'], tc['expected_output'])
        count += 1
    return count


if __name__ == '__main__':
    db.init_db()
    n = seed()
    print(f'已插入 {n} 道示例题目')
