function getMouseXY(e) {

  if($('big_image1') != null){
    var BORDER_ADJUSTMENT = 2 // px
    //ugly IE fix for getting the value of the mouse
    //the '-2' fix is to correct for the borders
    if(document.all){
      mX = event.clientX-BORDER_ADJUSTMENT
      mY = event.clientY-BORDER_ADJUSTMENT
    }
    else{
      mX = e.clientX
      mY = e.clientY
    }
    if( mX-$('big_image1').offsetParent.offsetLeft >=0 &&
        mX-$('big_image1').offsetParent.offsetLeft <= $('big_image1').width &&
        mY-$('big_image1').offsetParent.offsetTop >=0 &&
        mY-$('big_image1').offsetParent.offsetTop <= $('big_image1').height
      ){      
      $('MouseX').value = mX-$('big_image1').offsetParent.offsetLeft;
      $('MouseY').value = mY-$('big_image1').offsetParent.offsetTop;
      return;
    }
  }
  $('MouseX').value = "";
  $('MouseY').value = "";
}