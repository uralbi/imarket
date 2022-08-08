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