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
				var stateDiv = new Element('div',{'id':'stateDiv_'+states[i].id});
				var nameDiv = new Element('div');
				nameDiv.insert(states[i].fields.name);
				stateDiv.insert(nameDiv);
				
				var dateDiv = new Element('div');
				dateDiv.insert(states[i].fields.added);
				dateDiv.addClassName('stateDivDate');
				stateDiv.insert(dateDiv);
				
				stateDiv.addClassName('stateDiv');
				statesContainer.insert(stateDiv);

				makeStateObserver(stateDiv,states[i].pk);

			}

			$('tab_states').insert(statesContainer);
			
		}
	});
}

function makeStateObserver(div,id){
	div.observe('click',function(){
		new Effect.Highlight(div);
		popupIFrame(base_path+'state/show/'+id)
	});
}



document.observe('dom:loaded',function(){
	loadStates();
});