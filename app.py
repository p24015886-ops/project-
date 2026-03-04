from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
from mysql.connector import Error
import random

app = Flask(__name__)

# ================= MYSQL CONFIGURATION =================
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Root@1234",
    "database": "science_quiz"
}


def init_db():
    """Auto-create the database and tables if they don't exist."""
    try:
        conn = mysql.connector.connect(
            host=db_config["host"],
            user=db_config["user"],
            password=db_config["password"]
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS science_quiz")
        cursor.execute("USE science_quiz")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workshops (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(150) NOT NULL,
                description TEXT,
                category VARCHAR(100) NOT NULL,
                target_level VARCHAR(100) DEFAULT 'both',
                is_game TINYINT(1) DEFAULT 0,
                time_limit INT DEFAULT 0,
                duration_minutes INT DEFAULT 60,
                max_participants INT DEFAULT 20,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                workshop_id INT,
                question_text TEXT NOT NULL,
                question_image VARCHAR(500) NULL,
                option_a VARCHAR(255) NOT NULL,
                option_b VARCHAR(255) NOT NULL,
                option_c VARCHAR(255) NOT NULL,
                option_d VARCHAR(255) NOT NULL,
                correct_answer CHAR(1) NOT NULL,
                difficulty VARCHAR(20) DEFAULT 'medium',
                level VARCHAR(50) NOT NULL DEFAULT 'upper_primary',
                points INT DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (workshop_id)
                    REFERENCES workshops(id)
                    ON DELETE SET NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(100),
                role VARCHAR(20) DEFAULT 'student',
                level VARCHAR(50) DEFAULT 'lower_primary',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quiz_attempts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                workshop_id INT NOT NULL,
                score INT DEFAULT 0,
                total_questions INT DEFAULT 0,
                percentage DECIMAL(5,2),
                passed BOOLEAN DEFAULT FALSE,
                attempt_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (workshop_id) REFERENCES workshops(id) ON DELETE CASCADE
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Database initialized successfully")
    except Error as e:
        print(f"❌ DB Init Error: {e}")


def get_db():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(f"❌ Database Error: {e}")
        return None


# ================= NORMALIZATION HELPERS =================

def normalize_level(raw_level):
    level_map = {
        "Upper Primary":    "upper_primary",
        "Lower Primary":    "lower_primary",
        "Upper Secondary":  "upper_secondary",
        "Lower Secondary":  "lower_secondary",
        "Both":             "both",
        "upper_primary":    "upper_primary",
        "lower_primary":    "lower_primary",
        "upper_secondary":  "upper_secondary",
        "lower_secondary":  "lower_secondary",
        "both":             "both"
    }
    return level_map.get(raw_level)


def normalize_category(raw_category):
    if not raw_category:
        return None
    return raw_category.lower().replace(" ", "_")


# ================= NAVIGATION ROUTES =================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/category")
def category():
    return render_template("category.html")

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

@app.route("/games")
def games():
    """Create Games page — staff-only setup page"""
    conn = get_db()
    games_list = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM workshops WHERE is_game = 1 ORDER BY created_at DESC")
        games_list = cursor.fetchall()
        cursor.close()
        conn.close()
    return render_template("games.html", games=games_list)

@app.route("/start-games")
def start_games():
    """Start Games page — students play games created by staff"""
    return render_template("game_view.html")

@app.route("/videos")
def videos():
    return render_template("videos.html")


# ================= GET WORKSHOPS API (used by category.html dropdowns) =================

@app.route("/get-workshops/<category>")
def get_workshops_api(category):
    category = normalize_category(category)
    raw_level = request.args.get("level")
    level = normalize_level(raw_level) if raw_level else None

    conn = get_db()
    if not conn:
        return jsonify([])

    cursor = conn.cursor(dictionary=True)

    if level:
        cursor.execute(
            "SELECT id, title FROM workshops WHERE category = %s AND target_level = %s AND is_game = 0",
            (category, level)
        )
    else:
        cursor.execute(
            "SELECT id, title FROM workshops WHERE category = %s AND is_game = 0",
            (category,)
        )

    workshops = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(workshops)


@app.route("/get-games/<category>")
def get_games_api(category):
    """Get games (workshops marked as is_game=1) for start-games page"""
    category = normalize_category(category)
    raw_level = request.args.get("level")
    level = normalize_level(raw_level) if raw_level else None

    conn = get_db()
    if not conn:
        return jsonify([])

    cursor = conn.cursor(dictionary=True)

    if level:
        cursor.execute(
            "SELECT id, title FROM workshops WHERE category = %s AND target_level = %s AND is_game = 1",
            (category, level)
        )
    else:
        cursor.execute(
            "SELECT id, title FROM workshops WHERE category = %s AND is_game = 1",
            (category,)
        )

    games = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(games)


# ================= QUIZ ROUTE =================

@app.route("/quiz")
def start_quiz():
    raw_category  = request.args.get("category")
    raw_level     = request.args.get("level")
    workshop_id   = request.args.get("workshop_id")

    category = normalize_category(raw_category)
    level    = normalize_level(raw_level)

    if not category or not level:
        return redirect(url_for("category"))

    conn = get_db()
    if not conn:
        return "DB Error", 500

    cursor = conn.cursor(dictionary=True)

    # If a specific workshop was selected, pull only its questions
    if workshop_id:
        cursor.execute("""
            SELECT q.id,
                   q.question_text AS question,
                   q.option_a,
                   q.option_b,
                   q.option_c,
                   q.option_d,
                   q.correct_answer
            FROM questions q
            WHERE q.workshop_id = %s
            ORDER BY RAND()
            LIMIT 15
        """, (workshop_id,))
    else:
        cursor.execute("""
            SELECT q.id,
                   q.question_text AS question,
                   q.option_a,
                   q.option_b,
                   q.option_c,
                   q.option_d,
                   q.correct_answer
            FROM questions q
            JOIN workshops w ON q.workshop_id = w.id
            WHERE w.category = %s
              AND w.target_level = %s
              AND w.is_game = 0
            ORDER BY RAND()
            LIMIT 15
        """, (category, level))

    questions = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("quiz.html", questions=questions,
                           error="No questions found for this selection." if not questions else None)


# ================= RESULT ROUTE =================

@app.route("/result")
def result():
    score      = int(request.args.get("score", 0))
    total      = int(request.args.get("total", 0))
    percentage = round((score / total * 100) if total else 0)
    return render_template("result.html", score=score, total=total, percentage=percentage)


# ================= GAME QUESTIONS API (for game_view.html) =================

@app.route("/api/game-questions")
def game_questions():
    raw_category = request.args.get("category")
    raw_level    = request.args.get("level")
    workshop_id  = request.args.get("workshop_id")

    category = normalize_category(raw_category)
    level    = normalize_level(raw_level)

    conn = get_db()
    if not conn:
        return jsonify([])

    cursor = conn.cursor(dictionary=True)

    if workshop_id:
        cursor.execute("""
            SELECT q.question_text AS question,
                   q.option_a,
                   q.option_b,
                   q.option_c,
                   q.option_d,
                   q.correct_answer,
                   q.question_image
            FROM questions q
            WHERE q.workshop_id = %s
            ORDER BY RAND()
        """, (workshop_id,))
    elif category and level:
        cursor.execute("""
            SELECT q.question_text AS question,
                   q.option_a,
                   q.option_b,
                   q.option_c,
                   q.option_d,
                   q.correct_answer,
                   q.question_image
            FROM questions q
            JOIN workshops w ON q.workshop_id = w.id
            WHERE w.category = %s
              AND w.target_level = %s
              AND w.is_game = 1
            ORDER BY RAND()
        """, (category, level))
    else:
        return jsonify([])

    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)


# ================= CREATE WORKSHOP (FORM BASED) =================

@app.route("/create-workshop", methods=["POST"])
def create_workshop():
    title       = request.form.get("title")
    description = request.form.get("description")
    raw_category = request.form.get("category")
    raw_level   = request.form.get("level")

    category = normalize_category(raw_category)
    level    = normalize_level(raw_level)

    conn = get_db()
    if not conn:
        return "DB Error", 500

    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO workshops (title, description, category, target_level, is_game)
            VALUES (%s, %s, %s, %s, 0)
        """, (title, description, category, level))
        conn.commit()
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("make_quiz"))


# ================= DELETE WORKSHOP =================

@app.route("/delete-workshop/<int:workshop_id>")
def delete_workshop(workshop_id):
    conn = get_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM questions WHERE workshop_id = %s", (workshop_id,))
        cursor.execute("DELETE FROM workshops WHERE id = %s", (workshop_id,))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for("make_quiz"))


@app.route("/delete-game/<int:workshop_id>")
def delete_game(workshop_id):
    conn = get_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM questions WHERE workshop_id = %s", (workshop_id,))
        cursor.execute("DELETE FROM workshops WHERE id = %s", (workshop_id,))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for("games"))


# ================= ADD SINGLE QUESTION =================

@app.route("/add-question/<int:workshop_id>", methods=["POST"])
def add_question(workshop_id):
    q_text  = request.form.get("question_text")
    a       = request.form.get("option_a")
    b       = request.form.get("option_b")
    c       = request.form.get("option_c")
    d       = request.form.get("option_d")
    correct = request.form.get("correct_answer")

    conn = get_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO questions
            (workshop_id, question_text, option_a, option_b,
             option_c, option_d, correct_answer)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (workshop_id, q_text, a, b, c, d, correct))
        conn.commit()
        cursor.close()
        conn.close()

    return redirect(url_for("make_quiz"))


# ================= JSON BULK PUBLISH (Quiz) =================

@app.route("/api/publish-workshop", methods=["POST"])
def publish_workshop_api():
    try:
        data = request.get_json()
        print("📥 DATA RECEIVED:", data)

        title        = data.get("title")
        description  = data.get("description")
        raw_category = data.get("category")
        raw_level    = data.get("level")
        questions    = data.get("questions")

        category = normalize_category(raw_category)
        level    = normalize_level(raw_level)

        if not title or not category or not level or not questions:
            return jsonify({"error": "Invalid or missing fields"}), 400

        conn = get_db()
        if not conn:
            return jsonify({"error": "DB connection failed"}), 500

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO workshops (title, description, category, target_level, is_game)
            VALUES (%s, %s, %s, %s, 0)
        """, (title, description, category, level))

        workshop_id = cursor.lastrowid
        print("🆕 Quiz Workshop ID:", workshop_id)

        for q in questions:
            cursor.execute("""
                INSERT INTO questions
                (workshop_id, question_text, option_a, option_b,
                 option_c, option_d, correct_answer, level)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                workshop_id,
                q.get("text"),
                q.get("a"),
                q.get("b"),
                q.get("c"),
                q.get("d"),
                q.get("answer"),
                level
            ))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"success": True})

    except Exception as e:
        print("🔥 ERROR:", e)
        return jsonify({"error": str(e)}), 500


# ================= JSON BULK PUBLISH (Game) =================

@app.route("/api/publish-game", methods=["POST"])
def publish_game_api():
    try:
        data = request.get_json()
        print("📥 GAME DATA RECEIVED:", data)

        title        = data.get("title")
        description  = data.get("description")
        raw_category = data.get("category")
        raw_level    = data.get("level")
        questions    = data.get("questions")
        time_limit   = data.get("time_limit", 0)

        category = normalize_category(raw_category)
        level    = normalize_level(raw_level)

        if not title or not category or not level or not questions:
            return jsonify({"error": "Invalid or missing fields"}), 400

        conn = get_db()
        if not conn:
            return jsonify({"error": "DB connection failed"}), 500

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO workshops (title, description, category, target_level, is_game, time_limit)
            VALUES (%s, %s, %s, %s, 1, %s)
        """, (title, description, category, level, time_limit))

        workshop_id = cursor.lastrowid
        print("🆕 Game Workshop ID:", workshop_id)

        for q in questions:
            cursor.execute("""
                INSERT INTO questions
                (workshop_id, question_text, option_a, option_b,
                 option_c, option_d, correct_answer, level, question_image)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                workshop_id,
                q.get("text"),
                q.get("a"),
                q.get("b"),
                q.get("c"),
                q.get("d"),
                q.get("answer"),
                level,
                q.get("image", None)
            ))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"success": True})

    except Exception as e:
        print("🔥 ERROR:", e)
        return jsonify({"error": str(e)}), 500


# ================= GET WORKSHOP QUESTIONS (for edit) =================

@app.route("/api/workshop-questions/<int:workshop_id>")
def get_workshop_questions(workshop_id):
    conn = get_db()
    if not conn:
        return jsonify([])
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
    try:
        data      = request.get_json()
        questions = data.get("questions", [])

        conn = get_db()
        if not conn:
            return jsonify({"error": "DB error"}), 500

        cursor = conn.cursor()

        # Delete old questions and re-insert
        cursor.execute("DELETE FROM questions WHERE workshop_id = %s", (workshop_id,))

        for q in questions:
            cursor.execute("""
                INSERT INTO questions
                (workshop_id, question_text, option_a, option_b,
                 option_c, option_d, correct_answer)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                workshop_id,
                q.get("text"),
                q.get("a"),
                q.get("b"),
                q.get("c"),
                q.get("d"),
                q.get("answer")
            ))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================= RUN APP =================

if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5050, debug=True)




