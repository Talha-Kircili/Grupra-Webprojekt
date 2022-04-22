function main(time_, status_, reports_) {
	displayOutput = document.getElementById('display-remain-time');
	countdown(time_);
	if (status_ != 'True')
		return;
	time = 30;
	reports = parseInt(reports_);
	box = document.getElementById("matrix_toggle");
	box.addEventListener('click', function() {localStorage.setItem('collapse', !box.checked);});
	if (localStorage.getItem('collapse') == "true")
		box.checked = false;
	counter = time-1;
	table(JSON.parse(document.getElementById('progress').textContent));
	if (counter>0 || reports<1)
		window.setInterval(function() {
			if (!counter)
				location.reload();
			if (reports < 1)
				fetch_get('?refresh=True').then(data => {
					if (data && !reports)
						location.reload();
					reports = data;
				});
			counter--;
		}, 1000);
}

function table(progress) {
	table = document.createElement('table');
	table.setAttribute('id', 'styled-table');
	thead = document.createElement('thead');
	tr = document.createElement('tr');
	dummy = document.createElement('th');
	/* table head */
	tr.appendChild(dummy);
	for (i=1;i<5;i++)
		for (j=1;j<7;j++) {
			th = document.createElement('th');
			th.innerHTML="PC-"+String(i)+String(j);
			tr.appendChild(th);
		}
	thead.appendChild(tr);
	table.appendChild(thead);
	/* table body */
	tbody = document.createElement('tbody');
	for (aufgabe of Object.keys(progress)) {
		tr = document.createElement('tr');
		let td = document.createElement('td');
		td.innerHTML=aufgabe;
		tr.appendChild(td);
		for (s of progress[aufgabe]) {
			let td1 = document.createElement('td');
			if (s)
				td1.style.backgroundColor = '#00ff00';
			else
				td1.style.backgroundColor = '#ff0000';
			tr.appendChild(td1);
		}
		tbody.appendChild(tr);
	}
	table.appendChild(tbody);
	place = document.getElementById('matrix');
	place.appendChild(table);
	place.appendChild(document.createElement('p'));
}

function fetch_get(url) {
	return fetch(url, {
		method: "GET",
		headers: {'Content-Type': 'application/json', "X-CSRFToken": "{{ csrf_token }}"}, 
	}).then(response=>response.json()).then(data=> {return data;})
}
