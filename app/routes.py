from flask import render_template, request, jsonify
from app import app
from app.database import get_db_connection
from app.services.ai_service import ask_ai


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    connection = get_db_connection()

    try:
        conversations = connection.execute(
            """
            SELECT role, message, created_at
            FROM conversations
            ORDER BY id DESC
            LIMIT 50
            """
        ).fetchall()
    finally:
        connection.close()

    return render_template("dashboard.html", conversations=conversations)


@app.route("/api/ask-ai", methods=["POST"])
def ask_ai_route():
    connection = None

    try:
        data = request.get_json(silent=True) or {}
        question = data.get("question", "").strip()

        if not question:
            return jsonify({
                "success": False,
                "error": "Lütfen bir soru yazın."
            }), 400

        answer = ask_ai(question)
        connection = get_db_connection()

        connection.executemany(
            """
            INSERT INTO conversations (session_id, role, message)
            VALUES (?, ?, ?)
            """,
            [
                ("default", "user", question),
                ("default", "assistant", answer)
            ]
        )
        connection.commit()

        return jsonify({
            "success": True,
            "answer": answer
        }), 200

    except Exception:
        app.logger.exception("Yapay zeka isteğinde hata oluştu.")
        return jsonify({
            "success": False,
            "error": "Yapay zeka isteği tamamlanamadı."
        }), 500

    finally:
        if connection:
            connection.close()


@app.route("/api/health", methods=["GET"])
def health_check():
    connection = None

    try:
        connection = get_db_connection()
        connection.execute("SELECT 1")

        return jsonify({
            "success": True,
            "message": "Uygulama ve veritabanı çalışıyor."
        }), 200

    except Exception:
        app.logger.exception("Sağlık kontrolünde hata oluştu.")
        return jsonify({
            "success": False,
            "error": "Veritabanı bağlantısı kontrol edilemedi."
        }), 500

    finally:
        if connection:
            connection.close()
