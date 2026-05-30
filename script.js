let seconds = 0;
let timerInterval = null;
let startTime = null;

function startTimer() {
    if (timerInterval !== null) return;

    startTime = new Date();

    timerInterval = setInterval(() => {
        seconds++;
        displayTimer();
    }, 1000);
}

function displayTimer() {
    let hrs = Math.floor(seconds / 3600);
    let mins = Math.floor((seconds % 3600) / 60);
    let secs = seconds % 60;

    document.getElementById("timer").innerText =
        String(hrs).padStart(2, "0") + ":" +
        String(mins).padStart(2, "0") + ":" +
        String(secs).padStart(2, "0");
}

function stopTimer() {
    let managerName = document.getElementById("managerName").value;
    let task = document.getElementById("task").value;

    if (!managerName || !task) {
        alert("Please enter manager name and task");
        return;
    }

    if (timerInterval === null) {
        alert("Timer is not running");
        return;
    }

    clearInterval(timerInterval);
    timerInterval = null;

    let endTime = new Date();

    let data = {
        manager_name: managerName,
        task: task,
        start_time: startTime.toLocaleTimeString(),
        end_time: endTime.toLocaleTimeString(),
        duration_minutes: Math.ceil(seconds / 60)
    };

    fetch("/save-session", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(result => {
        alert(result.message);
        resetTimer();
        loadSessions();
    });
}

function resetTimer() {
    clearInterval(timerInterval);
    timerInterval = null;
    seconds = 0;
    startTime = null;
    displayTimer();
}

function loadSessions() {
    fetch("/sessions")
    .then(res => res.json())
    .then(data => {
        let table = document.getElementById("sessionTable");
        table.innerHTML = "";

        data.forEach(session => {
            table.innerHTML += `
                <tr>
                    <td>${session.manager_name}</td>
                    <td>${session.task}</td>
                    <td>${session.start_time}</td>
                    <td>${session.end_time}</td>
                    <td>${session.duration_minutes} min</td>
                    <td>${session.work_date}</td>
                </tr>
            `;
        });
    });
}

loadSessions();