import mysql.connector
from mysql.connector import Error

connection = None

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Root@1234"
    )

    cursor = connection.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS science_quiz")
    cursor.execute("USE science_quiz")

    # ================= WORKSHOPS =================
    # category and target_level use plain strings (not restricted ENUMs)
    # so the app can store any value like "physics", "upper_primary", etc.
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

    # ================= QUESTIONS =================
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

    # ================= USERS =================
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

    # ================= QUIZ ATTEMPTS =================
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
            FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE,
            FOREIGN KEY (workshop_id)
                REFERENCES workshops(id)
                ON DELETE CASCADE
        )
    """)

    connection.commit()
    print("✅ Database & Tables Created Successfully")
    print("🚀 Science Quiz System Ready")

except Error as e:
    print("❌ Error:", e)

finally:
    if connection and connection.is_connected():
        cursor.close()
        connection.close()
        print("✅ Connection Closed")