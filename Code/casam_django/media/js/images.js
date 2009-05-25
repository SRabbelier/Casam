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
	getImageElement : function() {
		return this.imageElement;
	},
	getOpacitySliderContainer : function() {
		return this.opacitySliderContainer;
	},
	setOpacityForImage : function(opacityValue) {
		this.opacity = opacityValue;
		this.imageElement.setOpacity(this.opacity);
	},
	makeNonActive: function(){
		for(var i = 0; i < measurements.length; i++){
			if(measurements[i].imageid == this.id)
				measurements[i].nonActive();			
		}
	},
	makeActive: function(){
		for(var i = 0; i < measurements.length; i++){
			if(measurements[i].imageid == this.id)
				measurements[i].setActive();			
		}
	},	
	addSelfToBigImages : function() {
		var parentAddedImageObject = this;
		this.imageElement.writeAttribute('src', '');
		this.imageElement.writeAttribute('src', this.getAppropriateSizeURL());
		this.imageElement.observe('load', function() {
			//resize the measurements
				checkboxes.each(function(item) {
					if ((item.item.imageid == parentAddedImageObject.id) && (item.box.checked == true) &&
					    (item.type == 's')){
						  	$('big_images').insert(item.item.pinDiv);
						  	item.item.replace();
					}
				});
				// big_images need to be resized again when the images are
				// loaded
				// the javascript continues while this.getAppropriateSizeURL()
				// is still
				// finding the correct size for the image
				var remainingWidth = document.viewport.getWidth() - 500;
				$('big_images').setWidth(remainingWidth);
				var remainingHeight = document.viewport.getHeight() - 150;
				$('big_images').setHeight(remainingHeight);
			});
		$('big_images').insert( {
			'bottom' : this.getImageElement()
		});
		this.getImageElement().observe('click', function() {
			LoadMMDD('', parentAddedImageObject.id);
		});

		$('bottomDiv' + parentAddedImageObject.id).insert( {
			top : this.getOpacitySliderContainer()
		});
		new Control.Slider(this.opacitySliderHandle,
				this.opacitySliderContainer, {
					minimum : 0,
					maximum : 1,
					sliderValue : parentAddedImageObject.opacity,
					onSlide : function(value) {
						parentAddedImageObject.setOpacityForImage(value);
					}
				});
	},
	addMetaDataToSelf : function() {
		getImageMeasurements(this.id);
		getImageBitmaps(this.id);
	},
	addSelfToImages : function() {
		this.addSelfToBigImages();
		this.addMetaDataToSelf();
	}
});


function addImage(originalImage) {
	var container = makePictureContainer(originalImage.evalJSON()[0]);
}


function removeImage(id) {

	$('mainDiv_' + id).remove();

	// delete measurements for this image
	for ( var i = 0; i < measurements.length; i++) {
		if (measurements[i].imageid == id) {
			if (measurements[i].imageid == addedImages[0].id) {
				measurements[i].restore();
			}
			measurements[i].pinDiv.remove();
			measurements.splice(i, 1);
			i = i - 1;
		}
	}

	//delete changes for this image
	for ( var i = 0; i < changes.length; i++) {
		if (changes[i].imageid == id) {
			changes[i].changeDiv.remove();
			changes.splice(i, 1);
			i = i - 1;
		}
	}

	//remove bitmaps            
	for ( var i = 0; i < bitmaps.length; i++) {
		if (bitmaps[i].imageid == id) {
			$('bitmap_' + bitmaps[i].id).remove();
			bitmaps.splice(i, 1);
			i = i - 1;
		}
	}

	//delete active image for this image
	for ( var i = 0; i < addedImages.length; i++) {
		if (addedImages[i].id == id) {
			$('addedImage_' + addedImages[i].id).remove();
			$('zoomImage').hide();
			addedImages.splice(i, 1);
			// set new picture as active layer
			if (addedImages.length > 0) {
				$('mainDiv_' + addedImages[0].id).setStyle(
						'border: 1px dashed red;');
				// set measurements of active layer to active
				for ( var j = 0; j < measurements.length; j++) {
					if (measurements[j].imageid == addedImages[0].id)
						measurements[j].setActive();
				}
			}
			break;
		}
	}
}



function showImage(id, name) {
	checkAuthenticationAndExecute( function() {

		var newAddedImage = new AddedImage(id, name);
		var newImageArray = new Array();
		// Delete the old image and put it up front
		for (i = 0; i < addedImages.length; i++) {
			if (addedImages[i].id != id) {
				newImageArray.push(addedImages[i]);
			}
		}
		addedImages = newImageArray
		addedImages.splice(0, 0, newAddedImage);

		id_array = Sortable.sequence("pictures");
		var temp = "";
		for ( var i = 0; i < id_array.length; i++) {
			if (id_array[i] == id) {
				temp = id_array[i];
				id_array.splice(i, 1);
				break;
			}
		}
		id_array.splice(0, 0, temp);
		Sortable.setSequence("pictures", id_array);
		newAddedImage.addSelfToImages();
		for ( var i = 1; i < addedImages.length; i++) {
			$('mainDiv_' + addedImages[i].id).setStyle('border: none;');
			addedImages[i].makeNonActive();
		}
		$('mainDiv_' + addedImages[0].id).setStyle('border: 1px dashed red;');
	});
}

