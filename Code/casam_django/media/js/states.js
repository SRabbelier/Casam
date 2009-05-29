var State = Class.create( {			
	initialize : function() {
			this.stateData = '';
			this.width = 0;
			this.height = 0;
	},
	fill: function(){
		this.stateData=$('big_images').innerHTML;
		var stateObject = this;
		$('big_images').select('img.big_image_sibling').each(function(item){
			stateObject.width = Math.max(stateObject.width,item.getWidth());
			stateObject.height = Math.max(stateObject.height,item.getHeight());
		});
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
		}else if(addedImages.length == 0){
			alert('Please select at least one image before saving the state');
		}else{
			var state = new State();
			state.fill();
			var url = base_path+'AJaX/addState/'+projectID;
			new Ajax.Request(url,{
				method:'post',
				parameters:{
					'serializedState':state.stateData,
					'name':$('stateNameTextfield').getValue(),
					'width':state.width,
					'height':state.height
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
			var states = transport.responseText.evalJSON();
			var statesContainer = new Element('div');
			for(i=0;i<states.length;i++){
				var stateDiv = new Element('div',{'id':'stateDiv_'+states[i].pk});
				var nameDateContainer = new Element('div');
				var nameDiv = new Element('div');
				nameDiv.insert(states[i].fields.name);
				nameDateContainer.insert(nameDiv);
				
				var dateDiv = new Element('div');
				dateDiv.insert(states[i].fields.added);
				dateDiv.addClassName('stateDivDate');
				nameDateContainer.insert(dateDiv);
				
				stateDiv.addClassName('stateDiv');
				stateDiv.insert(nameDateContainer);
				nameDateContainer.addClassName('stateNameDateDiv')

				stateDeleteDiv = new Element('div');
				stateDeleteDiv.insert(new Element('img',{'src':base_path+'media/img/delete.gif'}));
				stateDeleteDiv.addClassName('stateDeleteDiv');
				stateDiv.insert(stateDeleteDiv);

				statesContainer.insert(stateDiv);
				makeStateObserver(nameDateContainer,stateDeleteDiv,stateDiv,states[i].pk,states[i].fields.name);

			}

			$('tab_states').insert(statesContainer);
			
		}
	});
}

function makeStateObserver(clickDiv, deleteDiv, highlightDiv,id, stateName){
	clickDiv.observe('click',function(){
		new Effect.Highlight(highlightDiv);
		popupIFrame(base_path+'state/show/'+id)
	});
	deleteDiv.observe('click',function(){
		if(confirm('Are you sure you want to delete state: ' + stateName +'?')){
			new Effect.Highlight(highlightDiv,{'startcolor':'#ff0000','queue':'end'});
			var url = base_path + 'AJaX/deleteStates/';
			new Ajax.Request(url,{
				method: 'get',
				parameters: {'stateID':id},
				onSuccess:function(){
					new Effect.Fade(highlightDiv,{'queue':'end'});
				},
				onFailure:function(){
					alert('Something went wrong deleting '+stateName );
				}
			
			});
			
		}
	});
}
	



document.observe('dom:loaded',function(){
	loadStates();
});