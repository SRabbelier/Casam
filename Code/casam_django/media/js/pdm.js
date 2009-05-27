var PDM = Class.create( {			
	initialize : function(JSONString) {
		this.pdmData = new Array();
	},
	fill: function(){
		var addedObjects = new Array();
		for(i=0;i<addedImages.length;i++){
			var objectArray = new Array();
			objectArray.push(addedImages[i].id);		
			var measurementsArray = new Array();
			checkboxes.each(function(item){
				if(item.item.imageid == addedImages[i].id && item.checked && item.type =='s'){
					measurementsArray.push(item.id);
				}
			});
			objectArray.push(measurementsArray);
			addedObjects.push(objectArray);
		}
		console.log(Object.toJSON(addedObjects));
		this.pdmData=addedObjects;
	}
});
