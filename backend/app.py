from flask import Flask, request, jsonify, send_from_directory
from evaluator import evaluate_debate
from ai_generator import generate_debate

app = Flask(__name__, static_folder="../frontend", static_url_path="")


@app.route("/")
def home():
    return send_from_directory("../Frontend", "index.html")


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "success",
        "message": "DebateMate AI backend is running!"
    })


@app.route("/api/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "No data received."
        }), 400

    topic = data.get("topic", "").strip()
    argument = data.get("argument", "").strip()

    if not topic:
        return jsonify({
            "status": "error",
            "message": "Please enter a debate topic."
        }), 400

    if not argument:
        return jsonify({
            "status": "error",
            "message": "Please enter your argument."
        }), 400

    result = evaluate_debate(topic, argument)

    return jsonify({
        "status": "success",
        "result": result
    })


@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "No data received."
        }), 400

    topic = data.get("topic", "").strip()

    if not topic:
        return jsonify({
            "status": "error",
            "message": "Please enter a debate topic."
        }), 400

    try:
        result = generate_debate(topic)

        return jsonify({
            "status": "success",
            "result": result
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
