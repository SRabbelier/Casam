var AddedImage = Class.create( {
	initialize : function(id, name, className) {
		this.id = id;
		this.name = name;
		this.opacity = 1;
		this.className = className; 
		this.imageElement = new Element('img');

		// Create the image opacity slider
		this.opacitySliderContainer = new Element('div');
		this.opacitySliderContainer.setHeight(3);
		// Hardcode this width for the slider to work initially
		this.opacitySliderContainer.setWidth(100);
		this.opacitySliderContainer.writeAttribute('id',
				'opacitySliderContainer_' + this.id);
		this.opacitySliderContainer.addClassName('slider');

		this.opacitySliderHandle = new Element('div');
		this.opacitySliderHandle.setHeight(9);
		this.opacitySliderHandle.setWidth(3);
		this.opacitySliderHandle.writeAttribute('id',
				'opacitySliderHandle_' + this.id);
		this.opacitySliderHandle.addClassName('handle');

		this.opacitySliderContainer.insert(this.opacitySliderHandle);

	},
	getAppropriateSizeURL : function() {
		// className needed to distinguish between images and PMD-overlays
		if(!this.className){
			return (base_path + 'imageLoader/byMaxWidthHeight/original/'
				+ ($('big_images').getWidth() - 2) + '/'
				+ ($('big_images').getHeight() - 2) + '/' + this.id);
		}else if(this.className == "casam.pdm"){
			return (base_path + 'imageLoader/byMaxWidthHeight/overlay/'
					+ ($('big_images').getWidth() - 2) + '/'
					+ ($('big_images').getHeight() - 2) + '/' + this.id);
		}
	},
	setOpacityForImage : function(opacityValue) {
		this.opacity = opacityValue;
		this.imageElement.setOpacity(this.opacity);
	},
	makeNonActive: function(activeImage){
		// Restore this layer to not be the active layer
		$('mainDiv_' + this.id).setStyle({border: 'none',
																			backgroundColor: ''});
		
		// Make measurements inactive (blue and fire LoadMMDD on click)
		for(var i = 0; i < measurements.length; i++){
			if(measurements[i].imageid == this.id) {
				
				// Make green and non-draggable
				measurements[i].nonActive();			
				
				// Redirect a click
				measurements[i].pinDiv.observe('click', function(e) {
					hideLandmarkTooltip(e);
					LoadMMDD('', addedImages[0].id);
				});
			}
		}
		
		// Hide the zoom image
		$('zoomImage').setAttribute('src', '');
		$('zoomImage').hide();
	},
	makeActive: function(){
		// Make this layer the acitve layer
		$('mainDiv_' + this.id).setStyle({border: '1px red dashed',
																			backgroundColor: '#ffdddd'});

		// Set the new zoom image
		$('zoomImage').writeAttribute('src', base_path + 'imageLoader/byRatio/original/150/' + this.id);
		$('zoomImage').show();

		// If the imageElement was already added to the page, remove it first
		if(this.imageElement.parentNode){
			this.imageElement.remove();
		}
		// Add the imageElement to big_images
		$('big_images').insert( { bottom : this.imageElement	});

		// Restore potential measurement pins
		var mm_array = $$('img.mmPointer')
		for(var i = 0; i < mm_array.length; i++){
			mm_array[i].show();
		}

		// Make the measurements of the new active layer active
		for(var i = 0; i < measurements.length; i++){
			if(measurements[i].imageid == this.id) {
				
				measurements[i].pinDiv.stopObserving('click');
				
				measurements[i].setActive();							
			}
		}
		
		// Disable editing of existing bitmaps
		for(var i = 0; i < bitmaps.length; i++){
			if(bitmaps[i].imageid == this.id) {
				$('mm' + bitmaps[i].potid).hide();
			}
		}
	},
	addSelfToImages: function(full) {
		
		// Stop observing the imageElement, so that no event is fired on unload of src
		this.imageElement.stopObserving();
		// Create a new imageElement
		this.imageElement = new Element('img');
		this.imageElement.writeAttribute('id', 'addedImage_' + this.id);
		this.imageElement.addClassName('big_image_sibling');
		this.imageElement.setOpacity(this.opacity);
		
		this.imageElement.writeAttribute('src', this.getAppropriateSizeURL());
		makeImageObservers(this, full);
		
		$('big_images').insert( { bottom : this.imageElement	});
		
		// Create a slider
		$('sliderDiv_' + this.id).update();
		addSlider($('sliderDiv_' + this.id),this);
	}
});

// Do this when the image is fully loaded
function makeImageObservers(image, full){
	image.imageElement.observe('load', function() {
	
		// If needed, first get the image measurements and bitmaps, before the measurements can be resized
		if (full){
			getImageMeasurements(image.id);
			getImageBitmaps(image.id);
		}
		resizeMeasurements(image.id);
		
	});
		
	image.imageElement.observe('click', function() {
		LoadMMDD('', image.id);
	});	
	
}

