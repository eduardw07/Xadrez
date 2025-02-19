from flask import Flask
from flask_cors import CORS
from routes.detect import detect_bp

app = Flask(__name__)
CORS(app)

# Registrar as rotas do Blueprint
app.register_blueprint(detect_bp)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API está rodando!"}), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=False)
