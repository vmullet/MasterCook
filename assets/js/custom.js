$(function () {
    $(".rating-no-caption").rating({showCaption: false});
    $(".rating-disabled").rating({showCaption: false, disabled: true});

    $(".btn-confirm").on('click',function() {
        let modal_title = $(this).attr('data-title');
        let modal_message = $(this).attr('data-message');
        let modal_action = $(this).attr('data-action');
        $("#myModal-title").text(modal_title);
        $("#myModal-text").text(modal_message);
        $("#myModal-yes").on('click',function() {
            window.location.href = modal_action;
        });
        $("#myModal").modal('show');
    });
});
