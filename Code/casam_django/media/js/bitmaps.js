var Bitmap = Class.create( {
	initialize : function(bm, bmid, imageid, potid, typeid) {
		this.bitmap = bm;
		this.id = bmid;
		this.imageid = imageid;
		this.potid = potid;
		// Ugly default so this 'measurement' won't be selected when super_check is (de)selected
		this.typeid = 0; 
	},
	getAppropriateSizeURL : function() {
		return (base_path + 'imageLoader/byMaxWidthHeight/bitmap/'
				+ ($('big_images').getWidth() - 2) + '/'
				+ ($('big_images').getHeight() - 2) + '/' + this.id+'?time='+new Date().getTime());
	},
	resize : function() {
		this.bitmap.writeAttribute('src', this.getAppropriateSizeURL());
		this.bitmap.observe('load', function() {
			//big_images need to be resized again when the bitmaps are loaded 
			// the javascript continues while this.getAppropriateSizeURL()
			// is still finding the correct size for the bitmap
			resizeBigImages();
		});
	}
});

function addBitmap(bmid, imgid, potid, min_x, max_x, min_y, max_y) {
	
	// Create html-elements
	var bitmapDiv = new Element('div', {
		'id' : 'bitmapDiv_' + bmid
	});
	
	bitmapDiv.addClassName('projectImageBitmapDiv');
	bitmapDiv.addClassName('projectImageBitmapDivPotId_'+potid)

	var bitmap = new Element('img', {
		'id' : 'bitmap_' + bmid
	});

	var bm = new Bitmap(bitmap, bmid, imgid, potid)
	bitmaps.push(bm);

	bitmap.writeAttribute('src', '');
	bitmap.writeAttribute('src', bm.getAppropriateSizeURL());
	bitmap.addClassName('big_image_sibling_bitmap');
	$('big_images').insert(bitmap);
	bitmap.hide();
	
	// Redirect a click
	bitmap.observe('click', function(e) {
		hideLandmarkTooltip(e);
		LoadMMDD('', addedImages[0].id);
	});

	bitmap.setOpacity(0.5);

	checkbox = new Element('input', {
		'type' : 'checkbox',
		'name' : bmid,
		'id' : 'showbm' + bmid
	});	

	var check = new Check('b', bmid, checkbox, bm);
	check.setDefault();
	check.watch();
	checkboxes.push(check);

	textspan = new Element('span', {
		'id' : 'spanbm_' + bmid
	});
	textspan.update($('potmeas_'+potid).down('div').innerHTML);
	editlink = new Element('a', {'href':'javascript:loadEditScreen(\''+imgid+'\', \''+potid+'\', \''+bmid+'\', \''+min_x+'\', \''+max_x+'\', \''+min_y+'\', \''+max_y+'\')'});
	editimg = new Element('img');
	editimg.writeAttribute('src', base_path + 'media/img/pencil.gif');
	editimg.addClassName('smallPictureButton');
	editlink.insert(editimg);
	textspan.insert(editlink);
	bitmapDiv.insert(checkbox);
	bitmapDiv.insert(textspan);

	$('mm' + potid).hide();
	
	return bitmapDiv;
}

function reloadBitmaps() {
	//loop through the checkboxes array, to find all the bitmaps
	for ( var i = 0; i < checkboxes.length; i++) {
		if ((checkboxes[i].type == 'b')) {

			checkboxes[i].item.resize();

			$('big_images').insert(checkboxes[i].item.bitmap);
			checkboxes[i].item.bitmap.hide();
			// only show the bitmaps when the checkbox was checked
			if (checkboxes[i].checked)
				checkboxes[i].item.bitmap.show();
		}
	}
}

function removeBitmaps(imageID){
	for(var i = 0; i < bitmaps.length; i++){
		if(bitmaps[i].imageid == imageID){
			console.log(bitmaps[i].id)
			Element.remove($('bitmap_' + bitmaps[i].id));
			bitmaps.splice(i, 1);
			i = i - 1;
		}
	}
}