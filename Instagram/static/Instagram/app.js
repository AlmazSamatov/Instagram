$(".like").click(function () {

   var elem = this;
   var index = $(".like").index(elem);

   $.ajax({
       type: 'POST',
       url: 'like/',
       data: {
           path: $(".img").eq(index).attr("src"),
           csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
       },
       success: function( result ) {
           if (result["is_liked"]){
               $(elem).attr('src', 'static/Instagram/like_void.png');
           }
           else {
               $(elem).attr('src', 'static/Instagram/like.png');
           }
           $(".amount_of_likes").eq(index).html( result["amount_of_likes"] + " likes");
       }
   });

});

$(".comment_type_form").keyup(function(e) {
    if (e.which === 13) {
        var elem = this;
        var index = $(".comment_type_form").index(elem);
        var comment = $(".comment_type_form").eq(index).val();

        $.ajax({
            type: 'POST',
            url: 'leave_comment/',
            data: {
                path: $(".img").eq(index).attr("src"),
                comment: comment,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function( result ) {
                $(".comment_type_form").eq(index).val("");
                var string = "<div class='comments'> <a class=\"font-weight-bold\">" + result['user'] +
                    "</a> <a class=\"font-weight-normal text-secondary\">"  +
                    result['comment'] + "</a> </div> <div class=\"delete_comment\"> <a>&times</a> </div>";
                $(string).appendTo($(".comments-form").eq(index));
            }
        });
    }
});


$(document).on("click", ".delete_comment", function () {

   var elem = this;
   var index = $(".delete_comment").index(elem);
   console.log($(elem).prev().find(".comment").html());

   $.ajax({
       type: 'POST',
       url: 'delete_comment/',
       data: {
           path: $(elem).parent().siblings(".img").attr("src"),
           comment: $(elem).prev().find(".comment").html(),
           csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
       },
       success: function( result ) {
            if (result['success']){
                $(elem).prev().attr('style', 'display:none');
                $(elem).attr('style', 'display:none');
            }
       }
   });

});
