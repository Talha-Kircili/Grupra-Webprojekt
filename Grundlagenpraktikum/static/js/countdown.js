function timer(seconds) {
    remainTime = Date.now() + (seconds * 1000);
    displayTimeLeft(seconds);
    intervalTimer = setInterval(function() {
        timeLeft = Math.round((remainTime - Date.now()) / 1000);
        if(timeLeft < 60) {
            clearInterval(intervalTimer);
            return displayTimeLeft(0);
        }
        displayTimeLeft(timeLeft);
    }, 1000);
}

function displayTimeLeft(timeLeft) {
    hours = Math.floor(timeLeft / 3600);
    minutes = Math.floor(timeLeft / 60)-(hours*60);
    displayOutput.textContent = `${hours < 10 ? '0' : ''}${hours}:${minutes < 10 ? '0' : ''}${minutes}`;
}

function countdown(time) {
    total_minutes = 180; // Gesamtzeit
    today = new Date();
    if(time == 'None')
        return displayTimeLeft(0);
    time = time.split(':');
    time_hour = parseInt(time[0])+parseInt(total_minutes/60);
    time_minute = parseInt(time[1])+total_minutes%60;
    timeLeft = ((time_hour - today.getHours())*60 + time_minute - today.getMinutes())*60 - today.getSeconds() - 1;
    if(timeLeft > total_minutes*60 || timeLeft < 0)
        return displayTimeLeft(0);
    timer(timeLeft);
}
