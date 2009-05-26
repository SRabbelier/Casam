var State = Class.create( {			
	initialize : function(JSONString) {
		//If no JSON string is given, create empty arrays
		if(!JSONString){
			this.stateData = new Array();
		//Otherwise, create the arrays with the value of the JSON string
		}else{
			var JSONObject = JSONString.evalJSON();
			this.stateData = JSONObject.fields.serializedState.evalJSON().stateData;
			this.name = JSONObject.fields.name;
			this.dateAdded = JSONObject.fields.added;
			this.id = JSONObject.pk;
		}
	},
	fill: function(){
		var addedObjects = new Array();
		for(i=0;i<addedImages.length;i++){
			var objectArray = new Array();
			objectArray.push(addedImages[i].id);
			objectArray.push(addedImages[i].name);
			objectArray.push(addedImages[i].opacity);
			
			var measurementsArray = new Array();
			var bitmapsArray= new Array();
			var picturesArray = new Array();
			
			//Checkboxes should contain unique values,
			//if not: kick Ben and Jaap :P
			checkboxes.each(function(item){
				if(item.item.imageid == addedImages[i].id){
					if(item.checked){
						if(item.type == 's'){
							measurementsArray.push(item.id);
						}else if(item.type=='b'){
							var bitmapArray = new Array();
							bitmapArray.push(item.id);
							bitmapArray.push(0.5);
							bitmapsArray.push(bitmapArray);
						}else if(item.type=='u'){
							//THIS DOESN'T SEEM TO BE NECESSARY
							//picturesArray.push(item.id);
						}
					}
				}
			});
			
			
			objectArray.push(measurementsArray);
			objectArray.push(bitmapsArray);
			
			addedObjects.push(objectArray);
		}
		console.log(Object.toJSON(addedObjects));
		//console.log(checkboxes);
		this.stateData=addedObjects;
	}
});

var states = new Array();

function loadStates(){
	$('tab_states').update();
	var stateNameDiv = new Element('div');
	var stateNameLabel = new Element('label',{'for':'stateNameTextfield'});
	stateNameLabel.update('Name');
	stateNameDiv.insert(stateNameLabel);
	var stateNameTexfield = new Element('input',{'type':'text','id':'stateNameTextfield'});
	stateNameDiv.insert(stateNameTexfield);
	var stateSubmitButton = new Element('input',{'type':'button','value':'Make new state'});
	stateNameDiv.insert(stateSubmitButton);
	stateSubmitButton.observe('click',function(){
		if(!$('stateNameTextfield') || $('stateNameTextfield').getValue() == ''){
			alert('Please give in a name for the state');
		}else{
			var state = new State();
			state.fill();
			var url = base_path+'AJaX/addState/'+projectID;
			new Ajax.Request(url,{
				method:'post',
				parameters:{
					'serializedState':Object.toJSON(state),
					'name':$('stateNameTextfield').getValue()
				},
				onSuccess:function(){
					loadStates();
				}
			});
		}
	});
	$('tab_states').insert(stateNameDiv);
	var url = base_path + 'JSON/projectStates/' + projectID;
	new Ajax.Request(url,{
		onSuccess:function(transport){
			var json = transport.responseText.evalJSON();
			var statesContainer = new Element('div');
			states = new Array();
			for(i=0;i<json.length;i++){
				var stateDiv = new Element('div');

				states.push(new State(Object.toJSON(json[i])));
			}
			for(i=0;i<states.length;i++){
				var stateDiv = new Element('div',{'id':'stateDiv_'+states[i].id});
				var nameDiv = new Element('div');
				nameDiv.insert(states[i].name);
				stateDiv.insert(nameDiv);
				
				var dateDiv = new Element('div');
				dateDiv.insert(states[i].dateAdded);
				dateDiv.addClassName('stateDivDate');
				stateDiv.insert(dateDiv);
				
				stateDiv.addClassName('stateDiv');
				statesContainer.insert(stateDiv);

				makeStateObserver(stateDiv,states[i]);
				
			}
			$('tab_states').insert(statesContainer);
			
		}
	});
}

function makeStateObserver(div,stateObject){
	div.observe('click',function(){
		new Effect.Highlight(div);
		setState(stateObject);
	});
}

function setState(stateObject){
	console.log(stateObject);
	console.log('Revert to state: '+stateObject.name);

	for(i = 0; i<stateObject.stateData.length;i++){
		var id = stateObject.stateData[i][0];
		var name = stateObject.stateData[i][1];
		showImage(id,name);
		$('use'+id).writeAttribute('checked','checked');
	}
	/*resizeScreenElements(true);
	checkActiveLayer();*/

}

document.observe('dom:loaded',function(){
	loadStates();
});