var page_url = 'techgeek/get-question';
var page_url_index = 'techgeek';

var questionIds = [];
var interfaceNextId,interfaceCurId;
var i=1;
var time, clk;
var isFirst;

$(document).ready(function(){
	getQuestions();

});

function leaderboard(){
   // $.get('/kryptos/',function(data){});
    $.get('/techgeek/leaderboard',function(data){
        var leaderboard_element = $('#leadergeek');
        data = data.leaderboard_data;
        leaderboard_element.html('');
        for(var i=0; i<data.length; ++i )
        {
            toper_data = data[i];
            console.log(data[i])
            var outer = $('<div class="media p-l-5"></div>');
            var profile_pic = $('<img width="40" alt="">').attr("src",toper_data.image_url); 
            var image = $('<div class="pull-left"></div>').html(profile_pic);
            outer.append(image);
            var details = $('<div class="media-body"></div>');
            var name = $('<a class="t-overflow marg"></a>').text(toper_data.name); 
            var level = $('<a class="t-overflow marg" style="font-size:11px;margin-top:5px;"></a>').text('Score ' + toper_data.score + "                             #" + (i+1));
            details.append(name);
            details.append(level);
            outer.append(details);
            leaderboard_element.append(outer);
        }
  
    });
}
function getQuestions(){
	// alert("hello");
	console.log('get-question');
	$.ajax({
		type:'GET',
		url: page_url_index,
		success: startGame
	});
	
}

function startGame(){
	$.ajax({
		type:"POST",
		data:{'qns_id':-1,'-1':''},
		url: page_url,
		success:populate
	});
}


function populate(data){
	clearInterval(clk);
	var initTime = 900 - data.timestamp;
	var initMin = Math.floor(initTime/60);
	if(initTime<60)
		initMin = 0;
	var remainingTime = initTime - initMin*60;
	var initSec = remainingTime;
	console.log(initMin+':'+initSec);
	start_timer(initMin,initSec);
	var disp = $('#contents');
	disp.append( $('<p style="font-size:15px;"></p>').text(data.qns) );
	var k=0;
	interfaceNextId=data.next_id;
	interfaceCurId=data.qnsId;

	for( var choice of data.option )
	{
		var ch = $('<div class="radio" style="margin-left:5%;"></div>');
		k++;
		//var label = $('<label></label>');
		console.log(choice);
		var label = $('<label><input type="radio" name="radio" value="'+choice+'" style="position: absolute; top: -20%; left: -20%; display: block; width: 140%; height: 140%; margin: 0px; padding: 0px; background: rgb(255, 255, 255); border: 0px; opacity: 0;">'+choice+'</label>');
		// console.log(Textques);
		//label.append(Textques);
		ch.append(label);
		disp.append( ch );
		// disp.append( label.text(choice) );
	}
	var button=$('<button type="button" id="next" class="btn btn-sm btn-alt" style="float:right;margin:20px 50px 0px;width:60px">Next</button>');
	disp.append(button);

	radioload();
	i++;
	$('#next').on('click',function(){
	var postData={};
	// alert($('input[name=question]:checked').val());
	var v;
	if($("input:radio[name='radio']").is(":checked"))
		v=$('input[name=radio]:checked').val();
	else
		v="";
	console.log(v);
	postData[String(interfaceCurId)]=v;
	postData['qns_id'] = interfaceNextId;
	$.ajax({
		type:'POST',
		data:postData,
		url: page_url,
		success: clean
	});
	});
	
}
function clean(data){
	$('#contents').text("");
	if(data.qnsId==-1){
		$('#next').remove();
		var successText=$('<p style="font-size:15px"></p>');
		clearInterval(clk);
		successText.text(data['qns']);
		$('#contents').append(successText);
	}
	else
		populate(data);
}

function timer()
{
	if( time.sec== 0 )
	{
		if( time.min != 0 )
			--time.min;
		else{
			var postData={};
			var v;
			if($("input:radio[name='radio']").is(":checked"))
				v=$('input[name=radio]:checked').val();
			else
				v="";
			console.log(v);
			postData[String(interfaceCurId)]=v;
			postData['qns_id'] = interfaceNextId;
			$.ajax({
				type:'POST',
				data:postData,
				url: page_url,
				success: clean
			});
			return clearInterval(clk);
		}
		time.sec = 59;
	}
	else
		--time.sec;

	if(time.min<10)
		$('#min').text('0'+time.min);
	else
		$('#min').text(time.min);
	
	if(time.sec<10)
		$('#sec').text('0'+time.sec);
	else
		$('#sec').text(time.sec);
}

function start_timer(mins,secs)
{
	time = { min: mins , sec : secs  };
	clk = setInterval(timer,1000);
}
