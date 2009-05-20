function undoLastLandmarkChange(x, y, potid, imgid, mid) {
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
		;
		if (found) {
			c = new Change('r', mm,
					$('mmmeting').options[$('mmmeting').selectedIndex].text);
			c.position(Math.round(measurement.left), Math
					.round(measurement.top));
			c.reposition(measurement.id, mousex, mousey);
		} else {
			c = new Change('p', mm,
					$('mmmeting').options[$('mmmeting').selectedIndex].text);
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
							measurement.calcpieces();
							measurement.setPlace(mousex / measurement.piecex,
									mousey / measurement.piecey);
							measurement.place();
							var currentMeasurements = $(
									'bottomDiv' + measurement.imageid)
									.childElements()[1].childElements()[2]
									.childElements();
							for ( var i = 0; i < currentMeasurements.length; i++) {
								if (currentMeasurements[i].childElements()[0].name == measurement.id) {
									currentMeasurements[i].childElements()[1]
											.update(measurement.name + ' ('
													+ Math.round(measurement.x)
													+ ','
													+ Math.round(measurement.y)
													+ ')');
									new Effect.Highlight(currentMeasurements[i]);
									break;
								}
							}
						} else {
							var json = transport.responseText.evalJSON();
							//json[i] = meting
							//json[i+1] = image
							//getMainDiv to do mainDiv.insert
							var mainDiv = $('bottomDiv' + json[1].pk)
									.childElements()[1].childElements()[2];
							mainDiv.insert(createMeasurement(c.lmname,
									json[1].fields.name, mousex, mousey,
									json[0].pk, mm, json[1].pk,
									json[0].fields.imagewidth,
									json[0].fields.imageheight));
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

						$('lmdd').hide();
					}
				});
	}
}

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
	obj = (!e.target ? e.srcElement : e.target);
	if ($('MouseX').value != "" && $('MouseY').value != "") {
		xoffset = obj.offsetLeft * 1 + 12;
		yoffset = obj.offsetTop * 1 - 5;
		var tooltip = obj.parentNode.lastChild
		tooltip.setStyle('left: ' + xoffset + 'px; top: ' + yoffset + 'px;');
		tooltip.show();
	}
}
function hideLandmarkTooltip(e) {
	obj = (!e.target ? e.srcElement : e.target);
	var tooltip = obj.parentNode.lastChild;
	tooltip.hide();
}

var Measurement = Class.create( {
	initialize : function(id, potid, name, imageid, pin, originalWidth,
			originalHeight) {
		this.id = id;
		this.potid = potid;
		this.name = name;

		//info about the image
		this.imageid = imageid;
		this.originalWidth = originalWidth;
		this.originalHeight = originalHeight;

		//these are the coordinates of the pin in the original image
		this.x = 0;
		this.y = 0;

		this.pinDiv = pin;
		//theze are the coordinates of the pin in the scaled image
		this.left = 0;
		this.top = 0;

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
		$('mm' + this.potid).hide();
	},
	nonActive : function() {
		this.changeColor('green');
		if (this.drag != null)
			this.drag.destroy();
	},
	erase : function() {
		this.nonActive(); //to destroy draggable
	this.pinDiv.remove(); //remove the whole pin
}
});
function makeDraggable(measurement, pinDiv, potid, imageid) {
	return new Draggable(pinDiv, {
		onStart : function() {
			var c = new Change('r', potid, measurement.name);
			c.position(Math.round(measurement.left), Math
					.round(measurement.top));
			changes.push(c);
		},
		onDrag : function(element, event) {
			pinDiv.childElements()[1].hide();
		},
		onEnd : function() {
			LoadMMDD(potid, imageid);
			var c = changes.pop();
			c.reposition(measurement.id, $('lmmx').value, $('lmmy').value);
			c.add();
			changes.push(c);
		}
	});
}

