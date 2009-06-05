function createRequestObject() {
	var ro;
	var browser = navigator.appName;
	if (browser == "Microsoft Internet Explorer") {
		ro = new ActiveXObject("Microsoft.XMLHTTP");
	} else {
		ro = new XMLHttpRequest();
	}
	return ro;
}

function getProjectImages()
{
	checkAuthenticationAndExecute(function(){
				
		var url = base_path+'JSON/projectImages/'+projectID+'?time='+new Date().getTime();
		new Ajax.Request(url, {
		  method: 'get',
		  onSuccess: function(transport, json) {

		  	// Grab the picture-array
		    var json = transport.responseText.evalJSON();

		    // Build the content of the tab
		    initialisePictureTab(json);

		    // Initialise the dragging of images
		    makePicturesSortable();
        
			}
		});
	});
}

function getProjectOverlays()
{
	checkAuthenticationAndExecute(function(){
				
		var url = base_path+'JSON/projectOverlays/'+projectID+'?time='+new Date().getTime();
		new Ajax.Request(url, {
		  method: 'get',
		  onSuccess: function(transport, json) {
		  	
		  	// Grab the projectOverlay-array
		    var json = transport.responseText.evalJSON();

		    // Build the content of the tab
		    addOverlayTab(json);
		    
				// Initialise the dragging of images
		    makePicturesSortable();
        
			}
		});
	});
}


function getImageBitmaps(imgid) {
	var url = base_path + 'JSON/projectImageBitmaps/' + imgid 
			+ '?time=' + new Date().getTime();
	new Ajax.Request(url,	{
			method : 'get',
			onSuccess : function(transport, json) {
				
				// Grab the image bitmap-array
				var json = transport.responseText.evalJSON();
				
				// Build the content of the tab
				addBitmapsToPictureContainer(imgid, json);
			}
	});
}

function getImageMeasurements(imgid) {

	var url = base_path + 'JSON/projectImageCurrentMeasurements/' + imgid
			+ '?time=' + new Date().getTime();
	new Ajax.Request(url, {
			method : 'get',
			onSuccess : function(transport, json) {
				// Grab the image measurements-array
				var json = transport.responseText.evalJSON();
				// Build the content of the tab
				addMeasurementsToPictureContainer(imgid, json);
			}
	});
}



function getProjectTags()
{
	checkAuthenticationAndExecute(function(){
			
		var url = base_path+'JSON/projectTags/'+projectID+'?time='+new Date().getTime();
		new Ajax.Request(url, {
		  method: 'get',
		  onSuccess: function(transport, json) {
			  
			  // Grab the tags-array
		    var json = transport.responseText.evalJSON();
		    			     
		    // Clear the 'tags' information
		    $('tags').update();
		     
		    // Show every tag
		    for(i=0; i < json.length; i++)
					$('tags').insert(new Element('p').update(json[i].fields.name));
			}
		});
	});
}

function getProjectPotentialMeasurements()
{
  checkAuthenticationAndExecute(function(){
      
  var url = base_path+'JSON/projectPotentialMeasurements/'+projectID+'?time='+new Date().getTime();
  new Ajax.Request(url, {
    method: 'get',
    onSuccess: function(transport, json) {
			
			// Grab the potential measurements array
      var json = transport.responseText.evalJSON();

      // Clear the potential measurements tab
      $('possiblemeasurements').update();
      
      for(i=0; i < json.length; i++){
      	// For each potential measurement type, create a new subtab
      	if (json[i].model == 'casam.potentialmeasurementtype'){
      		createPotentialMeasurementType(json[i].pk, json[i].fields.name);
      	}
      	// For each potential measurement, create it
      	else{
        	createPotentialMeasurement(json[i].pk, json[i].fields.type, json[i].fields.name, json[i].fields.soort)
      	}
      }
    }
  });
  });
}

