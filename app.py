from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Assalamu Alaikum! Arsad AI OS is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
