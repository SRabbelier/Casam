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

function getProjectImages(afterFinishFunction)
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
        
        if(afterFinishFunction)
          afterFinishFunction();
			}
		});
	});
}


function getImageBitmaps(imgid) {
	var url = base_path + 'JSON/projectImageBitmaps/' + imgid 
			+ '?time=' + new Date().getTime();
	new Ajax.Request(url,	{
			asynchronous:	false,
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
				addMeasuermentsToPictureContainer(imgid, json);
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
        	createPotentialMeasurement(json[i].pk, json[i].fields.type, json[i].fields.name)
      	}
      }
    }
  });
  });
}
