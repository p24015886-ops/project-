from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
from mysql.connector import Error
import json

app = Flask(__name__)

# ================= MYSQL CONFIGURATION =================
# Ensure your MySQL server is running and the database 'science_quiz' exists
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Root@1234",
    "database": "science_quiz"
}

def get_db():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(f"❌ Database Connection Error: {e}")
        return None

def normalize_category(raw_category):
    if not raw_category:
        return None
    return raw_category.strip()

# ================= NAVIGATION ROUTES =================
# ================= VIDEO API ENDPOINTS =================

@app.route("/api/get-videos/<category>")
def get_videos_api(category):
    conn = get_db()
    if not conn:
        return jsonify([])

    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, title, description AS `desc`, category AS cat, url
            FROM videos
            WHERE category = %s
        """, (category,))

        videos = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(videos)

    except Exception as e:
        return jsonify({"error": str(e)})
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/category")
@app.route("/quiz")
def category():
    """Renamed from quiz_page to category to match url_for('category') in templates"""
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
        # Fetch only quizzes (is_game = 0)
        cursor.execute("SELECT * FROM workshops WHERE is_game = 0 ORDER BY created_at DESC")
        workshops = cursor.fetchall()
        cursor.close()
        conn.close()
    return render_template("make_quiz.html", workshops=workshops)

@app.route("/games")
def games():
    conn = get_db()
    all_games = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        # Fetch only games (is_game = 1)
        cursor.execute("SELECT * FROM workshops WHERE is_game = 1 ORDER BY created_at DESC")
        all_games = cursor.fetchall()
        cursor.close()
        conn.close()
    return render_template("games.html", games=all_games)

@app.route("/start-games")
def start_games():
    return render_template("game_view.html")

@app.route("/result")
def result():
    score = int(request.args.get("score", 0))
    total = int(request.args.get("total", 0))
    percentage = round((score / total * 100)) if total > 0 else 0
    return render_template("result.html", score=score, total=total, percentage=percentage)

# ================= QUIZ API ENDPOINTS =================

@app.route("/get-workshops/<category>")
def get_workshops_api(category):
    conn = get_db()
    if not conn: return jsonify([])
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, title FROM workshops WHERE category = %s AND is_game = 0",
        (category,)
    )
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@app.route("/api/publish-workshop", methods=["POST"])
def publish_workshop():
    data = request.json
    conn = get_db()
    if not conn: return jsonify({"success": False, "error": "DB Connection Error"})
    
    try:
        cursor = conn.cursor()
        # 1. Insert Workshop
        cursor.execute(
            "INSERT INTO workshops (title, description, category, is_game) VALUES (%s, %s, %s, 0)",
            (data['title'], data.get('description', ''), data['category'])
        )
        workshop_id = cursor.lastrowid
        
        # 2. Insert Questions
        for q in data['questions']:
            cursor.execute("""
                INSERT INTO questions (workshop_id, question_text, option_a, option_b, option_c, option_d, correct_answer)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (workshop_id, q['text'], q['a'], q['b'], q['c'], q['d'], q['answer']))
        
        conn.commit()
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
    cursor.execute("""
        SELECT id, question_text AS text, option_a AS a, option_b AS b, 
               option_c AS c, option_d AS d, correct_answer AS answer
        FROM questions WHERE workshop_id = %s
    """, (workshop_id,))
    questions = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(questions)

@app.route("/api/update-workshop/<int:workshop_id>", methods=["POST"])
def update_workshop(workshop_id):
    data = request.json
    conn = get_db()
    if not conn: return jsonify({"success": False})
    try:
        cursor = conn.cursor()
        # Simpler approach: Delete old questions and insert new ones
        cursor.execute("DELETE FROM questions WHERE workshop_id = %s", (workshop_id,))
        for q in data['questions']:
            cursor.execute("""
                INSERT INTO questions (workshop_id, question_text, option_a, option_b, option_c, option_d, correct_answer)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (workshop_id, q['text'], q['a'], q['b'], q['c'], q['d'], q['answer']))
        conn.commit()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
    finally:
        conn.close()

@app.route("/delete-workshop/<int:workshop_id>")
def delete_workshop(workshop_id):
    conn = get_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM workshops WHERE id = %s", (workshop_id,))
        conn.commit()
        conn.close()
    return redirect(url_for('make_quiz'))

# ================= GAME API ENDPOINTS =================
@app.route("/api/add-video", methods=["POST"])
def add_video():
    data = request.json
    conn = get_db()
    if not conn:
        return jsonify({"success": False, "error": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        # Inserting the video into the 'videos' table
        # Adjust column names based on your actual SQL schema
        cursor.execute("""
            INSERT INTO videos (title, description, category, url)
            VALUES (%s, %s, %s, %s)
        """, (
            data.get('title'),
            data.get('desc') or data.get('description'),
            data.get('category') or data.get('cat'),
            data.get('url')
        ))

        conn.commit()
        cursor.close()
        return jsonify({"success": True, "message": "Video added successfully!"})

    except Exception as e:
        print(f"❌ Error adding video: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        conn.close()
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

@app.route("/api/publish-game", methods=["POST"])
def publish_game():
    data = request.json
    conn = get_db()
    if not conn: return jsonify({"success": False})
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO workshops (title, description, category, target_level, time_limit, is_game) 
            VALUES (%s, %s, %s, %s, %s, 1)
        """, (data['title'], data.get('description', ''), data['category'], data['level'], data.get('time_limit', 0)))
        game_id = cursor.lastrowid
        
        for q in data['questions']:
            cursor.execute("""
                INSERT INTO questions (workshop_id, question_text, option_a, option_b, option_c, option_d, correct_answer, question_image)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (game_id, q['text'], q['a'], q['b'], q['c'], q['d'], q['answer'], q.get('image', '')))
        
        conn.commit()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
    finally:
        conn.close()

@app.route("/api/game-questions")
def game_questions_api():
    workshop_id = request.args.get('workshop_id')
    conn = get_db()
    if not conn: return jsonify([])
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT question_text AS question, option_a, option_b, option_c, option_d, 
               correct_answer, question_image
        FROM questions WHERE workshop_id = %s
    """, (workshop_id,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@app.route("/delete-game/<int:game_id>")
def delete_game(game_id):
    conn = get_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM workshops WHERE id = %s", (game_id,))
        conn.commit()
        conn.close()
    return redirect(url_for('games'))

if __name__ == "__main__":
    # Note: Running on 0.0.0.0 allows access from other devices on your network
    app.run(host="127.0.0.1", port=5050, debug=True)


