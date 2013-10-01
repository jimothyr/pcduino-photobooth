$(document).ready(function() { getData()});

function getData(){
	if(typeof inta != 'undefined'){clearInterval(inta)};
	if(typeof intb != 'undefined'){clearInterval(intb)};

	$.getJSON("../Data/list.json", function(data){getImages(data["F"]);})
};

function getImages(d){

var inta = window.setInterval(//replace strip image
		function(){
		//get random image
			var rand = d[Math.floor(Math.random()*d.length)];
		//change display
			document.getElementById("slideshow").src="../Images/Montages/"+rand.ID+".jpg";
		}
	,3000);

var reset=0
var intb = window.setInterval(//replace big image + timer
		function(){
		//get random image
			var rbig = d[Math.floor(Math.random()*d.length)];
			var vpic=Math.floor(Math.random()*4+1) 
		//change display
			document.getElementById("latest").src="../Images/Pics/"+rbig.ID+vpic+".jpg";
		//check for new json
		reset++
		if(reset>=6){clearInterval(inta);clearInterval(intb);getData()}
		}
	,10000);



}