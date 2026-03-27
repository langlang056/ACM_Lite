"""
ACM Trainer - Flask 后端
启动: python app.py [-p 端口]
"""
from flask import Flask, render_template

from backend import database as db
from backend.routes.problems import bp as problems_bp
from backend.routes.judge import bp as judge_bp
from backend.routes.stats import bp as stats_bp

app = Flask(__name__,
            static_folder='frontend/static',
            template_folder='frontend/templates')
app.config['JSON_AS_ASCII'] = False

app.register_blueprint(problems_bp)
app.register_blueprint(judge_bp)
app.register_blueprint(stats_bp)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=8080, help='端口 (默认 8080)')
    args = parser.parse_args()

    db.init_db()

    from backend.seed_data import seed
    n = seed()
    if n > 0:
        print(f"  已插入 {n} 道示例题目")

    print(f"\n{'=' * 50}")
    print(f"  ACM Trainer 已启动!")
    print(f"  访问: http://localhost:{args.port}")
    print(f"{'=' * 50}\n")
    app.run(host='0.0.0.0', port=args.port, debug=True)
