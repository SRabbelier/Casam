var Measurement = Class.create( {
	initialize : function(id, potid, typeid, name, imageid, pin, originalWidth,
			originalHeight) {
		this.id = id;
		this.potid = potid;
		this.typeid = typeid;
		this.name = name;

		//info about the image
		this.imageid = imageid;
		this.originalWidth = originalWidth;
		this.originalHeight = originalHeight;

		//these are the coordinates of the pin in the original image
		this.x = 0;
		this.y = 0;

		this.pinDiv = pin;
		
		// These are the coordinates of the pin in the scaled image
		this.left = 0;
		this.top = 0;

		// These are the scaling factors
		this.piecex = 0;
		this.piecey = 0;

		this.drag = null;
	},
	setPlace : function(x, y) {
		this.calcpieces();
		this.x = x;
		this.y = y;
		this.left = x * this.piecex;
		this.top = y * this.piecey;
	},
	place : function() {
		// if the pinDiv was not placed, place it
		if (this.pinDiv.ancestors() == '')
		  $('big_images').insert(this.pinDiv);
		
		this.pinDiv.setStyle( {
			position : 'absolute',
			left : '' + (Math.round(this.left)) + 'px',
			top : '' + (Math.round(this.top)) + 'px'
		});
		this.pinDiv.show();
	},
	replace : function() {
		this.calcpieces();
		this.left = this.x * this.piecex;
		this.top = this.y * this.piecey;
		this.place();
	},
	calcpieces : function() {
		this.piecex = $('addedImage_' + this.imageid).width
				/ this.originalWidth;
		this.piecey = $('addedImage_' + this.imageid).height
				/ this.originalHeight;
	},
	restore : function() {
		this.pinDiv.hide();
		// Show potential measurement again
		$('mm' + this.potid).show();
	},
	hide : function() {
		this.pinDiv.hide();
	},
	changeColor : function(color) {
		this.pinDiv.childElements()[0].src = base_path + "media/img/pin_"
				+ color + ".gif";
	},
	setActive : function() {
		this.changeColor('red');
		this.drag = makeDraggable(this, this.pinDiv, this.potid, this.imageid);
		// Hide corresponding potential measurement
		$('mm' + this.potid).hide();
	},
	nonActive : function() {
		this.changeColor('blue');
		// NonActive measurements are not draggable
		if (this.drag != null)
			this.drag.destroy();
	},
	erase : function() {
		// To destroy draggable
		this.nonActive(); 
		// Remove the whole pin
		this.pinDiv.remove(); 
	}
});
function watchSaveButton(item) {
	item.saveButton.observe('click', function() {
		item.save();

		saveLandMark(item.posx, item.posy, item.potid, item.imageid);
	});
}

function undoLastLandmarkChange(x, y, potid, imgid, mid) {
	// Measurement-id is unknown to the change on placing of landmark, so this can be checked
	if (mid == '')
		reloadUndonePlace(potid, imgid);
	else {
		new Ajax.Request(base_path + 'landmarks/save', {
			method : 'post',
			parameters : {
				x : escape(x),
				y : escape(y),
				mm : escape(potid),
				imgid : escape(imgid),
				imagewidth : $('addedImage_' + imgid).width,
				imageheight : $('addedImage_' + imgid).height
			},
			onSuccess : function() {
				reloadUndoneChange(mid, x, y);
			}
		});
	}
}

