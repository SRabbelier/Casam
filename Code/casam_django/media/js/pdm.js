var PDM = Class.create( {			
	initialize : function() {
		this.pdmData = new Array();
	},
	fill: function(){
		var addedObjects = new Array();
		for(i=0;i<addedImages.length;i++){
			var objectArray = new Array();
			objectArray.push(addedImages[i].id);//get the active images		
			var measurementsArray = new Array();
			checkboxes.each(function(item){
				if ((item.type == 's') || (item.type == 'b')){					
					if(item.item.imageid == addedImages[i].id && item.checked && item.type =='s'){
						measurementsArray.push(item.id);//get the measurements for each of those images
					}
				}
			});
			objectArray.push(measurementsArray);
			addedObjects.push(objectArray);
		}
		this.pdmData=addedObjects;
	}
	
});

document.observe('dom:loaded',function(){
	$('analyzeLandmarksButton').observe('click',function(){
		var pdmObject = new PDM();
		pdmObject.fill();
		var url = base_path+'vtk/PDMCreator?time='+new Date().getTime();
		new Ajax.Request(url,{
			method:'post',
			parameters:{
				'projectID':projectID,
				'pdmData':Object.toJSON(pdmObject)
			},
			onSuccess:function(transport){
				alert(transport.responseText);
				getProjectOverlays();
			},
			onFailure:function(transport){
				alert(transport.responseText);
			}
		});
	});
	$('MakeMorphButton').observe('click',function(){
		var pdmObject = new PDM();
		pdmObject.fill();
		var url = base_path+'vtk/MorphCreator?time='+new Date().getTime();
		new Ajax.Request(url,{
			method:'post',
			parameters:{
				'projectID':projectID,
				'pdmData':Object.toJSON(pdmObject)
			},
			onSuccess:function(transport){
				alert(transport.responseText);
				getProjectImages()
			},
			onFailure:function(transport){
				alert(transport.responseText);
			}
		});
	});
});
