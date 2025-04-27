import json
from flask import Flask, request, send_from_directory, Response
import requests
from flask_cors import CORS
import os

# Flask app setup
app = Flask(__name__, static_folder='static')  # Serve static files from the 'static' directory
CORS(app)  # Enable CORS for all routes

# Route to serve the HTML page
@app.route("/")
def index():
    return send_from_directory('static', 'comparator.html')  # Serving comparator.html from static folder

# Add CORS headers to all responses
@app.after_request
def add_cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp

# Proxy route for API comparison
@app.route("/proxy")
def proxy():
    url = request.args.get("url")
    if not url:
        return "Missing url parameter", 400
    try:
        upstream = requests.get(url, timeout=10)
    except Exception as e:
        return f"Upstream error: {e}", 502

    excluded = {"content-encoding", "content-length", "transfer-encoding", "connection"}
    headers = [(k, v) for k, v in upstream.raw.headers.items()
               if k.lower() not in excluded]
    return Response(upstream.content, upstream.status_code, headers)

# Run the Flask app locally
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)  # Running on all available interfaces at port 5000
