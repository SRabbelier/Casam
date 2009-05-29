function checkAuthenticationAndExecute(customFunction,possibleFailureMessage){
	new Ajax.Request(base_path+'JSON/userAuthenticated/?time='+new Date().getTime(),{
		method: 'get',
		onSuccess:function(transport){
			customFunction();
		},
		onFailure:function(transport){
			if(!possibleFailureMessage)possibleFailureMessage="You are not logged in, click OK to login";
			location.href=base_path;
		}
	});
	

}

Element.addMethods({
        setWidth: function(element, width) {
                element = $(element);
                if (typeof width == "number")
                        width = width + "px";
                element.setStyle({width: width});
                return element;
        },

        setHeight: function(element, height) {
                element = $(element);
                if (typeof height == "number")
                        height = height + "px";
                element.setStyle({height: height});
                return element;
        }});

document.observe('dom:loaded',function(){
	$('popupCloseButton').observe('click',function(){
		closePopup();
	});
	$('popup').hide();
});

function popupIFrame(url,width,height){
	checkAuthenticationAndExecute(function(){
		if(!popupActive){
			$('popup_overlay').hide();
			$('popup_overlay').setWidth(document.viewport.getWidth());
			$('popup_overlay').setHeight(document.viewport.getHeight());
			$('popup_overlay').setStyle({
				zIndex:9998
			});
			new Effect.Appear('popup_overlay',{to:0.8});
			$('popup').show();
		}
		popupActive = true;
		if(!width)width=600;
		if(!height)height=400;
		
		var iF = new Element('iframe', {'src':url});
		$('popupIFrameContainer').update(iF);
		
		
		changePopupDimensions(width, height);
		

	});
	
}
function changePopupDimensions(width,height){
	wishfulPopupWidth = width;
	wishfulPopupHeight = height;
	var maxWidth = document.viewport.getWidth() - 100;
	var maxHeight = document.viewport.getHeight() - 100	;
	$('popup').setWidth(Math.min(width+1,maxWidth));
	$('popup').setHeight(Math.min(height+20,maxHeight));
	$('popup').setStyle({
		zIndex:9999,
		top:((document.viewport.getHeight() - $('popup').getHeight())/2)+'px',
		left:((document.viewport.getWidth() - $('popup').getWidth())/2)+'px'
		});
	//console.log('Update popup size width:'+width+' height:'+height)
}

function closePopup(){
	$('popup').hide();
	$('popup').setStyle({
		zIndex:0,
		top:'0px',
		left:'0px'
		});
	$('popupIFrameContainer').update();
	new Effect.Fade('popup_overlay',{afterFinish:
		function(){
			$('popup_overlay').setWidth(0);
			$('popup_overlay').setHeight(0);	
			$('popup_overlay').setStyle({
				zIndex:0
			});
			popupActive = false;
		}
	});

}

Event.observe(window,'resize',function(){
	if(popupActive){
		$('popup_overlay').setWidth(document.viewport.getWidth());
		$('popup_overlay').setHeight(document.viewport.getHeight());
		$('popup').setStyle({
			top:((document.viewport.getHeight() - $('popup').getHeight())/2)+'px',
			left:((document.viewport.getWidth() - $('popup').getWidth())/2)+'px'
			});
		changePopupDimensions(wishfulPopupWidth,wishfulPopupHeight);
	}
});

var wishfulPopupWidth = 0;
var wishfulPopupHeight = 0;



