function getProjectAnnotations(){
	checkAuthenticationAndExecute( function() {
		$('tab_papers').update();
		annotationManagerLink = new Element('a',{'href':'#'});
		annotationManagerImage = new Element('img',{'src':base_path+'media/img/pencil.jpg'});
		annotationManagerImage.addClassName('smallPictureButton');
		annotationManagerLink.update(annotationManagerImage);
		annotationManagerLink.observe('click',
			function(){
				popupIFrame(base_path+'annotation/list/'+projectID);
			}
		);
		
		$('tab_papers').insert(annotationManagerLink);

		var url = '' + base_path + 'JSON/projectAnnotations/'+projectID;
		new Ajax.Request(url,{
			method:'get',
			onSuccess:function(transport){
				var json = transport.responseText.evalJSON();
				json.each(function(item){
					var annoDiv = new Element('div');
					var annoName = new Element('p').update(item.fields.name);
					var annoLink = new Element('p').update(item.fields.url.truncate(34));
					annoLink.addClassName('italic');
					annoDiv.insert(annoName);
					annoDiv.insert(annoLink);
					$('tab_papers').insert(annoDiv);
					annoDiv.addClassName('annotation_container');
					makeAnnotationDivObserver(annoDiv,item.fields.url);
					
				});
				
			}
		});
		//console.log('test');
	});
}

function makeAnnotationDivObserver(div, link){
	div.observe('click',function(){
		new Effect.Pulsate(div,{
			pulses:2,
			duration:0.3,
			afterFinish:
			function(){
				window.open(link);
			}
		});
		
	});

}