window.onload = function() {
	const out = document.createElement('p');
	out.innerHTML = "and js did too!";
	const body = document.getElementsByTagName('body')[0];
	body.appendChild(out);
};