from flask import Flask


app = Flask(__name__)

@app.route("/")
def index():
	"""Return simple string."""
    return "Main page text"

if __name__ == "__main__":
    app.run()
