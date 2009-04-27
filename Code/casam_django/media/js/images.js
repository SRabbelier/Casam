function ChangeOp(id,value){
  $('big_image'+id).setOpacity(value);
}

function hide_image(id){
  $('big_images').removeChild($('big_image'+id));
  $('delete_images').removeChild($('delete_photo_'+id));
  $('sliders').removeChild($('track'+id));
  $('sliders').removeChild($('valueopac'+id));
  total_images--;
}

function show_image(location){
	
  var insert = 0;
  for(var i = 1; i <= total_images; i++){
    if($('big_image'+i) == null)
      insert = i;
  }
  if(insert == 0){
    total_images++;
    insert = total_images;
  }


  // Creating the new image
  var newimg = Element.extend(document.createElement('img'));
  newimg.setAttribute('src',location);
  newimg.setStyle("opacity: 0.4; filter: alpha(opacity=40); width: 1000px; cursor: crosshair;");
  newimg.observe('click', function() { LoadMMDD(""); });
  newimg.setAttribute('id','big_image'+insert);
  $('big_images').appendChild(newimg);

  // To do: make the sliders div just like the objects of the delete button
  // $('sliders').innerHTML = $('sliders').innerHTML+'<div id="track'+insert+'" style="width:200px; background-color:#ccc; height:10px;"><div id="handle'+insert+'" style="width:10px; height:15px; background-color:#f00; cursor:move;"></div></div><p id="valueopac'+insert+'">&nbsp;</p>';
  var newdiv1 = Element.extend(document.createElement('div'));
  newdiv1.setAttribute('id','track'+insert);
  newdiv1.setStyle("width:200px; background-color:#ccc; height:10px;");
  var newdiv2 = Element.extend(document.createElement('div'));
  newdiv2.setAttribute('id','handle'+insert);
  newdiv2.setStyle("width:10px; height:15px; background-color:#f00; cursor:move;");
  var newp1 = Element.extend(document.createElement('p'));
  newp1.setAttribute('id','valueopac'+insert);
  $('sliders').appendChild(newdiv1);
  newdiv1.appendChild(newdiv2);
  $('sliders').appendChild(newp1);
  eval("new Control.Slider('handle"+insert+"', 'track"+insert+"', {onSlide: function(v) { $('valueopac"+insert+"').innerHTML = 'slide: ' + v*100; ChangeOp("+insert+",v) },onChange: function(v) { $('valueopac"+insert+"').innerHTML = 'changed: ' + v*100;  ChangeOp("+insert+",v) },sliderValue: 0.4})");
      
  // Creating the delete button
  var newbutton = Element.extend(document.createElement('button'));
  newbutton.innerHTML = 'Reset foto '+insert;
  newbutton.onclick = function() { hide_image(insert) };
  newbutton.setAttribute('id','delete_photo_'+insert);
  $('delete_images').insert({ top: newbutton});
}