function deleteImage(id) {
	$('mainDiv_' + id).remove();

	// Detele the image, and all corresponding stuff
	removeImage(id);

	// Check for the new active layer
	checkActiveLayer();
}

function addImage(originalImage) {
	var container = makePictureContainer(originalImage.evalJSON()[0]);
	makePicturesSortable();
}

function showImage(id, name, className) {
	// Function is called when the checkbox in front of an image is turned on
	checkAuthenticationAndExecute( function() {
		// Create a new Image object
		var newAddedImage = new AddedImage(id, name, className);
		$('big_images').insert(this.imageElement);
		// Add this new image to the fron of the array
		addedImages.splice(0, 0, newAddedImage);
		// Let it add itself
		newAddedImage.addSelfToImages(true);
		
		// Set the new active layer accordingly
		checkActiveLayer();
	});
}

function hideImage(id) {
	// Function is called when the checkbox in front of an image is turned off
	if (addedImages.length > 0){
		if (addedImages[0].id == id)
			addedImages[0].makeNonActive();
	}

	// Remove checkboxes
	removeCheckboxes(id);		

	//remove bitmaps
	removeBitmaps(id);

	// Remove measurements
	removeMeasurements(id);

	// Remove changes
	removeChanges(id);

	// Remove image
	removeImage(id);

	// Check for new active layer
	checkActiveLayer();
}

function reloadImages(full) {
	checkAuthenticationAndExecute( function() {

		// Clear the contents of big_images
		$('big_images').update();

		// Let every image add itself again, and mark only the first image as the active layer
		for ( var i = 0; i < addedImages.length; i++) {
			if ( i >= 1)
				addedImages[i].makeNonActive();
			addedImages[i].addSelfToImages(full);
		}

		if (addedImages.length > 0) {
			addedImages[0].makeActive();
		}
		
		// Make the pictures sortable again
		makePicturesSortable();
		
		// Also reload the bitmaps, since big_images was cleared
		reloadBitmaps();
	});
}

function updateImageList() {
	// Function is called on change of the sortable
	checkAuthenticationAndExecute( function() {
		// Get the new sequence as it is on screen
		id_array = Sortable.sequence("pictures");
		new_list = new Array();
		// Set this sequence in a new array
		for ( var i = 0; i < id_array.length; i++) {
			for ( var j = 0; j < addedImages.length; j++) {
				if (id_array[i] == addedImages[j].id) {
					new_list.push(addedImages[j]);
					break;
				}
			}
		}
		// Copy this array to 'addedImages'
		addedImages = new_list;
		
		// Check to see what the active layer is now
		checkActiveLayer();

	});
}

function removeImage(imageID){
	// Remove the image from 'addedImages'
	for ( var i = 0; i < addedImages.length; i++){
		if (addedImages[i].id == imageID){
			// Remove the image itself
			Element.remove($('addedImage_'+imageID))
			// Remove the images slider
			$('sliderDiv_' + imageID).update();
			// If the image is a real image, and not a PDM-Overlay, clear all measurement and bitmap information
			if ($('rightDiv_' + imageID).childElements()[0].innerHTML != "PDM-Overlay"){
				$('bottomDiv_' + imageID).update();
			}
			addedImages.splice(i, 1);
			break;
		}
	}
}

function checkActiveLayer(){
	// When there are images showing
	if (addedImages.length > 0) {
		// Make each image 'nonActive'
		addedImages.each(function(item){
			item.makeNonActive();
		});
		// Make the first image Active
		addedImages[0].makeActive();
		
		// Set sequence so that active layer is always on top
		id_array = Sortable.sequence("pictures");
		var temp = "";
		for ( var i = 0; i < id_array.length; i++) {
			if (id_array[i] == addedImages[0].id) {
				temp = id_array[i];
				id_array.splice(i, 1);
				break;
			}
		}
		id_array.splice(0, 0, temp);
		Sortable.setSequence("pictures", id_array);
		
		// Set the bitmaps to the end of the big_images, to ensure correct transparency
		var big_bitmaps = $('big_images').select('img.big_image_sibling_bitmap');
		for(var i = 0; i < big_bitmaps.length; i++){
			big_bitmaps[i].remove();
			$('big_images').insert({ bottom: big_bitmaps[i]});
		}
	}
	// When there are no images showing
	else{
		$('zoomImage').hide();
	}
	
}

function addSlider(div, object){
	div.update();
	div.insert( { top : object.opacitySliderContainer });
	new Control.Slider(
		object.opacitySliderHandle,
		object.opacitySliderContainer, 
		{ minimum : 0,
			maximum : 1,
			sliderValue : object.opacity,
			onSlide : function(value) {
				object.setOpacityForImage(value);
			}}
	);
}

function makePicturesSortable(){
	Sortable.create("pictures", {
		tag : 'div',
		only : 'projectPictureDiv',
		onUpdate : updateImageList
	});
}
