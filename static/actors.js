function case_actors (case_id) {

    var xmlhttp;
    var url;

    if (window.XMLHttpRequest)
    { // code for IE7+, Firefox, Chrome, Opera, Safari
	xmlhttp=new XMLHttpRequest();
    } else { // code for IE6, IE5
	xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }

    url = '/afera/' + case_id + '/podmioty/';

    xmlhttp.onreadystatechange = function() {

	var popup = document.getElementById('wydarzenie-aktorzy-'+case_id)
	if (xmlhttp.readyState==4 && xmlhttp.status==200) {
	    popup.innerHTML=xmlhttp.responseText;
	}
    }

    xmlhttp.open('GET', url, true);
    xmlhttp.send();
}

function event_actors (case_id) {

    var xmlhttp;
    var url;

    if (window.XMLHttpRequest)
    { // code for IE7+, Firefox, Chrome, Opera, Safari
	xmlhttp=new XMLHttpRequest();
    } else { // code for IE6, IE5
	xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }

    url = '/wydarzenie/' + case_id + '/podmioty/';

    xmlhttp.onreadystatechange = function() {

	var popup = document.getElementById('wydarzenie-aktorzy-'+case_id)
	if (xmlhttp.readyState==4 && xmlhttp.status==200) {
	    popup.innerHTML=xmlhttp.responseText;
	}
    }

    xmlhttp.open('GET', url, true);
    xmlhttp.send();
}
