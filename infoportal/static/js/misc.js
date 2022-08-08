setTimeout(function(){
    $('#message').fadeOut('slow')
}, 3000)

$(document).ready(function(){
        $("#my_list_template").click(function(){
            $('.item_card').addClass("d-flex list_card").removeClass("item_card");
            $('.item_card_img').removeClass("item_card_img").addClass("list_card_img");
            $('.item_card_title').removeClass("item_card_title").addClass("list_card_title");
            $('.item_card_price').removeClass("item_card_price").addClass("list_card_price");
            $('.item_card_desc').removeClass("item_card_desc").addClass("list_card_desc");
            $('.item_card_date').removeClass("item_card_date").addClass("list_card_date");
            $(this).hide()
            $("#my_card_template").show()
        });

        $("#my_card_template").click(function(){
            $('.list_card').removeClass("d-flex list_card").addClass("item_card");
            $('.list_card_img').removeClass("list_card_img").addClass("item_card_img");
            $('.list_card_title').removeClass("list_card_title").addClass("item_card_title");
            $('.list_card_price').removeClass("list_card_price").addClass("item_card_price");
            $('.list_card_desc').removeClass("list_card_desc").addClass("item_card_desc");
            $('.list_card_date').removeClass("list_card_date").addClass("item_card_date");
            $(this).hide()
            $("#my_list_template").show()
        });

});