var savelm = createRequestObject();

function handleResponseSaveLandmark() {
    if(savelm.readyState == 4){
        var response = savelm.responseText;
          $('ajax_result').innerHTML = response;
        var update = new Array();
    }
}

function saveLandMark(){

  var mousex = $('lmmx').value;
  var mousey = $('lmmy').value;
  var mm = $('mmmeting').options[$('mmmeting').selectedIndex].value;
  if(mm == "" || mousex == "" || mousey == ""){
    alert("you suck!");
  }
  else{
   savelm.open('post', '../landmarks/save');
   savelm.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
   savelm.onreadystatechange = handleResponseSaveLandmark;
   savelm.send('x='+escape(mousex)+'&y='+escape(mousey)+'&mm='+escape(mm));
  }
}

function LoadMMDD(){

  var mousex = $('MouseX').value;
  xoffset = $('big_image1').offsetLeft*1+mousex*1+10;
  var mousey = $('MouseY').value;
  yoffset = $('big_image1').offsetTop*1+mousey*1+10;
  $('lmdd').setStyle('left: '+xoffset+'px; top: '+yoffset+'px;');
  $('lmmx').value = mousex;
  $('lmmy').value = mousey;
  $('lmdd').show();
}

document.observe("dom:loaded", function() {
	if($('photosContextMenu'))
	{
		new Draggable('photosContextMenu');
	}
});
