function getMouseXY(e) {

  if($('big_image1') != null){
    //ugly IE fix for getting the value of the mouse
    if(document.all){
      mX = event.clientX
      mY = event.clientY
    }
    else{
      mX = e.pageX
      mY = e.pageY
    }
    if( mX-$('big_image1').offsetLeft >=0 &&
        mX-$('big_image1').offsetLeft <= $('big_image1').width &&
        mY-$('big_image1').offsetTop >=0 &&
        mY-$('big_image1').offsetTop <= $('big_image1').height
      ){
      $('MouseX').value = mX-$('big_image1').offsetLeft;
      $('MouseY').value = mY-$('big_image1').offsetTop;
      return;
    }
  }
  $('MouseX').value = "";
  $('MouseY').value = "";
}