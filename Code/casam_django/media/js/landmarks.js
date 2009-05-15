var savelm = createRequestObject();

var savex;
var savey;

function undoLastLandmarkChange(x, y, potid, imgid, mid){
  if (mid == '')
  	reloadUndonePlace(potid,imgid);
  else{
	  new Ajax.Request(base_path + 'landmarks/save',{
  		method:'post',
  		parameters:{x:escape(x),
  								y:escape(y),
  								mm:escape(potid),
  								imgid:escape(imgid),
  								imagewidth:$('addedImage_'+imgid).width,
  								imageheight:$('addedImage_'+imgid).height},
  		onSuccess:function(){
  			reloadUndoneChange(mid,x,y);
	  	}
  	});
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
  
  var c = '';
  var measurement = null;
  
  if (!$('mmmeting').disabled){ 
  	var found = false;
  	for(var i = 0; i < measurements.length; i++){
  		if(measurements[i].potid == mm && measurements[i].imageid == imageID){
  			found = true;
  			measurement = measurements[i];
  			break;
  		}
  	};
  	if(found){
	  	c = new Change('r', mm, $('mmmeting').options[$('mmmeting').selectedIndex].text);
			c.position(Math.round(measurement.left), Math.round(measurement.top));
			c.reposition(measurement.id, mousex, mousey);
  	}
  	else{
  		c = new Change('p', mm, $('mmmeting').options[$('mmmeting').selectedIndex].text);
  		c.position(mousex, mousey);
  	}
	 	c.add();
		changes.push(c);
  }
  
  if(mm == "" || mousex == "" || mousey == ""){
    alert("Please select a landmark!");
  }
  else{
	  new Ajax.Request(base_path + 'landmarks/save',{
	  	method:'post',
	  	parameters:{x:escape(mousex),
	  							y:escape(mousey),
	  							mm:escape(mm),
	  							imgid:escape(imageID),
	  							imagewidth:$('addedImage_'+imageID).width,
	  							imageheight:$('addedImage_'+imageID).height},
	  	onSuccess:function(transport,json){
      	c = changes.pop();
      	c.save();
      	changes.push(c);
      	var found = false;
    	  for(var i = 0; i < measurements.length; i++){
    	  	if (measurements[i].potid == mm && measurements[i].imageid == imageID){
    	  		var found = true;
    	  		measurement = measurements[i];
    	  		break;
    	  	}
    	  }
    	  if (found){
	    	  measurement.calcpieces();
	    	  measurement.setPlace(mousex/measurement.piecex,mousey/measurement.piecey);
	    	  measurement.place();
	        var currentMeasurements = $('bottomDiv'+measurement.imageid).childElements()[1].childElements()[2].childElements();
		      for(var i = 0; i < currentMeasurements.length; i++){
		        if (currentMeasurements[i].childElements()[0].name == measurement.id){
		          currentMeasurements[i].childElements()[1].update(measurement.name+' ('+Math.round(measurement.x)+','+Math.round(measurement.y)+')');
		          new Effect.Highlight(currentMeasurements[i]);                                                           
		          break;                                                              
		        }                                                    
		      }
    	  }
    	  else{
    	  	var json = transport.responseText.evalJSON();
    	  	//json[i] = meting
    	  	//json[i+1] = image
    	  	createMeasurement(c.lmname, json[1].fields.name, mousex, mousey, json[0].pk, mm, 
    	  										json[1].pk, json[0].fields.imagewidth, json[0].fields.imageheight);
    	  	for(var i = 0; i < measurements.length; i++){
	    	  	if (measurements[i].potid == mm && measurements[i].imageid == imageID){
	    	  		measurement = measurements[i];
	    	  		break;
	    	  	}
	    	  }									
    	  	measurement.calcpieces();
	    	  measurement.setPlace(mousex/measurement.piecex,mousey/measurement.piecey);
	    	  measurement.place();
    	  }
      	  
      	$('lmdd').hide();
	  	}
	  });   
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

