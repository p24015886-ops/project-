from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
from mysql.connector import Error
import json

app = Flask(__name__)

# ================= MYSQL CONFIGURATION =================
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "StrongPassword123!",
    "database": "science_quiz"
}

def get_db():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(f"❌ Database Connection Error: {e}")
        return None

# ================= NAVIGATION ROUTES =================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/category")
@app.route("/quiz")
def category():
    return render_template("quiz.html")

@app.route("/videos")
def videos():
    return render_template("videos.html")

@app.route("/make-quiz")
def make_quiz():
    conn = get_db()
    workshops = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM workshops WHERE is_game = 0 ORDER BY created_at DESC")
        workshops = cursor.fetchall()
        cursor.close()
        conn.close()
    return render_template("make_quiz.html", workshops=workshops)

# ================= VIDEO API ENDPOINTS (MySQL) =================

@app.route("/api/get-videos/<category>")
def get_videos_api(category):
    conn = get_db()
    if not conn: return jsonify([])
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, title, description as `desc`, category as cat, url FROM videos WHERE category = %s", (category,))
        data = cursor.fetchall()
        cursor.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        conn.close()

@app.route("/api/add-video", methods=["POST"])
def add_video_api():
    data = request.json
    conn = get_db()
    if not conn: return jsonify({"success": False, "error": "DB Connection Error"})
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO videos (title, description, category, url) VALUES (%s, %s, %s, %s)",
            (data['title'], data['desc'], data['cat'], data['url'])
        )
        conn.commit()
        cursor.close()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
    finally:
        conn.close()

@app.route("/api/delete-video/<int:video_id>", methods=["DELETE"])
def delete_video_api(video_id):
    conn = get_db()
    if not conn: return jsonify({"success": False, "error": "DB Connection Error"})
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM videos WHERE id = %s", (video_id,))
        conn.commit()
        cursor.close()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
    finally:
        conn.close()

# ================= QUIZ & GAME API ENDPOINTS =================

@app.route("/api/publish-workshop", methods=["POST"])
def publish_workshop():
    data = request.json
    conn = get_db()
    if not conn: return jsonify({"success": False})
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO workshops (title, description, category, is_game) VALUES (%s, %s, %s, 0)", (data['title'], data.get('description', ''), data['category']))
        workshop_id = cursor.lastrowid
        for q in data['questions']:
            cursor.execute("INSERT INTO questions (workshop_id, question_text, option_a, option_b, option_c, option_d, correct_answer) VALUES (%s, %s, %s, %s, %s, %s, %s)", (workshop_id, q['text'], q['a'], q['b'], q['c'], q['d'], q['answer']))
        conn.commit()
        return jsonify({"success": True})
    except Exception as e: return jsonify({"success": False, "error": str(e)})
    finally: conn.close()

@app.route("/api/update-workshop/<int:workshop_id>", methods=["POST"])
def update_workshop_api(workshop_id):
    """
    NEW: Handles updating an existing quiz by replacing its questions.
    """
    data = request.json
    conn = get_db()
    if not conn: return jsonify({"success": False, "error": "DB Error"})
    try:
        cursor = conn.cursor()
        # 1. Clear old questions
        cursor.execute("DELETE FROM questions WHERE workshop_id = %s", (workshop_id,))
        
        # 2. Insert updated questions
        for q in data['questions']:
            cursor.execute(
                "INSERT INTO questions (workshop_id, question_text, option_a, option_b, option_c, option_d, correct_answer) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (workshop_id, q['text'], q['a'], q['b'], q['c'], q['d'], q['answer'])
            )
        
        conn.commit()
        cursor.close()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
    finally:
        conn.close()

@app.route("/api/workshop-questions/<int:workshop_id>")
def get_workshop_questions(workshop_id):
    conn = get_db()
    if not conn: return jsonify([])
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, question_text AS text, option_a AS a, option_b AS b, option_c AS c, option_d AS d, correct_answer AS answer FROM questions WHERE workshop_id = %s", (workshop_id,))
    questions = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(questions)

@app.route("/delete-workshop/<int:workshop_id>")
def delete_workshop(workshop_id):
    conn = get_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM workshops WHERE id = %s", (workshop_id,))
        conn.commit()
        conn.close()
    return redirect(url_for('make_quiz'))

@app.route("/get-workshops/<category>")
def get_workshops_api(category):
    conn = get_db()
    if not conn: return jsonify([])
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, title FROM workshops WHERE category = %s AND is_game = 0", (category,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@app.route("/get-games/<category>")
def get_games_api(category):
    level = request.args.get('level')
    conn = get_db()
    if not conn: return jsonify([])
    cursor = conn.cursor(dictionary=True)
    query = "SELECT id, title FROM workshops WHERE category = %s AND is_game = 1"
    params = [category]
    if level:
        query += " AND target_level = %s"
        params.append(level)
    cursor.execute(query, params)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@app.route("/api/game-questions")
def game_questions_api():
    workshop_id = request.args.get('workshop_id')
    conn = get_db()
    if not conn: return jsonify([])
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT question_text AS question, option_a, option_b, option_c, option_d, correct_answer, question_image FROM questions WHERE workshop_id = %s", (workshop_id,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=True)