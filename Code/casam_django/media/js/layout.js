var Check = Class.create( {
	initialize : function(type, name, checkbox, item) {
		//type: s (show) is for measurements, u (use) is for pictures, b (bitmap) is for bitmaps
	this.type = type;

	if (this.type == 's')
		this.defaultValue = true;
	else
		this.defaultValue = false;

	this.id = name;
	this.box = checkbox;
	this.oldValue = '';
	this.item = item;
	this.checked = this.defaultValue;
},
update : function(newValue) {
	this.oldValue = this.checked;
	this.checked = newValue;
},
setDefault : function() {
	this.box.defaultChecked = this.defaultValue;
},
watch : function() {
	watchBox(this);
},
repair : function() {
	if (this.checked == true)
		this.box.checked = true;
}
});

function resizeScreenElements(firsttime) {
	checkAuthenticationAndExecute( function() {
		
		var remainingWidth = document.viewport.getWidth() - 500; 
		var remainingHeight = document.viewport.getHeight() - 150; 
             
		// Always resize the big_images-container 
		$('big_images').setWidth(remainingWidth); 
		$('big_images').setHeight(remainingHeight); 

		// If the flash paintover is loaded 
		if (flashpainting) { 
			$('flash_movie_object').setWidth(remainingWidth-5); 
			$('flash_movie_object').setHeight(remainingHeight-5); 
			$('flash_movie_embed').setWidth(remainingWidth-5); 
			$('flash_movie_embed').setHeight(remainingHeight-5); 

		// If we are viewing images 
		} else {  
			//reloadImages(firsttime); 
		
			// big_images need to be resized again when the images are
			// loaded
			// the javascript continues while this.getAppropriateSizeURL()
			// is still
			// finding the correct size for the image
			resizeBigImages();
			reloadImages(firsttime);
		}
	});
}

function resizeBigImages(){
	var remainingWidth = document.viewport.getWidth() - 500;
	$('big_images').setWidth(remainingWidth);
	var remainingHeight = document.viewport.getHeight() - 150;
	$('big_images').setHeight(remainingHeight);
	
	//Resize the white frames 
	remainingHeightWhiteFrame = remainingHeight - 36;
	$('leftFrame').setHeight(remainingHeightWhiteFrame);
	$('rightFrame').setHeight(remainingHeightWhiteFrame);	
}

function newTab(tab_title, content, open, sub) {
	var tabContainer = new Element('div');
	// Attach right style-class to container
	if (sub)
		tabContainer.addClassName("subTabContainer");
	else
		tabContainer.addClassName("tabContainer");
	
	var tabHeader = new Element('div');
	var tabLine = new Element('div');

	// Construct tabBody
	if (Object.isElement(content)) {
		if(content.parentNode != null)
			content.parentNode.removeChild(content);
		tabBody = content;
	} else
		var tabBody = new Element('div', {'id':content});

	if (!open)
		tabBody.hide();



	// Attach right style-class to tab-header
	if (sub)
		tabHeader.addClassName("subTabHeader");
	else
		tabHeader.addClassName("tabHeader");
	
	tabHeader.observe('click', function() {
		Effect.toggle(tabBody, 'blind', {
			duration : 0.5
		});
		this.update();
		putArrowsInTabHeader(this, tabBody.style.display == "none")
		this.insert("<span>"+tab_title+"</span>");
	});

	putArrowsInTabHeader(tabHeader, open)
	tabHeader.insert("<span>"+tab_title+"</span>");

	// Attach right style-class to tab-line
	if (sub)
		tabLine.addClassName("subTabLine");
	else
		tabLine.addClassName("tabLine");
	
	tabLine.style.backgroundImage = "url('" + base_path
			+ "media/img/bar_middle.jpg')";
	tabLine.innerHTML = "<img src=\"" + base_path
			+ "media/img/bar_left.jpg\" style=\"float:left;\" />"
			+ "<img src=\"" + base_path
			+ "media/img/bar_right.jpg\" style=\"float:right;\" />";

	// Return the three div's
	tabContainer.insert(tabHeader);
	tabContainer.insert(tabLine);
	tabContainer.insert(tabBody);
	return tabContainer;
}

function putArrowsInTabHeader(header, open) {
	foldUpImageLeft = new Element('img');
	foldUpImageLeft.setAttribute("src", base_path + "media/img/fold_up.gif");
	foldUpImageLeft.setStyle("float:left;margin:2px;");

	foldUpImageRight = new Element('img');
	foldUpImageRight.setAttribute("src", base_path + "media/img/fold_up.gif");
	foldUpImageRight.setStyle("float:right;margin:2px;");

	foldDownImageLeft = new Element('img');
	foldDownImageLeft.setAttribute("src", base_path + "media/img/fold_down.gif");
	foldDownImageLeft.setStyle("float:left;margin:2px;");

	foldDownImageRight = new Element('img');
	foldDownImageRight.setAttribute("src", base_path	+ "media/img/fold_down.gif");
	foldDownImageRight.setStyle("float:right;margin:2px;");
	
	if (open) {
		header.insert(foldUpImageLeft);
		header.insert(foldUpImageRight);
	} else {
		header.insert(foldDownImageLeft);
		header.insert(foldDownImageRight);
	}
}

