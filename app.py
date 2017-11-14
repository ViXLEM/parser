import os

from celery_config import init_celery
from config import DATABASE_URL
from datetime import timedelta
from flask import Flask


app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379',
	CELERY_IMPORTS=("parser",),
	CELERYBEAT_SCHEDULE = {
    'print': {
        'task': 'parser.get_goods_data',
        'schedule': timedelta(days=1),
        },
    }
)

celery = init_celery(app)

@app.route("/")
def index():
	"""Return simple string."""
	return "Main page text"


if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)
