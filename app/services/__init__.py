
from flask import Flask, jsonify


app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "İstenen adres bulunamadı."
    }), 404


@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error("Sunucu hatası: %s", error)

    return jsonify({
        "success": False,
        "error": "Sunucuda beklenmeyen bir hata oluştu."
    }), 500


from app import routes