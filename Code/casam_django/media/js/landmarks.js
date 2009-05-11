var savelm = createRequestObject();

var savex;
var savey;
var mmid;
function handleResponseSaveLandmark() {
    if(savelm.readyState == 4){
        var response = savelm.responseText;
          $('ajax_result').update(response);
          closePopupAndReloadCurrentMeasurements();
          $('lmdd').hide();
          $('mm'+mmid).setStyle('position: fixed; left: '+savex+'px; top: '+savey+'px;');
    }
}

function saveLandMark(){
  var viewportOffset = $('big_images').viewportOffset();
  var mousex = $('lmmx').value;
  var mousey = $('lmmy').value;
  var mm = $('mmmeting').options[$('mmmeting').selectedIndex].value;
  var imageID = $('imgid').value;
  savex = mousex*1+viewportOffset.left*1;
  savey = mousey*1+viewportOffset.top*1;
  mmid = mm;
  
  if(mm == "" || mousex == "" || mousey == ""){
    alert("Please select a landmark!");
  }
  else{
   savelm.open('post', base_path + 'landmarks/save');
   savelm.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
   savelm.onreadystatechange = handleResponseSaveLandmark;
   savelm.send('x='+escape(mousex)+'&y='+escape(mousey)+'&mm='+escape(mm)+'&imgid='+escape(imageID));
  }
}

function LoadMMDD(id, imgID){
  var viewportOffset = $('big_images').viewportOffset();                       

  var mousex = $('MouseX').value;
  var mousey = $('MouseY').value;
  var xoffset = mousex*1+viewportOffset.left+10;
  var yoffset = mousey*1+viewportOffset.top+10;
  
  var imageID = imgID
  
  $('lmdd').setStyle('left: '+xoffset+'px; top: '+yoffset+'px;');
  $('lmmx').value = mousex;
  $('lmmy').value = mousey;
  $('imgid').value = imageID;
  if(id != ""){
    $('option'+id).selected = true;
    $('mmmeting').setStyle('visibility: hidden');
    $('labelmmmeting').setStyle('visibility: hidden');
  }
  else{
    $('mmmeting').setStyle('visibility: visible');
    $('labelmmmeting').setStyle('visibility: visible');
  }
  $('lmdd').show();
}

function showLandmarkTooltip(e){
  if($('MouseX').value != "" && $('MouseY').value != ""){
    xoffset = e.currentTarget.offsetLeft*1+12;
    yoffset = e.currentTarget.offsetTop*1-5;
    var tooltip = e.currentTarget.parentNode.lastChild
    tooltip.setStyle('left: '+xoffset+'px; top: '+yoffset+'px;');
    tooltip.show();
  }                     
}
function hideLandmarkTooltip(e){
  var tooltip = e.currentTarget.parentNode.lastChild
  tooltip.hide();
}

