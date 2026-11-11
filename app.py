from flask import Flask, render_template, request

from checker import check_url
from storage import save_result, list_results

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        url = request.form.get("url", "").strip()[:2000]
        if url:
            result = check_url(url)
            save_result(result)
    return render_template("index.html", result=result, history=list_results())


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False)