function watchBox(item) {
	item.box.observe('click', function() {
		item.update(item.box.checked);
		if (item.box.checked == true) {
			if (item.type == 's')
				item.item.place();
			else if (item.type == 'b')
				item.item.bitmap.show();
		} else {
			if (item.type == 's')
				item.item.hide();
			else if (item.type == 'b')
				item.item.bitmap.hide();
		}
	});
}

function initialisePictureTab(pictureJSON_array) {
	
	// Clear the general container
	$('tab_pictures').update();
	
	// Generate a container for the pictures
  $('tab_pictures').insert(new Element('div',{'id':'pictures'}));
  
  // Create a picture container for each picture
  for(i=0; i < pictureJSON_array.length; i++)
		makePictureContainer(pictureJSON_array[i]);
}

function makePictureContainer(pictureJSON) {
	// Overall container
	var mainDiv = new Element('div', {
		"id" : "mainDiv_" + pictureJSON.pk
	});
	mainDiv.addClassName('projectPictureDiv');
	
	// Container for picture and activation selection
	var leftDiv = new Element('div', {
		"id" : "leftDiv_" + pictureJSON.pk
	});
	leftDiv.addClassName('pictureContainerLeftDiv');
	
	// Container for title
	var rightDiv = new Element('div', {
		"id" : "rightDiv_" + pictureJSON.pk
	});
	rightDiv.addClassName('pictureContainerRightDiv');

	// Container for slider
	var sliderDiv = new Element('div', {
		"id" : "sliderDiv_" + pictureJSON.pk
	});
	sliderDiv.addClassName('pictureContainerSliderDiv');
	
	// Container for tabs
	var bottomDiv = new Element('div', {
		"id" : "bottomDiv_" + pictureJSON.pk
	});
	bottomDiv.addClassName('pictureContainerBottomDiv');

	// Create activation checkbox
	var useCheck = new Element('input', {
		'type' : 'checkbox',
		'id' : 'use' + pictureJSON.pk
	});
	useCheck.observe('click', function() {
		if (useCheck.checked == true)
			showImage(pictureJSON.pk, pictureJSON.fields.name);
		else
			hideImage(pictureJSON.pk);
	});

	leftDiv.insert(useCheck);

	// Insert image
	leftDiv.insert(new Element('img', {
		'src' : base_path + 'imageLoader/thumbnail/original/30/'
				+ pictureJSON.pk
	}));
	rightDiv.insert(new Element('span').update(pictureJSON.fields.name)
			.addClassName('projectPictureInfo'));	

	mainDiv.insert(leftDiv);
	mainDiv.insert(rightDiv);
	mainDiv.insert(sliderDiv);
	mainDiv.insert(bottomDiv);	
	$('pictures').insert(mainDiv);

	// Ugly IE fix for setting the checkboxes
	for ( var i = 0; i < addedImages.length; i++) {
		if (addedImages[i].id == pictureJSON.pk) {
			Element.writeAttribute(useCheck, 'checked', true);
			break;
		}
	}
}

function addMeasurementsToPictureContainer(imgid, json) {

	// Create overall container
	var mainDiv = new Element('div');
	mainDiv.writeAttribute('id', 'measurementsList_'+imgid);
	mainDiv.addClassName('projectPictureDiv');

	// Add all measurements
	var subtab = '';
	for (i = 0; i < json.length; i++) {

		if (json[i].model == 'casam.potentialmeasurementtype'){
			subtab = createImageMeasurementSubTab(json[i].pk, json[i].fields.name, imgid);
			mainDiv.insert(subtab);
			if ((i+1 == json.length) || (json[i+1].model == 'casam.potentialmeasurementtype'))
				subtab.hide();
		}
		else{		
			// Create measurement
			tempMeasurement = createMeasurement(
				json[i].fields.name, 
				json[i + 1].fields.x,
				json[i + 1].fields.y,
				json[i + 1].pk,
				json[i].pk,
				imgid,
				json[i + 1].fields.imagewidth,
				json[i + 1].fields.imageheight);
			
			
			subtab.childElements()[2].insert(tempMeasurement);
			i++;
		}
	}

	// Add this subtab
	var tab_measurements = newTab('Measurements', mainDiv, true, true);
	tab_measurements.id = 'measurementsDiv_'+imgid;
	tab_measurements.addClassName('imgSubTabMeasurements');
	$('bottomDiv_' + imgid).insert({ top: tab_measurements });
}

