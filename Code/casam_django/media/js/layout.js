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
		// big_images need to be resized again when the images are
		// loaded
		// the javascript continues while this.getAppropriateSizeURL()
		// is still
		// finding the correct size for the image
		resizeBigImages();
		reloadImages(firsttime);
	});
}

function resizeBigImages(){
	var remainingWidth = document.viewport.getWidth() - 500;
	$('big_images').setWidth(remainingWidth);
	var remainingHeight = document.viewport.getHeight() - 150;
	$('big_images').setHeight(remainingHeight);
	remainingHeightWhiteFrame = remainingHeight - 36;
	$('leftFrame').setHeight(remainingHeightWhiteFrame);
	$('rightFrame').setHeight(remainingHeightWhiteFrame);	
}

function newTab(tab_title, content, open) {
	var tabContainer = new Element('div');
	var tabHeader = new Element('div');
	var tabLine = new Element('div');
	if (Object.isElement(content)) {
		if(content.parentNode != null)
			content.parentNode.removeChild(content);
		tabBody = content;
	} else {
		var tabBody = new Element('div', {'id':content});
	}
	if (!open)
		tabBody.hide();

	foldUpImageLeft = new Element('img');
	foldUpImageLeft.setAttribute("src", base_path + "media/img/fold_up.gif");
	foldUpImageLeft.setStyle("float:left;margin:2px;");

	foldUpImageRight = new Element('img');
	foldUpImageRight.setAttribute("src", base_path + "media/img/fold_up.gif");
	foldUpImageRight.setStyle("float:right;margin:2px;");

	foldDownImageLeft = new Element('img');
	foldDownImageLeft
			.setAttribute("src", base_path + "media/img/fold_down.gif");
	foldDownImageLeft.setStyle("float:left;margin:2px;");

	foldDownImageRight = new Element('img');
	foldDownImageRight.setAttribute("src", base_path
			+ "media/img/fold_down.gif");
	foldDownImageRight.setStyle("float:right;margin:2px;");

	tabHeader.style.backgroundColor = "#dddddd";
	tabHeader.style.cursor = "pointer";
	tabHeader.observe('click', function() {
		Effect.toggle(tabBody, 'blind', {
			duration : 0.5
		});
		this.update();
		if (tabBody.style.display == "none") {
			this.insert(foldUpImageLeft);
			this.insert(foldUpImageRight);
		} else {
			this.insert(foldDownImageLeft);
			this.insert(foldDownImageRight);
		}
		this.innerHTML += "<b>" + tab_title + "</b>";
	});

	if (open) {
		tabHeader.insert(foldUpImageLeft);
		tabHeader.insert(foldUpImageRight);
	} else {
		tabHeader.insert(foldDownImageLeft);
		tabHeader.insert(foldDownImageRight);
	}
	tabHeader.innerHTML += "<b>" + tab_title + "</b>";

	tabLine.style.height = "2px";
	tabLine.style.backgroundImage = "url('" + base_path
			+ "media/img/bar_middle.jpg')";
	tabLine.style.backgroundRepeat = "repeat-x";
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
  
	// Put below it a bar with tools
	var toolbar = new Element('div');
	toolbar.setStyle("clear:both;float:right;");
	var addLink = new Element('a',{'href':'#'});
	var addImage = new Element('img',{'src':base_path+'media/img/pencil.jpg','id':'addPictureButton','class':'smallPictureButton'});
	addLink.insert(addImage);
	toolbar.insert(addLink);
	Event.observe(addLink,'click',function(){
		popupIFrame(base_path+'project/imageManager/'+projectID,670,400);
	});
	$('tab_pictures').insert(toolbar);
	
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
		'src' : base_path + 'imageLoader/thumbnail/original/50/'
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

function addMeasuermentsToPictureContainer(imgid, measurementJSON_array) {
	
	// Create overall container
	var mainDiv = new Element('div');
	mainDiv.writeAttribute('id', 'measurementsList_'+imgid);
	mainDiv.addClassName('projectPictureDiv');

	// Add all measurements
	for (i = 0; i < measurementJSON_array.length - 1; i = i + 2) {
		
		// Create measurement
		tempMeasurement = createMeasurement(
				measurementJSON_array[i].fields.name, 
				measurementJSON_array[i + 1].fields.x,
				measurementJSON_array[i + 1].fields.y,
				measurementJSON_array[i + 1].pk,
				measurementJSON_array[i].pk,
				imgid,
				measurementJSON_array[i + 1].fields.imagewidth,
				measurementJSON_array[i + 1].fields.imageheight);
		
		mainDiv.insert(tempMeasurement);
	}
	
	// Add this subtab
	var tab_measurements = newTab('Measurements', mainDiv, true);
	tab_measurements.id = 'measurementsDiv_'+imgid;
	tab_measurements.addClassName('imgSubTabMeasurements');
	$('bottomDiv_' + imgid).insert(tab_measurements);	
}

function addBitmapsToPictureContainer(imgid, bitmapJSON_array) {
	
	// Check or it is already there
	if ($('bitmapsDiv_'+imgid) != null)
		return;
	
	// Create an overall container
	var mainDiv = new Element('div');
	mainDiv.writeAttribute('id','bitmapsList_'+imgid)
	mainDiv.addClassName('projectBitmapDiv');
	
	// Create temporary link to paintover
	var paintoverLink = new Element('a', {
		'href' : 'javascript:loadEditScreen(\''+imgid+'\')'
	}).update('Paintover');
	mainDiv.insert(paintoverLink);

	// Add all the bitmaps
	for ( var i = 0; i < bitmapJSON_array.length; i++)
		mainDiv.insert(addBitmap(bitmapJSON_array[i].pk, imgid));
	
	// Add this subtab
	var tab_bitmaps = newTab('Bitmaps', mainDiv, true);
	tab_bitmaps.id = 'bitmapsDiv_'+imgid;
	tab_bitmaps.addClassName('imgSubTabBitmaps');
	$('bottomDiv_' + imgid).insert(tab_bitmaps);
}

function closePopupAndReloadPictures() {
	getProjectImages();
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
		createPotentialMeasurement(measObject.pk, measObject.fields.type, measObject.fields.name);
		new Effect.Highlight('potmeas_' + measObject.pk);
		closePopup();
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

function loadEditScreen(id, bmid) {
	checkAuthenticationAndExecute( function() {

		flashpainting = true;
		
		// Are we editing an existing bitmap?
		img_url = base_path + 'imageLoader/original/' + id;
		if ((bmid != '') && (bmid != undefined))
		  bitmap_url = base_path + 'imageLoader/bitmap/'+bmid;
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
				+ "&img_bitmap=" + bitmap_url + "&img_previous_id=" + bmid);

		movie_object.insert(movie_embed);
		$('big_images').update();
		$('big_images').insert(movie_object);
	});
}

function closePaintOver(bmid) {
	if(bmid != '') {
		newBitmapDiv = addBitmap(bmid, addedImages[0].id);
		$('bitmapsList_'+addedImages[0].id).insert(newBitmapDiv);
	}
	
	flashpainting = false; 
	reloadImages(false); 
} 