function saveLandMark(mx, my, potid, imgid) {
	var viewportOffset = $('big_images').viewportOffset();
	var mousex = (mx == undefined) ? $('lmmx').value : mx;
	var mousey = (my == undefined) ? $('lmmy').value : my;
	var mm = (potid == undefined) ? $('mmmeting').options[$('mmmeting').selectedIndex].value
			: potid;
	var imageID = (imgid == undefined) ? $('imgid').value : imgid;
	savex = mousex * 1 + viewportOffset.left * 1;
	savey = mousey * 1 + viewportOffset.top * 1;
	
	var c = '';
	var measurement = null;

	if (!$('mmmeting').disabled) {
		var found = false;
		for ( var i = 0; i < measurements.length; i++) {
			if (measurements[i].potid == mm
					&& measurements[i].imageid == imageID) {
				found = true;
				measurement = measurements[i];
				break;
			}
		}
		// Make change on saving landmark
		if (found) {
			c = new Change('r', mm, lmname);
			c.position(Math.round(measurement.left), Math.round(measurement.top));
			c.reposition(measurement.id, mousex, mousey);
		} else {
			c = new Change('p', mm, lmname);
			c.position(mousex, mousey);
		}
		c.add();
		changes.push(c);
	}

	if (mm == "" || mousex == "" || mousey == "") {
		alert("Please select a landmark!");
	} else {
		new Ajax.Request(
				base_path + 'landmarks/save',
				{
					method : 'post',
					parameters : {
						x : escape(mousex),
						y : escape(mousey),
						mm : escape(mm),
						imgid : escape(imageID),
						imagewidth : $('addedImage_' + imageID).width,
						imageheight : $('addedImage_' + imageID).height
					},
					onSuccess : function(transport, json) {
						// save the last created change. This can be done, because the change was created just before
						c = changes.pop();
						c.save();
						changes.push(c);
						var found = false;
						for ( var i = 0; i < measurements.length; i++) {
							if (measurements[i].potid == mm
									&& measurements[i].imageid == imageID) {
								var found = true;
								measurement = measurements[i];
								break;
							}
						}
						if (found) {
							// Replace existing measurement
							measurement.calcpieces();
							measurement.setPlace(mousex / measurement.piecex,
									mousey / measurement.piecey);
							measurement.place();
							$('span_'+measurement.id).update(measurement.name);
							new Effect.Highlight($('measidMeasDiv_'+measurement.id));
						} else {
							// Create new measurement
							var json = transport.responseText.evalJSON();
							//json[i] = meting
							//getMainDiv to do mainDiv.insert
							var typeid = $('potmeas_'+json[0].fields.mogelijkemeting).up().id.slice(9);
							var subtab = $('measurementTypeList_'+json[0].fields.image+'-'+typeid);
							subtab.insert(createMeasurement(c.lmname,
									mousex, mousey, json[0].pk, mm, json[0].fields.image,
									json[0].fields.imagewidth,
									json[0].fields.imageheight));
							subtab.up().show();
							// Replace the (new) measurement, just to be sure
							for ( var i = 0; i < measurements.length; i++) {
								if (measurements[i].potid == mm
										&& measurements[i].imageid == imageID) {
									measurement = measurements[i];
									break;
								}
							}
							measurement.calcpieces();
							measurement.setPlace(mousex / measurement.piecex,
									mousey / measurement.piecey);
							measurement.place();
						}

						
					},
					// on either fail or complete:
					onComplete: function(){
						$('lmdd').hide();						
					}
				});
	}
}

// Load MMMM Measurement Decision Div
function LoadMMDD(id, imgID) {
	var viewportOffset = $('big_images').viewportOffset();
	var mousex = $('MouseX').value;
	var mousey = $('MouseY').value;
	var xoffset = mousex * 1 + viewportOffset.left + 10;
	var yoffset = mousey * 1 + viewportOffset.top + 10;

	var imageID = imgID

	$('lmdd').setStyle('left: ' + xoffset + 'px; top: ' + yoffset + 'px;');
	$('lmmx').value = mousex;
	$('lmmy').value = mousey;
	$('imgid').value = imageID;
	if (id != "") {
		$('option' + id).selected = true;
		$('mmmeting').setStyle('visibility: visible');
		$('mmmeting').disabled = true;
		$('labelmmmeting').setStyle('visibility: visible');
	} else {
		$('mmmeting').setStyle('visibility: visible');
		$('mmmeting').disabled = false;
		$('labelmmmeting').setStyle('visibility: visible');
	}
	$('lmdd').show();
}

