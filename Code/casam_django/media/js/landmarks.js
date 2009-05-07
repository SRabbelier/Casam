var savelm = createRequestObject();

var savex;
var savey;
var mmid;
function handleResponseSaveLandmark() {
    if(savelm.readyState == 4){
        var response = savelm.responseText;
          $('ajax_result').innerHTML = response;
          $('lmdd').hide();
          $('mm'+mmid).setStyle('position: absolute; left: '+savex+'px; top: '+savey+'px;');
    }
}

function saveLandMark(){

  var mousex = $('lmmx').value;
  var mousey = $('lmmy').value;
  var mm = $('mmmeting').options[$('mmmeting').selectedIndex].value;
  savex = mousex*1+$('big_image1').offsetLeft*1;
  savey = mousey*1+$('big_image1').offsetTop*1;
  mmid = mm;
  
  if(mm == "" || mousex == "" || mousey == ""){
    alert("you suck!");
  }
  else{
   savelm.open('post', base_path + 'landmarks/save');
   savelm.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
   savelm.onreadystatechange = handleResponseSaveLandmark;
   savelm.send('x='+escape(mousex)+'&y='+escape(mousey)+'&mm='+escape(mm));
  }
}

function LoadMMDD(id){
  var mousex = $('MouseX').value;
  xoffset = $('big_image1').offsetLeft*1+mousex*1+10;
  var mousey = $('MouseY').value;
  yoffset = $('big_image1').offsetTop*1+mousey*1+10;
  $('lmdd').setStyle('left: '+xoffset+'px; top: '+yoffset+'px;');
  $('lmmx').value = mousex;
  $('lmmy').value = mousey;
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