function removePotentialMeasurement(potid){
	var url = base_path + 'AJaX/deletePotentialMeasurement/?time='+new Date().getTime();
  new Ajax.Request(url, {
    method: 'get',
    parameters: {'potID': potid},
    onSuccess: function(transport, json) {
      
      // Remove potential measurement from option list
      if (!$('potmeas_'+potid).childElements()[0].hasClassName('paintoverLink'))
      	$('option'+potid).remove();
      // Delete potential measurements
      var parentPotentialMeasurements = $$('div.potMeasDiv');
      for(var i = 0; i < parentPotentialMeasurements.length; i++){
        if (parentPotentialMeasurements[i].id.slice(8) == potid){
          Effect.Fade(parentPotentialMeasurements[i]);
          parentPotentialMeasurements[i].remove();
        }                  
      }
      // Delete current measurements
      for(var j = 0; j < measurements.length; j++){
        if (measurements[j].potid == potid){
          // Hide the potential type if the current measurement is the only measurement of the type
          if ($('measidMeasDiv_'+measurements[j].id).up().childElements().length == 1)
            $('measidMeasDiv_'+measurements[j].id).up().up().hide();
          // Remove text of current measurements
          $('measidMeasDiv_'+measurements[j].id).remove();
          // Remove current measurements from array
          measurements[j].erase();
          measurements.splice(j,1);
          // correct for index-changing by 'splice' method
          j = j - 1;
        }                                             
      }
      // Delete current bitmaps
      var parentCurrentBitmaps = $$('div.projectImageBitmapDivPotId_'+potid);
      var bitmapIDs = new Array();
      for(var i = 0; i < parentCurrentBitmaps.length; i++){
				// Find the bitmap-id to remove the bitmaps from the bitmaps array
				var bitmapid = parentCurrentBitmaps[i].id.slice(10);
				bitmapIDs.push(bitmapid);
				Effect.Fade(parentCurrentBitmaps[i]);
				// Delete bitmap from big_images
				parentCurrentBitmaps[i].remove();
				$('bitmap_'+bitmapid).remove();     	
      }
      // Delete bitmaps from bitmaps array
      for(var j = 0; j < bitmapIDs.length; j++){
      	for(var i = 0; i < bitmaps.length; i++){
      		if (bitmaps[i].id == bitmapsIDs[j]){
      		  bitmaps.splice(i, 1);
      		  break;
      		}
      	}
      }
      // Since deletion cannot be undone, delete changes
      for(var i = 0; i < changes.length; i++){
        if (changes[i].potid == potid){
          changes[i].erase();
          changes.splice(i,1);
          i = i - 1;
        }
      }
    },
    onFailure:function(){
      alert('Something went wrong while deleting potential measurement '+potid);
    }
  });
}

function removePotentialType(typeid){
  var url = base_path + 'AJaX/deletePotentialMeasurementType/?time='+new Date().getTime();
  new Ajax.Request(url, {
      method: 'get',
      parameters: {'potTypeID': typeid},
      onSuccess: function(transport, json) {
        // Delete current measurements
        for(var j = 0; j < measurements.length; j++){
          if ($('potmeas_'+measurements[j].potid).up().id.slice(9) == typeid){
            measurements.splice(j,1);
            j = j - 1;
          }                                             
        }
        // Remove text of current measurements
        for(var i = 0; i < addedImages.length; i++){
          $('measurementTypesDiv_'+addedImages[i].id+'-'+typeid).remove();                                          
        }
      	// Since deletion cannot be undone, delete changes
        for(var i = 0; i < changes.length; i++){
          if ($('potmeas_'+changes[i].potid).up().id.slice(9) == typeid){
            changes[i].changeDiv.remove();
            changes.splice(i,1);
            i = i - 1;
          }
        }
        // Delete potential measurements
        var parentPotentialMeasurements = $$('div.potMeasDiv');
        var bitmapIDs = new Array();
        for(var i = 0; i < parentPotentialMeasurements.length; i++){
          if (parentPotentialMeasurements[i].up().id.slice(9) == typeid){
            Effect.Fade(parentPotentialMeasurements[i]);
        		// Remove current bitmaps
            var parentCurrentBitmaps = $$('div.projectImageBitmapDivPotId_'+parentPotentialMeasurements[i].id.slice(8))
            for(var i = 0; i < parentCurrentBitmaps.length; i++){
							// Find the bitmap-id to remove the bitmaps from the bitmaps array
      				var bmid = parentCurrentBitmaps[i].id.slice(10)
      				bitmapIDs.push(bmid);
      				// Delete bitmaps from big_images
      				$('bitmap_'+bmid).remove();
      				parentCurrentBitmaps[i].remove();
      			} 
            // Only delete measurement from option-list if measurement is no bitmap
            if (!parentPotentialMeasurements[i].childElements()[0].hasClassName('paintoverLink'))
            	$('option'+parentPotentialMeasurements[i].id.slice(8)).remove();
            parentPotentialMeasurements[i].remove();
          }                  
        }
        // Delete bitmaps from bitmap array
        for(var i = 0; i < bitmapIDs.length; i++){
        	for(var j = 0; j < bitmaps.length; j++){
        		if (bitmaps[j].id == bitmapIDs[i])
        		  bitmaps.splice(j, 1);
        		  break;
        	}
        }
        // Delete potential measurements group
        var parentPotentialMeasurementTypes = $$('div.projectPotentialTypeDiv');
        for(var i = 0; i < parentPotentialMeasurementTypes.length; i++){
          if (parentPotentialMeasurementTypes[i].id.slice(9) == typeid){
            Effect.Fade(parentPotentialMeasurementTypes[i].up());
            $('optgroup_'+typeid).remove();
            parentPotentialMeasurementTypes[i].up().remove();                                                              
          }                                                                
        }          
      },
      onFailure:function(){
        alert('Something went wrong while deleting potential measurement '+containerDiv.childElements()[0].innerHTML);
      }
  });                                   
} 