var distanceError = '';
var distanceRelation = '';
function makeDistanceDiv(){
  $('rightFrame_content').insert(newTab('Distances', $('tab_distances'), false, false));
  mainDiv = new Element('div');
  
  labelL = new Element('label').update('Afstand camera:');
  inputL = new Element('input', { 'id' : 'distanceL'});
  mainDiv.insert(labelL);
  mainDiv.insert(inputL);
  mainDiv.insert(new Element('br'));
  
  labelMin = new Element('label').update('Min. afstand:')
  inputMin = new Element('input', { 'id' : 'distancedepthMin'});
  mainDiv.insert(labelMin);
  mainDiv.insert(inputMin);
  mainDiv.insert(new Element('br'));
    
  labelMax = new Element('label').update('Max. afstand:')
  inputMax = new Element('input', { 'id' : 'distancedepthMax'});
  mainDiv.insert(labelMax);
  mainDiv.insert(inputMax);
  mainDiv.insert(new Element('br'));
  
  calcError = new Element('button').update('bereken');
  calcError.setStyle('display: block');
  calcError.observe('click', function(){
    calcDistanceError();
  });
  mainDiv.insert(calcError);
   
  $('tab_distances').insert(newTab('instellingen', mainDiv, true, true));
  mainDiv = new Element('div');

  calcCalibration = new Element('button').update('Kalibreer');
  calcCalibration.setStyle('display: block');
  calcCalibration.observe('click', function(){
    cpos1x = '';
    cpos1y = '';
    cpos2x = '';
    cpos2y = '';
    startCalibration();
  });
  mainDiv.insert(calcCalibration);
  
  labelPixCm = new Element('label').update('Verhouding px - cm:')
  inputPixCm = new Element('input', { 'id' : 'distancePixCm', 'disabled': 'disabled'});
  mainDiv.insert(labelPixCm);
  mainDiv.insert(inputPixCm);
  
  $('tab_distances').insert(newTab('kalibratie', mainDiv, false, true));
  mainDiv = new Element('div');
  calcDistance = new Element('button').update('Meet afstand');
  calcDistance.setStyle('display: block');
  calcDistance.observe('click', function(){
    pos1x = '';
    pos1y = '';
    pos2x = '';
    pos2y = '';
    startDistanceMeas();
  });
  mainDiv.insert(calcDistance);
  
  labelDistance = new Element('label').update('gemeten afstand:')
  inputDistance = new Element('input', { 'id' : 'Distancemeas', 'disabled': 'disabled'});
  mainDiv.insert(labelDistance);
  mainDiv.insert(inputDistance);
  
  $('tab_distances').insert(newTab('meten', mainDiv, false, true));

}

function calcDistanceError(){
  var L = ($('distanceL').value)*1;
  var min = ($('distancedepthMin').value)*1;
  var max = ($('distancedepthMax').value)*1;
  if(L && min && max){
    //error we can't solve
    var ls = L/(L-max);
    var rs = L/(L-min);
    var error = (ls-rs)/(max-min);
    distanceError = error;
    
    // Relation between ruler layer and meausering layer
    var mean = (max+min)/2;
    var mid = L/(L+mean);
    distanceRelation = mid;
  }
  else{
    alert('All fields are required!');
  }
}

  var cpos1x = '';
  var cpos1y = '';
  var cpos2x = '';
  var cpos2y = '';
  var cdistancecm = '9';
  
function startCalibration(){
  if(addedImages[0]){
    if(cpos1x == ''){
      addedImages[0].imageElement.stopObserving('click');
      addedImages[0].imageElement.observe('click', function(){
        setCalibrationPos(1);
      });
    }
    else if(cpos2x == ''){
    addedImages[0].imageElement.stopObserving('click');
      addedImages[0].imageElement.observe('click', function(){
        setCalibrationPos(2);
      });
    }
    else{
      var distancepx = Math.sqrt(Math.pow(Math.abs((cpos2x-cpos1x)),2)+Math.pow(Math.abs((cpos2y-cpos1y)),2));
      $('distancePixCm').value = cdistancecm/distancepx;
    }
  }
  else{
    alert('First open the image!');
  }
}

function setCalibrationPos(pos){
  if(pos == 1){
    cpos1x = $('MouseX').value;
    cpos1y = $('MouseY').value;
  }
  else{
    cpos2x = $('MouseX').value;
    cpos2y = $('MouseY').value;
  }
  startCalibration();
}

  var pos1x = '';
  var pos1y = '';
  var pos2x = '';
  var pos2y = '';

function startDistanceMeas(){
  if($('distancePixCm').value != '' && distanceRelation){
    if(pos1x == ''){
      addedImages[0].imageElement.stopObserving('click');
      addedImages[0].imageElement.observe('click', function(){
        setDistancePos(1);
      });
    }
    else if(pos2x == ''){
    addedImages[0].imageElement.stopObserving('click');
      addedImages[0].imageElement.observe('click', function(){
        setDistancePos(2);
      });
    }
    else{
      var distancepx = Math.sqrt(Math.pow(Math.abs((pos2x-pos1x)),2)+Math.pow(Math.abs((pos2y-pos1y)),2));
      var distancecm = distancepx * $('distancePixCm').value;
      var realdistancecm = distancecm * distanceRelation;
      $('Distancemeas').value = realdistancecm;
    }
  }
  else{
    alert('First calculate the calculation error and calibrate!');
  }
}

function setDistancePos(pos){
  if(pos == 1){
    pos1x = $('MouseX').value;
    pos1y = $('MouseY').value;
  }
  else{
    pos2x = $('MouseX').value;
    pos2y = $('MouseY').value;
  }
  startDistanceMeas();
}