/*
function show_image(location) {

	var insert = 0;
	for ( var i = 1; i <= total_images; i++) {
		if ($('big_image' + i) == null)
			insert = i;
	}
	if (insert == 0) {
		total_images++;
		insert = total_images;
	}

	// Creating the new image
	var newimg = Element.extend(document.createElement('img'));
	newimg.setAttribute('src', location);
	newimg
			.setStyle("opacity: 0.4; filter: alpha(opacity=40);  cursor: crosshair;");
	newimg.observe('click', function() {
		LoadMMDD("");
	});
	newimg.setAttribute('id', 'big_image' + insert);
	newimg.setAttribute('class', 'big_image_sibling');
	$('big_images').appendChild(newimg);

	// To do: make the sliders div just like the objects of the delete button
	// $('sliders').innerHTML = $('sliders').innerHTML+'<div
	// id="track'+insert+'" style="width:200px; background-color:#ccc;
	// height:10px;"><div id="handle'+insert+'" style="width:10px; height:15px;
	// background-color:#f00; cursor:move;"></div></div><p
	// id="valueopac'+insert+'">&nbsp;</p>';
	var newdiv1 = Element.extend(document.createElement('div'));
	newdiv1.setAttribute('id', 'track' + insert);
	newdiv1.setStyle("width:200px; background-color:#ccc; height:10px;");
	var newdiv2 = Element.extend(document.createElement('div'));
	newdiv2.setAttribute('id', 'handle' + insert);
	newdiv2
			.setStyle("width:10px; height:15px; background-color:#f00; cursor:move;");
	var newp1 = Element.extend(document.createElement('p'));
	newp1.setAttribute('id', 'valueopac' + insert);
	$('sliders').appendChild(newdiv1);
	newdiv1.appendChild(newdiv2);
	$('sliders').appendChild(newp1);
	eval("new Control.Slider('handle" + insert + "', 'track" + insert
			+ "', {onSlide: function(v) { $('valueopac" + insert
			+ "').innerHTML = 'slide: ' + v*100; ChangeOp(" + insert
			+ ",v) },onChange: function(v) { $('valueopac" + insert
			+ "').innerHTML = 'changed: ' + v*100;  ChangeOp(" + insert
			+ ",v) },sliderValue: 0.4})");

	// Creating the delete button
	var newbutton = Element.extend(document.createElement('button'));
	newbutton.innerHTML = 'Reset foto ' + insert;
	newbutton.onclick = function() {
		hide_image(insert)
	};
	newbutton.setAttribute('id', 'delete_photo_' + insert);
	$('delete_images').insert( {
		top : newbutton
	});
}
*/


function hideImage(id) {
	checkAuthenticationAndExecute( function() {

		//clear the data of this image
		$('bottomDiv' + id).update();
		$('mainDiv_' + id).setStyle('border: none;');

		var newImageArray = new Array();
		// Delete the old image and copy the rest
		for (i = 0; i < addedImages.length; i++) {
			if (addedImages[i].id != id) {
				newImageArray.push(addedImages[i]);
			}
		}
		
		addedImages = newImageArray;
		if (addedImages == "")
			getProjectPotentialMeasurements();
		
		//remove bitmaps
		for(var i = 0; i < bitmaps.length; i++){
			if(bitmaps[i].imageid == id){
				Element.remove($('bitmap_' + bitmaps[i].id));
				bitmaps.splice(i, 1);
				i = i - 1;
			}
		}
		
		//remove measurements
		for(var i = 0; i < measurements.length; i++){
			if(measurements[i].imageid == id){
				Element.remove(measurements[i].pinDiv);
				measurements.splice(i, 1);
				i = i - 1;
			}
		}
		
		//remove checkboxes
		for(var i = 0; i < checkboxes.length; i++){
			if(checkboxes[i].item.imageid == id){
				checkboxes.splice(i,1);
				i = i - 1;
			}
		}
		
		Element.remove($('addedImage_'+id))
		//true of false?
		//reloadImages(false);
	});
}

/*
function hide_image(id) {
	$('big_images').removeChild($('big_image' + id));
	$('delete_images').removeChild($('delete_photo_' + id));
	$('sliders').removeChild($('track' + id));
	$('sliders').removeChild($('valueopac' + id));
	total_images--;
}
*/

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
		Sortable.create("pictures", {
			tag : 'div',
			only : 'projectPictureDiv',
			onUpdate : updateImageList
		});
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
		reloadImages(false);

	});
}

function ChangeOp(id, value) {
	$('big_image' + id).setOpacity(value);
}