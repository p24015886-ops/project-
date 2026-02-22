from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
from mysql.connector import Error
import random

app = Flask(__name__)

# === MYSQL CONFIGURATION ===
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "StrongPassword123!",
    "database": "science_quiz"
}

def get_db():
    """Establishes and returns a connection to the MySQL database."""
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(f"❌ Database Error: {e}")
        return None

# ================= NAVIGATION ROUTES =================

@app.route("/")
def home():
    """Renders the main landing page."""
    return render_template("index.html")

@app.route("/category")
def category():
    """Renders the level selection page."""
    return render_template("category.html")

@app.route("/make-quiz")
def make_quiz():
    """Renders the workshop management page (Dashboard)."""
    conn = get_db()
    workshops = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM workshops ORDER BY created_at DESC")
        workshops = cursor.fetchall()
        cursor.close()
        conn.close()
    return render_template("make_quiz.html", workshops=workshops)

@app.route("/games")
def games():
    """Renders the games selection/lobby page."""
    return render_template("game_view.html")

@app.route("/game-play")
def game_play():
    """Renders the actual interactive quiz game."""
    return render_template("game_play.html")

@app.route("/videos")
def videos():
    """Renders the science video library."""
    return render_template("videos.html")

# ================= CRUD OPERATIONS =================

@app.route("/create-workshop", methods=["POST"])
def create_workshop():
    """Creates a new workshop entry."""
    title = request.form.get("title")
    description = request.form.get("description")
    category = request.form.get("category", "physics")
    level = request.form.get("level", "upper_primary")
    
    conn = get_db()
    if not conn: return "DB Error", 500
    
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO workshops (title, description, category, target_level) VALUES (%s, %s, %s, %s)", 
            (title, description, category, level)
        )
        conn.commit()
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for("make_quiz"))

@app.route("/delete-workshop/<int:workshop_id>")
def delete_workshop(workshop_id):
    """Deletes a workshop and its associated questions."""
    conn = get_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM questions WHERE workshop_id = %s", (workshop_id,))
        cursor.execute("DELETE FROM workshops WHERE id = %s", (workshop_id,))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for("make_quiz"))

@app.route("/add-question/<int:workshop_id>", methods=["POST"])
def add_question(workshop_id):
    """Adds a specific question to a specific workshop."""
    q_text = request.form.get("question_text")
    a = request.form.get("option_a")
    b = request.form.get("option_b")
    c = request.form.get("option_c")
    d = request.form.get("option_d")
    correct = request.form.get("correct_answer")
    
    # Get the level from the workshop to maintain consistency
    conn = get_db()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT target_level FROM workshops WHERE id = %s", (workshop_id,))
        workshop = cursor.fetchone()
        level = workshop['target_level'] if workshop else "upper_primary"
        
        cursor.execute("""
            INSERT INTO questions (workshop_id, question_text, option_a, option_b, option_c, option_d, correct_answer, level)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (workshop_id, q_text, a, b, c, d, correct, level))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for("make_quiz"))

# ================= QUIZ ENGINE =================

@app.route("/quiz")
def start_quiz():
    """Renders the static quiz view for students."""
    level_map = {'lower': 'lower_primary', 'upper': 'upper_primary', 'secondary': 'upper_primary'}
    raw_level = request.args.get('level', 'upper')
    db_level = level_map.get(raw_level, 'upper_primary')
    
    conn = get_db()
    if not conn: return "DB Error", 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT question_text as question, option_a, option_b, option_c, option_d 
        FROM questions 
        WHERE level = %s 
        ORDER BY RAND() 
        LIMIT 10
    """, (db_level,))
    
    questions = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template("quiz.html", questions=questions)

@app.route("/save-game-settings", methods=["POST"])
def save_game_settings():
    """Placeholder for saving custom game parameters before play."""
    return redirect(url_for("game_play"))

# ================= API ENDPOINTS =================

@app.route("/get-question")
def get_question():
    """API endpoint to fetch a random question for the JS game engine."""
    conn = get_db()
    if not conn: return jsonify({"error": "DB unavailable"}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM questions ORDER BY RAND() LIMIT 1")
    q = cursor.fetchone()
    cursor.close()
    conn.close()

    if q:
        return jsonify({
            "question": q["question_text"],
            "option_a": q["option_a"],
            "option_b": q["option_b"],
            "option_c": q["option_c"],
            "option_d": q["option_d"],
            "correct_option": q["correct_answer"]
        })
    return jsonify({"error": "No data found"}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)