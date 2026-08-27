from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from process_incoming import process_query


app = Flask(
    __name__,
    static_folder="frontend",
    static_url_path=""
)

CORS(app)


@app.route("/")
def home():
    return send_from_directory("frontend", "index.html")


@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()

        if not data or "query" not in data:
            return jsonify({
                "success": False,
                "error": "Query is required."
            }), 400

        query = data["query"].strip()

        if not query:
            return jsonify({
                "success": False,
                "error": "Query cannot be empty."
            }), 400

        response = process_query(query)

        return jsonify({
            "success": True,
            "response": response
        })

    except Exception as e:
        print("Error:", e)

        return jsonify({
            "success": False,
            "error": "Something went wrong while processing your question."
        }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )