var Change = Class
		.create( {
			initialize : function(type, lmid, lmname) {
				//type: p is for positioning landmarks, r is for repositioning landmarks
				this.type = type;
				this.potid = lmid;
				this.lmname = lmname;
				this.metingid = '';
				this.oldx = '';
				this.oldy = '';
				this.saved = false;
				this.changeDiv = '';
				this.imageid = addedImages[0].id;
				this.saveButton = '';
				this.posx = '';
				this.posy = '';
			},
			reposition : function(mid, x, y) {
				this.metingid = mid;
				this.oldx = this.posx;
				this.oldy = this.posy;
				this.posx = x;
				this.posy = y;
			},
			position : function(x, y) {
				this.posx = x;
				this.posy = y;
			},
			forceSave : function() {
				if (!this.saved) {
					this.changeDiv.childElements()[1].remove();
					this.saveButton = '';
				}
				this.saved = true;
				this.changeDiv.removeClassName('unsavedChangeDiv');
				this.changeDiv.addClassName('savedChangeDiv');
			},
			save : function() {
				this.forceSave();
				mid = this.metingid;
				changes.each( function(item) {
					if (item.metingid == mid) {
						item.forceSave();
					}
				});
			},
			add : function() {
				this.changeDiv = new Element('div');
				if (this.saved)
					this.changeDiv.addClassName('savedChangeDiv');
				else
					this.changeDiv.addClassName('unsavedChangeDiv');
				var span = new Element('span');
				if (this.type == 'r')
					span.update('Landmark ' + this.lmname + ' has moved from ('
							+ this.oldx + ',' + this.oldy + ') to ('
							+ this.posx + ',' + this.posy + ')')
				else
					span.update('Landmark ' + this.lmname
							+ ' has been placed at (' + this.posx + ','
							+ this.posy + ')');
				this.changeDiv.insert(span);
				if (!this.saved) {
					var saveButton = new Element('a', {
						'href' : '#'
					});
					saveButton.addClassName('saveChangeButton');
					saveButton.update('Save this change');
					this.saveButton = saveButton;
					this.changeDiv.insert(saveButton);
				}
				$('ajax_result').insert(this.changeDiv);
				watchSaveButton(this);
			},
			undo : function() {
				$('ajax_result').childElements()[$('ajax_result')
						.childElements().length - 1].remove();
				undoLastLandmarkChange(this.oldx, this.oldy, this.potid,
						this.imageid, this.metingid);
				changes.pop();
			},
			erase : function() {
				this.changeDiv.remove();
			}
		});
function reloadUndoneChange(metingid, posx, posy) {
	var pin = ''
	for ( var i = 0; i < measurements.length; i++) {
		if (measurements[i].id == metingid) {
			pin = measurements[i];
			break;
		}
	}
	pin.calcpieces();
	pin.setPlace(posx / pin.piecex, posy / pin.piecey);
	pin.place();
	var currentMeasurements = $('bottomDiv' + pin.imageid).childElements()[1]
			.childElements()[2].childElements();
	for ( var i = 0; i < currentMeasurements.length; i++) {
		if (currentMeasurements[i].childElements()[0].name == pin.id) {
			currentMeasurements[i].childElements()[1].update(pin.name + ' ('
					+ Math.round(pin.x) + ',' + Math.round(pin.y) + ')');
			break;
		}
	}
}

function reloadUndonePlace(potid, imageID) {
	var url = base_path + 'AJaX/deleteMeasurement/?time='
			+ new Date().getTime();
	new Ajax.Request(
			url,
			{
				method : 'get',
				parameters : {
					'potentialMeasurementID' : potid,
					'imageID' : imageID
				},
				onSuccess : function(transport, json) {
					var pin = ''
					for ( var i = 0; i < measurements.length; i++) {
						if ((measurements[i].potid == potid)
								&& (measurements[i].imageid = imageID)) {
							pin = measurements[i];
							measurements.splice(i, 1);
							break;
						}
					}
					pin.restore();
					measurementDescriptionOffset = $('mm' + potid).up().down(
							"div[class='mmText']").positionedOffset();
					$('mm' + potid).setStyle( {
						'left' : (measurementDescriptionOffset[0] - 12) + 'px',
						'top' : (measurementDescriptionOffset[1]) + 'px'
					});

					var currentMeasurements = $('bottomDiv' + imageID)
							.childElements()[1].childElements()[2]
							.childElements();
					for ( var i = 0; i < currentMeasurements.length; i++) {
						if (currentMeasurements[i].childElements()[0].name == pin.id) {
							currentMeasurements[i].remove();
							break;
						}
					}
				},
				onFailure : function() {
					alert('Something went wrong while restoring measurement');
				}
			});
}

function undoLastChange() {
	var c = changes[changes.length - 1];
	c.undo();
}