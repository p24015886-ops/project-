let correctOption = "";
let score = 0;
let totalQuestions = 10;
let currentQuestion = 0;
let correctCount = 0;
let wrongCount = 0;

function loadQuestion() {
    if (currentQuestion >= totalQuestions) {
        endGame();
        return;
    }

    fetch("/get-question")
        .then(res => res.json())
        .then(q => {
            document.getElementById("question").innerText = q.question;
            document.getElementById("A").innerText = q.option_a;
            document.getElementById("B").innerText = q.option_b;
            document.getElementById("C").innerText = q.option_c;
            document.getElementById("D").innerText = q.option_d;
            correctOption = q.correct_option;
        });

    currentQuestion++;
}

function checkAnswer(choice) {
    if (choice === correctOption) {
        score += 10;
        correctCount++;
    } else {
        wrongCount++;
    }

    document.getElementById("score").innerText = score;

    setTimeout(loadQuestion, 800);
}

function endGame() {
    alert("Game Over! Your Score: " + score);

    fetch("/save-result", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            score: score,
            total_questions: totalQuestions,
            correct: correctCount,
            wrong: wrongCount
        })
    })
    .then(res => res.json())
    .then(data => {
        console.log(data.message);
        window.location.href = "/";
    });
}

window.onload = loadQuestion;
