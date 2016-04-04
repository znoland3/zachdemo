

/* Hide Table Details */
$(".detail_row").hide();

/* Toggle Table details */
$(".element_parent").click(function() {

    var toggle_target;
    toggle_target = $(this).children('.name').text();


    var arrow;
    arrow = $(this).children('.arrow').children('i').attr('class');
    if (arrow == "fa fa-caret-down") {
        $(this).children('.arrow').html("<i class='fa fa-caret-right'></i>");
        $( '.' + toggle_target ).fadeOut();
    } else {
        $(this).children('.arrow').html("<i class='fa fa-caret-down'></i>");
        $( '.' + toggle_target ).fadeIn();
    };



});