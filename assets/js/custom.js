$(function () {
    $("#id_rate").rating({showCaption: false});
    $(".rating-disabled").each(function (){
        $(this).rating({showCaption: false, disabled: true})
    })
    $('[data-toggle="confirmation"]').confirmation();
});
