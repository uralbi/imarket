$(document).ready(function(){
    var $nm = 0
    var $nav_h = 40
    var $foot_h = $('footer').height() + $nm;
    var $height = $(window).height();
    var $adj_height = $height - $nav_h - $foot_h
    $("#dynamic_height").innerHeight($adj_height)

    $(window).resize(function(){
        var $foot_h = $('footer').height() + $nm;
        var $height = $(window).height();
        var $adj_height = $height - $nav_h - $foot_h
        $("#dynamic_height").innerHeight($adj_height)
    });
});

$(document).ready(function(){
    var $nm = 68
    var $foot_h = $('footer').height() + $nm;
    var $height = $(window).height();
    var $adj_height = $height - 72 - $foot_h
    $("#dynamic_min_height").css("min-height",$adj_height)

    $(window).resize(function(){
        var $foot_h = $('footer').height() + $nm;
        var $height = $(window).height();
        var $adj_height = $height - 72 - $foot_h
        $("#dynamic_min_height").css("min-height",$adj_height)
    });
});

$(document).ready(function(){
    $(".page-link").css("padding", '2px 12px');
    $(".page-link").css("color", '#4080bf');
    $(".page-link").first().css("border-top-left-radius", '20px');
    $(".page-link").first().css("border-bottom-left-radius", '20px');
    $(".page-link").last().css("border-top-right-radius", '20px');
    $(".page-link").last().css("border-bottom-right-radius", '20px');

    $(".page-link").hover(
        function(){
        $(this).css("background", '#206020');
        $(this).css("color", '#ecf9ec');
        },
        function(){
        $(this).css("background", '')
        $(this).css("color", '#4080bf')
    });

    $(".page-item").addClass('my_shadow');
    $(".page-item").first().css("border-top-left-radius", '25px');
    $(".page-item").first().css("border-bottom-left-radius", '25px');
    $(".page-item").last().css("border-top-right-radius", '25px');
    $(".page-item").last().css("border-bottom-right-radius", '25px');
 });