function addBitmapsToPictureContainer(imgid, bitmapJSON_array, potid) {
	
	// Check or it is already there
	if ($('bitmapsDiv_'+imgid) != null)
		return;
	
	// Create an overall container
	var mainDiv = new Element('div');
	mainDiv.writeAttribute('id','bitmapsList_'+imgid)
	mainDiv.addClassName('projectBitmapDiv');

	// Add all the bitmaps
	for ( var i = 0; i < bitmapJSON_array.length; i++)
		mainDiv.insert(addBitmap(bitmapJSON_array[i].pk, imgid, potid));
	
	// Add this subtab
	var tab_bitmaps = newTab('Bitmaps', mainDiv, true, true);
	tab_bitmaps.id = 'bitmapsDiv_'+imgid;
	tab_bitmaps.addClassName('imgSubTabBitmaps');
	$('bottomDiv_' + imgid).insert({ bottom: tab_bitmaps });
}

function closePopupAndReloadPictures() {
	getProjectImages(false);
	new Effect.Highlight('pictures');
	//$('tab_pictures').scrollTo($('addPictureButton'));
	closePopup();
}

function closePopupAndReloadTags() {
	getProjectTags();
	new Effect.Highlight('tags');
	closePopup();
}

function closePopupAndReloadPotentialMeasurements(meas) {
	if (meas == '')
		closePopup();
	else {
		measObject = meas.evalJSON()[0];
		createPotentialMeasurement(measObject.pk, measObject.fields.type, measObject.fields.name, measObject.fields.soort);
		new Effect.Highlight('potmeas_' + measObject.pk);
		popupIFrame(base_path+'pm/new/'+projectID,350,150);
	}
}


function closePopupAndReloadPotentialMeasurementTypes(pottype){
	if (pottype == '')
		closePopup();
	else{
		typeObject = pottype.evalJSON()[0];
		createPotentialMeasurementType(typeObject.pk, typeObject.fields.name);
		closePopup();
	}
}

function loadEditScreen(id, pm_id, bmid) {
	checkAuthenticationAndExecute( function() {

		flashpainting = true;
		
		// Are we editing an existing bitmap?
		img_url = base_path + 'imageLoader/original/' + id;
		if ((bmid != '') && (bmid != undefined))
		  bitmap_url = base_path + 'imageLoader/bitmap/'+bmid+'?time='+new Date().getTime();
	  else
	    bitmap_url = '';
		mov_width = ($('big_images').getWidth() - 5);
		mov_heigth = ($('big_images').getHeight() - 5);

		// Create the html-objects
		movie_object = new Element('object');
		movie_object.writeAttribute('id', 'flash_movie_object'); 
		movie_object.writeAttribute('classid',
				"clsid:d27cdb6e-ae6d-11cf-96b8-444553540000");
		movie_object
				.writeAttribute(
						'codebase',
						"http://fpdownload.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=8,0,0,0");
		movie_object.writeAttribute('width', mov_width);
		movie_object.writeAttribute('height', mov_heigth);

		movie_embed = new Element('embed');
		movie_embed.writeAttribute('id', 'flash_movie_embed'); 
		movie_embed.writeAttribute('src', base_path + 'media/flash/paint.swf');
		movie_embed.writeAttribute('quality', "high");
		movie_embed.writeAttribute('bgcolor', "#000000");
		movie_embed.writeAttribute('width', mov_width);
		movie_embed.writeAttribute('height', mov_heigth);
		movie_embed.writeAttribute('allowScriptAccess', "sameDomain");
		movie_embed.writeAttribute('type', "application/x-shockwave-flash");
		movie_embed.writeAttribute('pluginspage',
				"http://www.macromedia.com/go/getflashplayer");
		movie_embed.writeAttribute('flashvars', "img_source=" + img_url
				+ "&server_url=" + base_path + "bitmap_dump&img_id=" + id
				+ "&img_bitmap=" + bitmap_url + "&img_previous_id=" + bmid+"&img_pm_id="+pm_id);

		movie_object.insert(movie_embed);
		$('big_images').update();
		$('big_images').insert(movie_object);
	});
}

function closePaintOver(bmid, potid) {
	if(bmid != '' && $('bitmapDiv_'+bmid) == undefined) {
		newBitmapDiv = addBitmap(bmid, addedImages[0].id, potid);
		$('bitmapsList_'+addedImages[0].id).insert(newBitmapDiv);
	}
	
	flashpainting = false; 
	reloadImages(false); 
} 


