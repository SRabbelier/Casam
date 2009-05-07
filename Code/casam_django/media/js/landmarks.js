var savelm = createRequestObject();

var savex;
var savey;
var mmid;
function handleResponseSaveLandmark() {
    if(savelm.readyState == 4){
        var response = savelm.responseText;
          $('ajax_result').innerHTML = response;
          $('lmdd').hide();
          $('mm'+mmid).setStyle('position: absolute; left: '+savex+'px; top: '+savey+'px; zIndex: 2');
    }
}

function saveLandMark(){

  var mousex = $('lmmx').value;
  var mousey = $('lmmy').value;
  var mm = $('mmmeting').options[$('mmmeting').selectedIndex].value;
  var imageID = $('imgid').value;
  savex = mousex*1+$('big_images').firstChild.offsetLeft*1;
  savey = mousey*1+$('big_images').firstChild.offsetTop*1;
  mmid = mm;
  
  if(mm == "" || mousex == "" || mousey == ""){
    alert("you suck!");
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

function showLandmarkTooltip(id){
  if($('MouseX').value != "" && $('MouseY').value != ""){
    xoffset = $('mm'+id).offsetLeft*1+12;
    yoffset = $('mm'+id).offsetTop*1-5;
    $('tooltip'+id).setStyle('left: '+xoffset+'px; top: '+yoffset+'px;');
    $('tooltip'+id).show();
  }                     
}
function hideLandmarkTooltip(id){
  $('tooltip'+id).hide();
}

