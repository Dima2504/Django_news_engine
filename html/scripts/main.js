// document.getElementById('navbar-three-stripes').onclick = function navbar_toggle() {
// 	var sidebar = document.getElementById('sidebar-menu');
// 	sidebar.classList.toggle('invisible');
// 	var main = document.getElementById('main');
// 	main.classList.toggle('offset-xl-3');
// 	main.style.transition = '0.3s';
// }
document.getElementById('navbar-three-stripes').onclick = function navbar_toggle() {
	var sidebar = document.getElementById('sidebar-menu');
	main.classList.toggle('offset-xl-3');
	if(sidebar.style.marginLeft == '-1500px'){
		sidebar.style.marginLeft = '0';
	} else {
		sidebar.style.marginLeft = '-1500px';
	}
	sidebar.style.transition = '0.3s';
	main.style.transition = '0.3s';

	if(main.style.width <= 789.33){
		sidebar.classList.toggle('active');
	}
}