function showLandmarkTooltip(e) {
	// Set 'obj' no matter using firefox or internet explorer
	obj = (!e.target ? e.srcElement : e.target);
	if ($('MouseX').value != "" && $('MouseY').value != "") {
		xoffset = obj.offsetLeft * 1 + 12;
		yoffset = obj.offsetTop * 1 - 5;
		var tooltip = obj.parentNode.lastChild
		tooltip.setStyle('left: ' + xoffset + 'px; top: ' + yoffset + 'px;');
		
		// If the box doesn't fit on the rightbottom side in big_images, replace it
		if ( ((sizeFromStyle(obj.parentNode.style.left) + tooltip.getWidth() + 5) > $('big_images').getWidth() ) || 
				 ((sizeFromStyle(obj.parentNode.style.top) + tooltip.getHeight() + 5) > $('big_images').getHeight() ) )
			
			tooltip.setStyle('margin-left: -' + (tooltip.getWidth() + 5) + 'px;'
					           +' margin-top: -' + (tooltip.getHeight() + 5) + 'px;');
		else
			tooltip.setStyle('margin-left: 0px;margin-top: 0px;');
		
		tooltip.show();
	}
}
function hideLandmarkTooltip(e) {
	// Set 'obj' no matter using firefox or internet explorer
	obj = (!e.target ? e.srcElement : e.target);
	var tooltip = obj.parentNode.lastChild;
	tooltip.hide();
}


function makeDraggable(measurement, pinDiv, potid, imageid) {
	return new Draggable(pinDiv, {
		onStart : function() {
			// When starting the drag, create the change
			var c = new Change('r', potid, measurement.name);
			c.position(Math.round(measurement.left), Math
					.round(measurement.top));
			changes.push(c);
		},
		onDrag : function(element, event) {
			pinDiv.childElements()[1].hide();
		},
		onEnd : function() {
			// When ending the drag, update the change
			LoadMMDD(potid, imageid);
			var c = changes.pop();
			c.reposition(measurement.id, $('lmmx').value, $('lmmy').value);
			c.add();
			changes.push(c);
		}
	});
}

function createMeasurement(	name, x, y, measid, potid, imgid, imgwidth,
														imgheight) {
	
	// Find the image name, which is needed for the tooltip of the measurement
	var imgname = '';
	for ( var j = 0; j < addedImages.length; j++) {
		if (addedImages[j].id == imgid) {
			imgname = addedImages[j].name;
			break;
		}
	}

	var typename = $('potmeas_'+potid).up().up().down('span').innerHTML;
	var typeid = $('potmeas_'+potid).up().id.slice(9);
	var measname = name;

	var pinDiv = new Element('div');
	pinDiv.addClassName('pinDiv');
	pinDiv.hide();

	var pin = new Element('img', {
		'src' : base_path + 'media/img/pin_green.gif'
	});
	pin.addClassName('pinImage');
	var pintooltip = new Element('div').update(measname + '<br />' + imgname
			+ '<br />' + x + ', ' + y);
	pintooltip.addClassName('pintooltip');
	pintooltip.hide();

	pin.observe('mouseover', showLandmarkTooltip);
	pin.observe('mouseout', hideLandmarkTooltip);

	pinDiv.insert(pin);
	pinDiv.insert(pintooltip);
	$('big_images').insert(pinDiv);
	
	// Make new measurement object
	var measurement = new Measurement(measid, potid, typeid, measname, imgid, pinDiv,
			imgwidth, imgheight);
	
	var measurementDiv = new Element('div', {
		'id' : 'measidMeasDiv_' + measid
	});
	measurementDiv.addClassName('projectImageMeasurementDiv');

	checkbox = new Element('input', {
		'type' : 'checkbox',
		'name' : measid,
		'id' : 'showm_' + measid
	});

	// Make new checkbox object
	var check = new Check('s', measid, checkbox, measurement);
	check.setDefault();
	check.watch();
	checkboxes.push(check);

	textspan = new Element('span', {
		'id' : 'span_' + measid
	});
	textspan.update(measname);
	measurementDiv.insert(checkbox);
	measurementDiv.insert(textspan);

	//load the measurements the first time
	measurement.setPlace(x, y);
	measurement.place();

	// If the measurement is for the active image
	if (addedImages[0].id == imgid)
		measurement.setActive();
	else
		measurement.nonActive();

	measurements.push(measurement);
	return measurementDiv;
}

function createImageMeasurementSubTab(typeid, typename, imgid){
	var typeDiv = new Element('div');
	typeDiv.writeAttribute('id', 'measurementTypeList_'+imgid+'-'+typeid);
	typeDiv.addClassName('imgTypeMeasurements');
	
	var subtab_measurements = newTab(typename, typeDiv, true);
	subtab_measurements.id = 'measurementTypesDiv_'+imgid+'-'+typeid;
	subtab_measurements.addClassName('imgSubTabMeasurementTypes');
	
	// Create type checkbox
	super_check = new Element('input');
	super_check.writeAttribute('id', 'super_check_'+typeid);
	super_check.writeAttribute('type', 'checkbox');
	super_check.writeAttribute('name', typeid);
	super_check.writeAttribute('style', 'margin:0px;float:left;');
	subtab_measurements.insert({top: super_check});
	
	// Create ceckbox object
	var check = new Check('sg', typeid, super_check, null);
	check.setDefault();
	check.watch();
	checkboxes.push(check);

	return subtab_measurements;
}

