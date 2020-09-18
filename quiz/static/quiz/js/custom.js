new fullpage('#fullpage', {
	anchors: ['page1', 'page2', 'page3', 'page4','page5'],
	navigationTooltips: ['fullPage', 'Open', 'Easy', 'Touch'],
	css3: true,
	scrollingSpeed: 1000,
	navigation: true,
	slidesNavigation: true,
	responsiveHeight: 50,
	dragAndMove: true,
	// dragAndMoveKey: 'YWx2YXJvdHJpZ28uY29tX0EyMlpISmhaMEZ1WkUxdmRtVT0wWUc=',
	controlArrows: false,
	menu: '#menu',
verticalCentred: true,

	
});

$('#popup').click(function(){
$('#popup').modal('hide');
});


//$(document).on('click', '#jumpto', function(){
// fullpage_api.moveTo($(this).index);
//});

$('#jumpto').on('click',function() {
    fullpage_api.moveTo($(event.target).index() + 2);
});

function start() {
    fullpage_api.moveTo(2);
};


