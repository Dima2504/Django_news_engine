document.getElementById('navbar-close').onclick = function navbar_toggle() {
	var sidebar = document.getElementById('sidebar-menu');
	var c_left = document.getElementById('chevron-left');
	var c_right = document.getElementById('chevron-right');
	
	main.classList.toggle('offset-xl-3');
	sidebar.classList.toggle("sb-off");

	c_left.classList.toggle('invisible');
	c_right.classList.toggle('invisible');
}