function getImageMeasurements(imgid) {
	var url = base_path + 'JSON/projectImageCurrentMeasurements/' + imgid
			+ '?time=' + new Date().getTime();
	new Ajax.Request(
			url,
			{
				method : 'get',
				onSuccess : function(transport, json) {
					var json = transport.responseText.evalJSON();
					var mainDiv = new Element('div');
					mainDiv.addClassName('projectPictureDiv');

					//add Div for tab
				var tempDiv = new Element('div');
				tempDiv.insert(mainDiv);

				for ( var i = 0; i < measurements.length; i++) {
					if (measurements[i].imageid == imgid) {
						measurements[i].restore();
						measurements.splice(i, 1);
						//splice shifts the index of the array 1 to the left, so compensate
				i = i - 1;
			}
		}

		var imgname = '';
		for ( var j = 0; j < addedImages.length; j++) {
			if (addedImages[j].id == imgid) {
				imgname = addedImages[j].name;
				break;
			}
		}
		for (i = 0; i < json.length - 1; i = i + 2) {
			mainDiv.insert(createMeasurement(json[i].fields.name, imgname,
					json[i + 1].fields.x, json[i + 1].fields.y, json[i + 1].pk,
					json[i].pk, imgid, json[i + 1].fields.imagewidth,
					json[i + 1].fields.imageheight));
		}

		if ($('bottomDiv' + imgid).childElements().length == 2) {
			$('bottomDiv' + imgid).childElements()[1].childElements()[2].innerHTML = mainDiv.innerHTML;
		} else {
			var tab_measurements = newTab('Measurements', mainDiv, true);
			tab_measurements.addClassName('imgSubTabMeasurements');
			$('bottomDiv' + imgid).insert(tab_measurements);
		}
	}
});
}

function createMeasurement(name, imgname, x, y, measid, potid, imgid, imgwidth,
		imgheight) {

	var pinDiv = new Element('div');
	pinDiv.addClassName('pinDiv');
	pinDiv.hide();

	var pin = new Element('img', {
		'src' : base_path + 'media/img/pin_green.gif'
	});
	pin.addClassName('pinImage');
	var pintooltip = new Element('div').update(name + '<br />' + imgname
			+ '<br />' + x + ', ' + y);
	pintooltip.addClassName('pintooltip');
	pintooltip.hide();

	pin.observe('mouseover', showLandmarkTooltip);
	pin.observe('mouseout', hideLandmarkTooltip);

	pinDiv.insert(pin);
	pinDiv.insert(pintooltip);
	$('big_images').insert(pinDiv);

	var measurement = new Measurement(measid, potid, name, imgid, pinDiv,
			imgwidth, imgheight);
	var measurementDiv = new Element('div', {
		'id' : 'potidMeasDiv_' + potid
	});
	measurementDiv.addClassName('projectImageMeasurementDiv');

	checkbox = new Element('input', {
		'type' : 'checkbox',
		'name' : measid,
		'id' : 'show' + measid
	});

	var check = new Check('s', measid, checkbox, measurement);

	//when called insert, IE defaults his checkboxes to the default value (which is false).
	//so set the default to true
	check.setDefault();
	check.watch();

	checkboxes.push(check);

	textspan = new Element('span', {
		'id' : 'span_' + potid
	});
	textspan.update(name + ' (' + x + ', ' + y + ')')
	measurementDiv.insert(checkbox);
	measurementDiv.insert(textspan);

	//load the measurements the first time
	measurement.setPlace(x, y);
	measurement.place();

	if (addedImages[0].id == imgid)
		measurement.setActive();
	else
		measurement.nonActive();

	measurements.push(measurement);
	return measurementDiv
}

function watchSaveButton(item) {
	item.saveButton.observe('click', function() {
		item.save();

		saveLandMark(item.posx, item.posy, item.potid, item.imageid);
	});
}

function createPotentialMeasurement(potid, potname) {
	var pmmContainerDiv = new Element('div', {
		'id' : 'potmeas_' + potid
	});
	pmmContainerDiv.addClassName('potMeasDiv');
	var pmmPointerIMG = new Element('img', {
		'src' : base_path + 'media/img/pin_blue.gif',
		'id' : ('mm' + potid)
	});
	pmmPointerIMG.addClassName('mmPointer');
	pmmContainerDiv.insert(pmmPointerIMG);
	var json = json;

	var pmmTextDiv = new Element('div', {
		'class' : 'mmText'
	}).update(potname);
	pmmContainerDiv.insert(pmmTextDiv);

	var pmmDeleteIMG = new Element('img', {
		'src' : base_path + 'media/img/delete.gif',
		'id' : ('mmDel' + potid)
	});
	pmmDeleteIMG.addClassName('pmmDelete');
	//pmmContainerDiv.insert(pmmDeleteIMG);

	$('possiblemeasurements').insert(pmmContainerDiv);

	var option = new Element('option', {
		'id' : 'option' + potid,
		'value' : potid
	});
	option.update(potname);
	$('mmmeting').add(option, null)
}