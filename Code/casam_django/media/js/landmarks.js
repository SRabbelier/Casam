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
   savelm.send('x='+escape(mousex)+'&y='+escape(mousey)+'&mm='+escape(mm)+'&imgid='+escape(imageID)+'&imagewidth='+$('addedImage_'+imageID).width+'&imageheight='+$('addedImage_'+imageID).height);
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
    $('mmmeting').setStyle('visibility: visible');
    $('mmmeting').disabled = true;
    $('labelmmmeting').setStyle('visibility: visible');
  }
  else{
    $('mmmeting').setStyle('visibility: visible');
    $('mmmeting').disabled = false;
    $('labelmmmeting').setStyle('visibility: visible');
  }
  $('lmdd').show();
}

function showLandmarkTooltip(e){
  obj=(!e.target?e.srcElement:e.target);
  if($('MouseX').value != "" && $('MouseY').value != ""){
    xoffset = obj.offsetLeft*1+12;
    yoffset = obj.offsetTop*1-5;
    var tooltip = obj.parentNode.lastChild
    tooltip.setStyle('left: '+xoffset+'px; top: '+yoffset+'px;');
    tooltip.show();
  }                     
}
function hideLandmarkTooltip(e){
  obj=(!e.target?e.srcElement:e.target);
  var tooltip = obj.parentNode.lastChild;
  tooltip.hide();
}

