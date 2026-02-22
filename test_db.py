import mysql.connector
from mysql.connector import Error

# Initialize connection as None to avoid NameError if the connection fails
connection = None

try:
    # === CONNECT TO MYSQL ===
    # IMPORTANT: Update 'user' and 'password' to match your local MySQL credentials
    connection = mysql.connector.connect(
        host="localhost",  # Usually 'localhost' or '127.0.0.1'
        user="root",       # Your MySQL username
        password="StrongPassword123!" # Your MySQL password
    )

    cursor = connection.cursor()

    # === CREATE DATABASE IF NOT EXISTS ===
    cursor.execute("CREATE DATABASE IF NOT EXISTS science_quiz")
    cursor.execute("USE science_quiz")

    # === 1. USERS TABLE (Students & Teachers) ===
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(100),
            role ENUM('student', 'teacher', 'admin') DEFAULT 'student',
            level ENUM('lower_primary', 'upper_primary', 'both') DEFAULT 'lower_primary',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # === 2. WORKSHOPS TABLE ===
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workshops (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            description TEXT,
            category ENUM('solar_system', '3d_pen', 'vr', 'robotics', 'chemistry', 'physics') NOT NULL,
            target_level ENUM('lower_primary', 'upper_primary', 'both') DEFAULT 'both',
            duration_minutes INT,
            max_participants INT DEFAULT 20,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # === 3. QUIZ QUESTIONS TABLE ===
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            workshop_id INT,
            question_text TEXT NOT NULL,
            option_a VARCHAR(255) NOT NULL,
            option_b VARCHAR(255) NOT NULL,
            option_c VARCHAR(255) NOT NULL,
            option_d VARCHAR(255) NOT NULL,
            correct_answer CHAR(1) NOT NULL,  -- 'A', 'B', 'C', 'D'
            difficulty ENUM('easy', 'medium', 'hard') DEFAULT 'medium',
            level ENUM('lower_primary', 'upper_primary') NOT NULL,
            points INT DEFAULT 1,
            FOREIGN KEY (workshop_id) REFERENCES workshops(id) ON DELETE SET NULL
        )
    """)

    # === 4. QUIZ ATTEMPTS TABLE ===
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

    # === 5. WORKSHOP REGISTRATIONS TABLE ===
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            workshop_id INT NOT NULL,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            attended BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (workshop_id) REFERENCES workshops(id) ON DELETE CASCADE
        )
    """)

    # === INSERT SAMPLE WORKSHOPS ===
    workshops = [
        ('Solar System Exploration', 'Learn about planets, stars, and galaxies!', 'solar_system', 'both', 60, 25),
        ('3D Pen Creations', 'Design and create 3D objects with pens', '3d_pen', 'upper_primary', 90, 15),
        ('VR Science Lab', 'Virtual reality experiments', 'vr', 'upper_primary', 45, 10),
        ('Junior Astronauts', 'Fun space facts for little ones', 'solar_system', 'lower_primary', 45, 20),
        ('3D Art for Kids', 'Simple 3D pen projects', '3d_pen', 'lower_primary', 60, 15)
    ]

    for w in workshops:
        cursor.execute("""
            INSERT IGNORE INTO workshops (title, description, category, target_level, duration_minutes, max_participants)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, w)

    # === INSERT SAMPLE QUESTIONS ===
    # Solar System - Upper Primary
    cursor.execute("""
        INSERT IGNORE INTO questions (workshop_id, question_text, option_a, option_b, option_c, option_d, correct_answer, difficulty, level, points)
        VALUES 
        (1, 'What is the largest planet in our solar system?', 'Mars', 'Saturn', 'Jupiter', 'Venus', 'C', 'easy', 'upper_primary', 1),
        (1, 'How many planets are in our solar system?', '7', '8', '9', '10', 'B', 'easy', 'upper_primary', 1),
        (1, 'What is the closest planet to the Sun?', 'Venus', 'Earth', 'Mercury', 'Mars', 'C', 'easy', 'upper_primary', 1),
        (4, 'Which planet is known as the Red Planet?', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'B', 'easy', 'lower_primary', 1),
        (4, 'What do we call a person who goes to space?', 'Pilot', 'Driver', 'Astronaut', 'Captain', 'C', 'easy', 'lower_primary', 1)
    """)

    # === INSERT SAMPLE USERS ===
    cursor.execute("""
        INSERT IGNORE INTO users (username, password, email, role, level)
        VALUES 
        ('teacher1', 'password123', 'teacher@school.com', 'teacher', 'upper_primary'),
        ('student_ali', '123456', 'ali@student.com', 'student', 'upper_primary'),
        ('student_siti', '123456', 'siti@student.com', 'student', 'lower_primary'),
        ('admin1', 'admin123', 'admin@quiz.com', 'admin', 'both')
    """)

    connection.commit()
    print("✅ MySQL Database setup complete!")
    print("📊 Science Quiz System is ready!")
    print("\nWorkshops added:")
    print("- Solar System Exploration")
    print("- 3D Pen Creations")
    print("- VR Science Lab")
    print("- Junior Astronauts")
    print("- 3D Art for Kids")

except Error as e:
    print(f"❌ Error: {e}")
    print("\nTip: Make sure your MySQL server is running and your 'root' password is correct.")

finally:
    # Check if connection exists before trying to close it
    if connection and connection.is_connected():
        cursor.close()
        connection.close()
        print("✅ MySQL connection closed.")