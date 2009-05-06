function getMouseXY(e) {

  if($('big_images').firstChild != null){
    mX = e.clientX
    mY = e.clientY
  
      viewportOffset = $('big_images').viewportOffset();    
      $('MouseX').value = mX-viewportOffset.left;
      $('MouseY').value = mY-viewportOffset.top;
 
  }

}