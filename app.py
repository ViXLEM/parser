from flask import Flask


app = Flask(__name__)

@app.route("/")
def main_text():
    return "Main page text"

if __name__ == "__main__":
    app.run()
