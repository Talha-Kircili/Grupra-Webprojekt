function main(help_, time_, csrf_) {
    csrftoken = csrf_;
    rank_txt = "Platz in der Warteschlange: ";
    melden = document.getElementById('melden');
    ranks = document.getElementById('rank_text');
    priority_field = document.getElementById('priority_field');	
    displayOutput = document.getElementById('display-remain-time');
    aufgaben = JSON.parse(document.getElementById('aufgaben').textContent);
    progress = JSON.parse(document.getElementById('progress').textContent);
    table(aufgaben, progress);
    document.getElementById('help').addEventListener('submit',
        function(event) {
            event.preventDefault();
            prio=this[0].value;
            report();
        });
    help = JSON.parse(help_);
    priority_field.value=help[0];
    prio = help[0];
    rank = help[1];
    ranks.textContent = rank_txt+rank;
    /* initial visuals */
    if (!prio)
        melden.style.backgroundColor = '#82ff5f';
    else {
        ranks.hidden = false;
        melden.value = 'Abbrechen';
        melden.style.backgroundColor = '#fa4444';
    }
    countdown(time_);
    intervalId = window.setInterval(function() { interval(); }, 1000);            

    window.onload = function() {
        /* close menu */
        if (visualViewport.width <= 600)
            setTimeout(() => document.getElementById('toggle').checked = false, 1000);
    }
}

// table
function table(aufgaben, progress) {
    table = document.createElement('table');
    table.setAttribute('id', 'styled-table');
    /* table head */
    thead = document.createElement('thead');
    tr = document.createElement('tr');
    table_head = ['Aufgabe', 'Ergebnis'];
    for (column_name of table_head) {
        th = document.createElement('th');
        th.innerHTML=column_name;
        tr.appendChild(th);
    }
    thead.appendChild(tr);
    table.appendChild(thead);
    /* table body */
    tbody = document.createElement('tbody');
    for (aufgabe of aufgaben) {
        tr = document.createElement('tr');
        let td = document.createElement('td');
        let td1 = document.createElement('td');
        td1.setAttribute('class','td1');
        td.innerHTML=aufgabe.description;
        if (progress.includes(aufgabe.description)) {
            td1.innerHTML = "Geschafft";
            td1.style.backgroundColor = '#82ff5f';
        }
        /* actions */
        td1.onclick = function() {
            if (td1.innerHTML == "") {
                td1.innerHTML = "Geschafft";
                td1.style.backgroundColor = '#82ff5f';
                fetch_post({"finished": td.innerHTML});
            } else {
                td1.innerHTML = "";
                td1.style.backgroundColor = "";
                fetch_post({"unfinished": td.innerHTML});
            }
        };
        tr.appendChild(td);
        tr.appendChild(td1);
        tbody.appendChild(tr);
    }
    table.appendChild(tbody);
    document.body.appendChild(table);
}

function interval() {
    if (!prio)
        return stop();
    fetch_get('?refresh=True').then(data => {
        prio = data[0];
        rank = data[1];
    });
    ranks.textContent = rank_txt+rank;
}

function stop() {
    melden.value = 'Melden';
    melden.style.backgroundColor = '#82ff5f';
    ranks.hidden = true;
    clearInterval(intervalId);
    priority_field.value=0;
}

function report() {
    if (melden.value == 'Melden' && prio > 0) {
        fetch_post({'priority': prio});
        melden.value = 'Abbrechen';
        melden.style.backgroundColor = '#fa4444';
        ranks.hidden = false;
        intervalId = window.setInterval(function() { interval(); }, 1000);
    } else {
        if (prio > 0)
            fetch_get("?stop=True");
        stop();
    }
}

function fetch_get(url) {
    return fetch(url, {
        method: "GET",
        headers: {'Content-Type': 'application/json', "X-CSRFToken": csrftoken} 
    }).then(response => response.json()).then(data => { return data; });
}

function fetch_post(data) {
    fetch('/', {
        method: "POST",
        headers: {'Content-Type': 'application/json', "X-CSRFToken": csrftoken}, 
        body: JSON.stringify(data)
    });
}