function createPotentialMeasurementType(typeid, typename){

	var mainDiv = new Element('div', {'id': 'typesList'+typeid});
	mainDiv.addClassName('projectPotentialTypeDiv');

	var tab_potentialtypes = newTab(typename, mainDiv, true, true);
	tab_potentialtypes.writeAttribute('id','potSubTabType');
	$('possiblemeasurements').insert(tab_potentialtypes);		
	
	// Add the new subtab to the measurementslists of the images, but hide it.
	// This is so the measurements themselves can be added to their measurement types
	for(var i = 0;i < addedImages.length; i++){
		var subtab = createImageMeasurementSubTab(typeid, typename, addedImages[i].id);
		$('measurementsList_'+addedImages[i].id).insert(subtab);
		subtab.hide();
	}
	
	// Create an optiongroup for each potential measurement type
	var optgroup = new Element('optgroup');
	optgroup.writeAttribute('label', typename);
	optgroup.writeAttribute('id', 'optgroup_'+typeid);
	$('mmmeting').add(optgroup,null);
}

function createPotentialMeasurement(potid, pottype, potname, potsoort) {
	
	var pmmContainerDiv = new Element('div', {
		'id' : 'potmeas_' + potid
	});
	pmmContainerDiv.addClassName('potMeasDiv');
	
	var pmmPointerIMG = new Element('img', {
		'id' : ('mm' + potid)
	});
	// Base the picture of the potential measurement on it's 'soort'
	if (potsoort == 'L')
		pmmPointerIMG.writeAttribute('src', base_path + 'media/img/landmark.gif');
	else{
	  pmmPointerIMG.writeAttribute('src', base_path + 'media/img/pencil.gif');
	}
	pmmPointerIMG.addClassName('mmPointer');
	pmmContainerDiv.insert(pmmPointerIMG);
	var json = json;

	var pmmTextDiv = new Element('div', {
		'class' : 'mmText'
	}).update(potname);
	pmmContainerDiv.insert(pmmTextDiv);

	// Add the containerDiv to the correct list
	$('typesList'+pottype).insert(pmmContainerDiv);

	// Only add the potential measurement to the option list for creating measurements if it is a
	// 'Landmark'
  if (potsoort == 'L'){
  	var typename = $('typesList'+pottype).up().down('span').innerHTML;

		var option = new Element('option', {
			'id' : 'option' + potid,
			'value' : potid
		});
		option.update(potname);
		var optgroup = $('optgroup_'+pottype).next();
		$('mmmeting').add(option, optgroup);
  } 
  // Otherwise, set a link to the paintOver
  else{
  	var link = new Element('a');
		link.writeAttribute('href', '#');
		link.writeAttribute('id', 'paintoverLink_'+potid);
		link.addClassName('paintoverLink');
		$('mm'+potid).insert({before: link});
		link.update($('mm'+potid));
  	observeEditLink(potid);  	
  }
}
function observeEditLink(potid){
	$('paintoverLink_'+potid).observe('click', function(){
		if (addedImages.length > 0)
  		// Change the link if the bitmap already exists for the active image
  		var bitmapIDs = $('bitmapsList_'+addedImages[0].id).select('div.projectImageBitmapDivPotId_'+potid);
			if (bitmapIDs.length > 0)
				loadEditScreen(addedImages[0].id, potid, bitmapIDs[0].id.slice(10));
  		else 
  			loadEditScreen(addedImages[0].id, potid);
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
			// Correct for the index changing, done by the splice method
			i = i - 1;
		}
	}
}
function resizeMeasurements(imageID){
	for(var i = 0; i < checkboxes.length; i++) {
		if ((checkboxes[i].type == 's') && (checkboxes[i].item.imageid == imageID) &&
		    (checkboxes[i].box.checked == true)){
			  	checkboxes[i].item.replace();
		}
	}
}
