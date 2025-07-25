from flask import Flask, render_template
from main import scan_top_stocks

app = Flask(__name__)

@app.route("/")
def index():
    signals = scan_top_stocks()
    return render_template("index.html", signals=signals)

from pyngrok import ngrok

if __name__ == "__main__":
    public_url = ngrok.connect(5000).public_url
    print(f"Public URL: {public_url}")
    app.run(debug=True)
