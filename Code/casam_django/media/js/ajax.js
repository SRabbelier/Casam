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
				
		// Notice the use of a proxy to circumvent the Same Origin Policy
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
				
		// Notice the use of a proxy to circumvent the Same Origin Policy
		var url = base_path+'JSON/projectOverlays/'+projectID+'?time='+new Date().getTime();
		new Ajax.Request(url, {
		  method: 'get',
		  onSuccess: function(transport, json) {
		  	// Grab the picture-array
		    var json = transport.responseText.evalJSON();

		    // Build the content of the tab
		    addOverlayTab(json);
		    

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
				var json = transport.responseText.evalJSON();
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
		
				var json = transport.responseText.evalJSON();
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
			  
		    var json = transport.responseText.evalJSON();
		    			     
		    $('tags').update();
		     
		    // Create a picture container for each picture
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

      var json = transport.responseText.evalJSON();

      $('possiblemeasurements').update();
      // Create a picture container for each picture
      for(i=0; i < json.length; i++){
      	if (json[i].model == 'casam.potentialmeasurementtype'){
      		createPotentialMeasurementType(json[i].pk, json[i].fields.name);
      	}
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
      //containerDiv.remove();
      //DELETE POTENTIAL MEASUREMENTS
      var parentPotentialMeasurements = $$('div.potMeasDiv');
      for(var i = 0; i < parentPotentialMeasurements.length; i++){
        if (parentPotentialMeasurements[i].id.slice(8) == potid){
          Effect.Fade(parentPotentialMeasurements[i]);
          parentPotentialMeasurements[i].remove();
        }                  
      }
      //DELETE CURRENT MEASUREMENTS
      for(var j = 0; j < measurements.length; j++){
        if (measurements[j].potid == potid){
          // HIDE THE POTENTIAL TYPE IF THE CURRENT LANDMARK IS THE ONLY LANDMARK OF THAT TYPE
          if ($('measidMeasDiv_'+measurements[j].id).up().childElements().length == 1)
            $('measidMeasDiv_'+measurements[j].id).up().up().hide();
          // REMOVE TEXT OF CURRENT MEASUREMENTS
          $('measidMeasDiv_'+measurements[j].id).remove();
          // REMOVE CURRENT MEASUREMENT FROM ARRAY
          measurements[j].erase();
          measurements.splice(j,1);
          j = j - 1;
        }                                             
      }
      //SINCE DELETION CANNOT BE UNDONE, DELETE CHANGES
      for(var i = 0; i < changes.length; i++){
        if (changes[i].potid == potid){
          changes[i].erase();
          changes.splice(i,1);
          i = i - 1;
        }
      }
      // REMOVE POTENTIAL MEASUREMENT FROM OPTION LIST
      $('option'+potid).remove();
    },
    onFailure:function(){
      alert('Something went wrong while deleting potential measurement '+containerDiv.childElements()[0].innerHTML);
    }
  });
}

function removePotentialType(typeid){
  var url = base_path + 'AJaX/deletePotentialMeasurementType/?time='+new Date().getTime();
  new Ajax.Request(url, {
      method: 'get',
      parameters: {'potTypeID': typeid},
      onSuccess: function(transport, json) {
        //DELETE CURRENT MEASUREMENTS
        for(var j = 0; j < measurements.length; j++){
          if ($('potmeas_'+measurements[j].potid).up().id.slice(9) == typeid){
            measurements.splice(j,1);
            j = j - 1;
          }                                             
        }
        //REMOVE TEXT OF CURRENT MEASUREMENTS
        for(var i = 0; i < addedImages.length; i++){
          $('measurementTypesDiv_'+addedImages[i].id+'-'+typeid).remove();                                          
        }
        //SINCE DELETION CANNOT BE UNDONE, DELETE CHANGES
        for(var i = 0; i < changes.length; i++){
          if ($('potmeas_'+changes[i].potid).up().id.slice(9) == typeid){
            changes[i].changeDiv.remove();
            changes.splice(i,1);
            i = i - 1;
          }
        }
        //DELETE POTENTIAL MEASUREMENTS
        var parentPotentialMeasurements = $$('div.potMeasDiv');
        var bitmapIDs = new Array();
        for(var i = 0; i < parentPotentialMeasurements.length; i++){
          if (parentPotentialMeasurements[i].up().id.slice(9) == typeid){
            Effect.Fade(parentPotentialMeasurements[i]);
        		// REMOVE CURRENT BITMAPS
            var parentCurrentBitmaps = $$('div.projectImageBitmapDivPotId_'+parentPotentialMeasurements[i].id.slice(8))
            for(var i = 0; i < parentCurrentBitmaps.length; i++){
      				var bmid = parentCurrentBitmaps[i].id.slice(10)
      				bitmapIDs.push(bmid);
      				//DELETE BITMAP FROM BIG_IMAGES
      				$('bitmap_'+bmid).remove();
      				parentCurrentBitmaps[i].remove();
      			} 
            if (!parentPotentialMeasurements[i].childElements()[0].hasClassName('paintoverLink'))
            	$('option'+parentPotentialMeasurements[i].id.slice(8)).remove();
            parentPotentialMeasurements[i].remove();
          }                  
        }
        // DELETE BITMAPS FROM BITMAP ARRAY
        for(var i = 0; i < bitmapIDs.length; i++){
        	for(var j = 0; j < bitmaps.length; j++){
        		if (bitmaps[j].id == bitmapIDs[i])
        		  bitmaps.splice(j, 1);
        		  break;
        	}
        }
        //DELETE POTENTIAL MEASUREMENTS GROUP
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