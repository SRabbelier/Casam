function getMouseXY(e) {

  if($('big_images').firstChild != null){
    var mX = e.clientX
    var mY = e.clientY
  
    var viewportOffset = $('big_images').viewportOffset();    
    $('MouseX').value = mX-viewportOffset.left;
    $('MouseY').value = mY-viewportOffset.top;
 
  }

}