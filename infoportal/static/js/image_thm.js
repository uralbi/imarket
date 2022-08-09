$(document).ready(function(){
$('.item_detail_img_thm').click(function(e){
  e.preventDefault();
  $('.item_detail_img').attr('src', $(this).attr("src"));
})
})


$(document).ready(function(){
    $('#open_modal').click(function() {
        $("#delete_modal").show();
         return false;
    });

});

$(document).ready(function(){
    $('#close_modal').click(function() {
        $("#delete_modal").hide();
    });
});

$(document).ready(function(){
    $('#main_img').click(function(){
        $('.my_image_modal').show()
    });

    $('#img_modal_close').click(function(){
        $('.my_image_modal').hide()
    });
});


$(document).ready(function(){
    $('.prev_btn').hover(
        function(){
            $(this).prepend('&#10094;')},
        function(){
            $(this).html('&#10094; PREV')
            });
    $('.next_btn').hover(
        function(){
            $(this).append('&#10095;')},
        function(){
            $(this).html('NEXT &#10095;')
            });
});