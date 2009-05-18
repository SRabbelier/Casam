function getMouseXY(e) {

  if($('big_images').firstChild != null){
    var mX = e.clientX
    var mY = e.clientY
  
    var viewportOffset = $('big_images').viewportOffset();    
    $('MouseX').value = mX-viewportOffset.left;
    $('MouseY').value = mY-viewportOffset.top;
   
  }

  if(addedImages[0]){
	  $('zoomImage').setAttribute('src',base_path+'imageLoader/byRatio/150/'+addedImages[0].id);
	  $('zoomImage').show();
  }else{
	  $('zoomImage').setAttribute('src','');
	  $('zoomImage').hide();
  }
  if($('zoomImage').getAttribute('src') && $('zoomImage').getAttribute('src') != '' ){
	  var zoomImg = new Image();
	  zoomImg.setAttribute('src',$('zoomImage').getAttribute('src'));
	  
	  var originalWidth = zoomImg.width / 1.5;
	  var originalHeight = zoomImg.height / 1.5;
	  var activeImages = $('big_images').select('.big_image_sibling');
	  if(!activeImages)return;
	  var activeImage = activeImages[activeImages.length-1];
	  if(!activeImage)return;
	  var middleImage = new Image();
	  middleImage.setAttribute('src',activeImage.getAttribute('src'));
	  var resizedWidth = middleImage.width;
	  var resizedHeight = middleImage.height;
	  
	  var zoomRatio = (originalWidth / resizedWidth) * 1.5;
	  var newLeft =  Math.round(-1 *  $('MouseX').value * zoomRatio + 90);
	  var newTop =  Math.round(-1 *  $('MouseY').value * zoomRatio + 90);
	  $('zoomImage').setStyle({
		  marginLeft:newLeft+'px',
		  marginTop:newTop+'px'
	  });
	  
	  
	  
  }

}