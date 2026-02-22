let correctOption = "";
let score = 0;
let totalQuestions = 10;
let currentQuestion = 0;
let correctCount = 0;
let wrongCount = 0;
let isAnswered = false;

function loadQuestion() {
    if (currentQuestion >= totalQuestions) {
        endGame();
        return;
    }

    isAnswered = false;
    fetch("/get-question")
        .then(res => res.json())
        .then(q => {
            document.getElementById("question").innerText = q.question;
            document.getElementById("A").innerText = q.option_a;
            document.getElementById("B").innerText = q.option_b;
            document.getElementById("C").innerText = q.option_c;
            document.getElementById("D").innerText = q.option_d;
            correctOption = q.correct_option;

            document.querySelectorAll(".option").forEach(btn => {
                btn.classList.remove("correct", "wrong");
            });
        })
        .catch(err => {
            console.error("Error loading question:", err);
            document.getElementById("question").innerText = "Connection lost to Graviton Core.";
        });

    currentQuestion++;
}

function checkAnswer(choice) {
    if (isAnswered) return;
    isAnswered = true;

    if (choice === correctOption) {
        score += 10;
        correctCount++;
        document.getElementById(choice).classList.add("correct");
    } else {
        wrongCount++;
        document.getElementById(choice).classList.add("wrong");
        document.getElementById(correctOption).classList.add("correct");
    }

    document.getElementById("score").innerText = score;
    setTimeout(loadQuestion, 1500);
}

function endGame() {
    // Custom Modal logic could go here, for now using basic UI behavior
    const confirmed = window.confirm(`🎮 Mission Complete!\n\nScore: ${score}\nAccuracy: ${(correctCount/totalQuestions)*100}%\n\nReturn to Base?`);
    
    fetch("/save-result", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ score, correctCount, wrongCount })
    }).finally(() => {
        window.location.href = "/games";
    });
}

window.onload = loadQuestion;