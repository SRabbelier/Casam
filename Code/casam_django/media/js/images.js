var AddedImage = Class.create( {
	initialize : function(id, name) {
		this.id = id;
		this.name = name;
		this.opacity = 0.5;
		this.imageElement = new Element('img');
		this.imageElement.writeAttribute('src', this.getAppropriateSizeURL());
		this.imageElement.writeAttribute('id', 'addedImage_' + id);
		this.imageElement.addClassName('big_image_sibling');
		this.imageElement.setOpacity(this.opacity);

		this.opacitySliderContainer = new Element('div');
		// HARDCODE THIS WIDTH FOR THE SLIDER TO WORK INITIALLY
		this.opacitySliderContainer.setWidth(170);
		this.opacitySliderContainer.writeAttribute('id',
				'opacitySliderContainer_' + this.id);
		this.opacitySliderContainer.addClassName('slider');

		this.opacitySliderHandle = new Element('div');
		this.opacitySliderHandle.writeAttribute('id',
				'opacitySliderHandle_' + this.id);
		this.opacitySliderHandle.addClassName('handle');

		this.opacitySliderContainer.insert(this.opacitySliderHandle);

	},
	getAppropriateSizeURL : function() {
		return (base_path + 'imageLoader/byMaxWidthHeight/original/'
				+ ($('big_images').getWidth() - 2) + '/'
				+ ($('big_images').getHeight() - 2) + '/' + this.id);
	},
	setOpacityForImage : function(opacityValue) {
		this.opacity = opacityValue;
		this.imageElement.setOpacity(this.opacity);
	},
	makeNonActive: function(){
		$('mainDiv_' + this.id).setStyle({border: 'none',
																			backgroundColor: ''});
		for(var i = 0; i < measurements.length; i++){
			if(measurements[i].imageid == this.id)
				measurements[i].nonActive();			
		}
		
		$('zoomImage').setAttribute('src', '');
		$('zoomImage').hide();
	},
	makeActive: function(){
		$('mainDiv_' + this.id).setStyle({border: '1px red dashed',
																			backgroundColor: 'red'});
		//zoom image
		$('zoomImage').writeAttribute('src',base_path + 'imageLoader/byRatio/original/150/' + this.id);
		$('zoomImage').show();
																							
		for(var i = 0; i < measurements.length; i++){
			if(measurements[i].imageid == this.id)
				measurements[i].setActive();			
		}
	},	
	addSelfToBigImages : function() {
		
		//we need this for the observer and the slider
		parentAddedImageObject = this;
		//because of slow servers we need to empty the src
		this.imageElement.writeAttribute('src', '');
		this.imageElement.writeAttribute('src', this.getAppropriateSizeURL());
		this.imageElement.observe('load', function() {
			//resize the measurements
			resizeMeasurements(this.id);
			resizeBigImages();
		});
			
		this.imageElement.observe('click', function() {
			LoadMMDD('', parentAddedImageObject.id);
		});

		$('big_images').insert( { bottom : this.imageElement	});
		
		//create a slider
		addSlider($('bottomDiv' + this.id),this);
	},
	addMetaDataToSelf : function() {
		getImageMeasurements(this.id);
		getImageBitmaps(this.id);
	},
	addSelfToImages : function() {
		$('big_images').insert(this.imageElement);
		this.addSelfToBigImages();
		this.addMetaDataToSelf();
	}
});

function deleteImage(id) {

	$('mainDiv_' + id).remove();

	removeImage(id);

	//delete active image for this image
	checkActiveLayer();
}

function addImage(originalImage) {
	var container = makePictureContainer(originalImage.evalJSON()[0]);
}

function showImage(id, name) {
	checkAuthenticationAndExecute( function() {

		var newAddedImage = new AddedImage(id, name);
		addedImages.splice(0, 0, newAddedImage);
		newAddedImage.addSelfToImages();
		
		checkActiveLayer();
	});
}

function hideImage(id) {
	checkAuthenticationAndExecute( function() {

		if (addedImages[0].id == id)
			addedImages[0].makeNonActive();
		
		//remove bitmaps
		removeBitmaps(id);
		
		//remove measurements
		removeMeasurements(id);
		
		//remove checkboxes
		removeCheckboxes(id);
		
		//remove changes
		removeChanges(id);
		
		//remove image
		removeImage(id);
		
		//check for new active layer
		checkActiveLayer();
	});
}

function reloadImages(full) {
	checkAuthenticationAndExecute( function() {

		//.update() clears the contents of the elements
		$('big_images').update();

		for ( var i = addedImages.length - 1; i >= 0; i--) {
			$('mainDiv_' + addedImages[i].id).setStyle('border: none;');
			if ( i >= 1)
				addedImages[i].makeNonActive();
			if (full) {
				$('bottomDiv' + addedImages[i].id).update();
				addedImages[i].addSelfToImages();
			} else
				addedImages[i].addSelfToBigImages();
		}

		if (addedImages.length > 0) {
			$('mainDiv_' + addedImages[0].id).setStyle(
					'border: 1px dashed red;');
			addedImages[0].makeActive();
		}
		makePicturesSortable();
		reloadBitmaps();
	});
}

function updateImageList() {
	checkAuthenticationAndExecute( function() {
		id_array = Sortable.sequence("pictures");
		new_list = new Array();
		for ( var i = 0; i < id_array.length; i++) {
			for ( var j = 0; j < addedImages.length; j++) {
				if (id_array[i] == addedImages[j].id) {
					new_list.push(addedImages[j]);
					break;
				}
			}
		}
		addedImages = new_list;
		
		//reloadImages(false);
		checkActiveLayer();

	});
}

function removeMeasurements(imageID){
	for ( var i = 0; i < measurements.length; i++) {
		if (measurements[i].imageid == imageID) {
			if (measurements[i].imageid == addedImages[0].id) {
				measurements[i].restore();
			}
			measurements[i].pinDiv.remove();
			measurements.splice(i, 1);
			i = i - 1;
		}
	}
}
function resizeMeasurements(imageID){
	for(var i = 0; i < checkboxes.length; i++) {
		if ((checkboxes[i].item.imageid == imageID) && (checkboxes[i].box.checked == true) &&
		    (checkboxes[i].type == 's')){
			  	checkboxes[i].item.replace();
		}
	}
}




function removeCheckboxes(imageID){
	for(var i = 0; i < checkboxes.length; i++){
		if(checkboxes[i].item.imageid == imageID){
			checkboxes.splice(i,1);
			i = i - 1;
		}
	}
}

function removeChanges(imageID){
	for ( var i = 0; i < changes.length; i++) {
		if (changes[i].imageid == imageID) {
			changes[i].changeDiv.remove();
			changes.splice(i, 1);
			i = i - 1;
		}
	}
}

function removeImage(imageID){
	for ( var i = 0; i < addedImages.length; i++){
		if (addedImages[i].id == imageID){
			addedImages.splice(i, 1);
			break;
		}
	}
	Element.remove($('addedImage_'+imageID))
	
	$('bottomDiv' + imageID).update();
}

function checkActiveLayer(){
	//$('zoomImage').hide();
	if (addedImages.length > 0) {
		addedImages.each(function(item){
			item.makeNonActive();
		});
		addedImages[0].makeActive();
		
		//set sequence so that active layer is always on top
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
	}
	else{
		$('zoomImage').hide();
	}
}

function addSlider(div,object){
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