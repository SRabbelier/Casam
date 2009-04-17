var savelm = createRequestObject();

function handleResponseSaveLandmark() {
    if(savelm.readyState == 4){
        var response = savelm.responseText;
          $('ajax_result').innerHTML = response;
        var update = new Array();
    }
}

function saveLandMark(id){
  var mousex = $('MouseX').value;
  var mousey = $('MouseY').value;

   savelm.open('post', '/landmarks/save');
   savelm.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
   savelm.onreadystatechange = handleResponseSaveLandmark;
   savelm.send('x='+escape(mousex)+'&y='+escape(mousey));

}