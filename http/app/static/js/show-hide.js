	function clearText(thefield){
	if (thefield.defaultValue==thefield.value)
	thefield.value = ""
	}
	function hideDiv(d) {
		document.getElementById(d).style.display = "none";
	}
	function showDiv(d) {
		document.getElementById(d).style.display = "block";
	}

	var imgExp = "../imgs/expanded.gif";
	var imgColl = "../imgs/collapsed.gif";
	function switchElSwitchImg(el_id, img_id) {
		var el = document.getElementById(el_id);
		var img = document.getElementById(img_id);
		if (el != null && img != null)	{
			if (el.style.display != "none") {
				el.style.display = "none";
				img.src = imgColl;
			}
			else {
				el.style.display = "table-cell";
				img.src = imgExp;
			}
		}
	}
	function showClick(el_id,t) {
		var el = document.getElementById(el_id);
		var txt = document.getElementById(t);
		if (el != null)	{
			if (el.style.display == "block") {
				el.style.display = "none";
				txt.innerHTML = "show";
			}
			else {
				el.style.display = "block";
				txt.innerHTML = "hide";
			}
		}
	}