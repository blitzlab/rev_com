$(document).ready(function(){



  // $('.faq-answer').hide();
  // $("#get_referal_link").click(function(){
  //   var url = $(this).attr("data-url");
  //   // alert($(this).attr("data-username"));
  //   $.ajax({
  //     type: 'GET',
  //     url: url,
  //     data:{ username: $(this).attr("data-username") },
  //     // dataType: "JSON",
  //     success: function (response) {
  //       // var data = JSON.parse(response)
  //       // console.log(response.reflink)
  //       $(".modal-body > p:first").text(response.reflink)
  //       $('.modal').modal('toggle');
  //     },
  //     error: function (response) {
  //       // alert the error if any error occured
  //       // alert(response["responseJSON"]["error"]);
  //     }
  //   });
  //
  // });
  //
  // $("#contact-form").submit(function(e){
  //   e.preventDefault();
  //   $("#contact-sub").prop( "disabled", true);
  //   var csrftoken = $("input[name=csrfmiddlewaretoken]").val();
  //   console.log("Form");
  //   $.ajax({
  //     type: 'POST',
  //     url: "/contact-form/",
  //     // contentType: "application/x-www-form-urlencoded",
  //     headers:{
  //       "X-CSRFToken": csrftoken
  //     },
  //     data: $("#contact-form").serialize(),
  //     success: function (response) {
  //       // var data = JSON.parse(response)
  //       console.log(response.status);
  //       $("#contact").addClass("alert alert-success");
  //       $("#contact > span:first").text(response.message);
  //     },
  //     error: function (error) {
  //       console.log("error occoured");
  //       console.log(error);
  //       // alert the error if any error occured
  //       // alert(response["responseJSON"]["error"]);
  //     }
  //   });
  // });
  //
  // $(".faq").click(function(){
  //   // $('.faq-answer').show();
  //   $(this).next(".faq-answer").toggle();
  // });
  //
  // $(".like").click(function(){
  //   // alert("liked");
  //
  //   $.ajax({
  //     type: 'GET',
  //     url: "/blog-like/",
  //     data:{ blog_slug: $(this).attr("data-blog_slug") },
  //     success: function (response) {
  //       // console.log(response);
  //       if(response.liked){
  //         $(".like").attr("src", "/static/images/vector/like.svg");
  //         $(".like").next("span").html(response.all_like);
  //       }else {
  //         alert("Please login to like a post");
  //       }
  //     },
  //     error: function (response) {
  //       // alert the error if any error occured
  //       // alert(response["responseJSON"]["error"]);
  //     }
  //   });
  // });
  $("#recover-password").click(function(e){
    e.preventDefault();
    if($("#auth-form").valid()){
      $(this).attr("disabled",true);
      const csrftoken = $("input[name=csrfmiddlewaretoken]").val();
      $.ajax({
        method: 'POST',
        url: "/forgotpasswordajax/",
        headers:{
          "X-CSRFToken": csrftoken
        },
        data: {email:$("#recoverEmail").val()},
        success: function (response) {
            let alert = $("#pass-reset-notify").addClass("alert alert-soft-info");
            alert.html("Check your email inbox or spam for password reset link");
        },
        error: function (error) {
          if(error.status == 400){
            let alert = $("#pass-reset-notify").addClass("alert alert-soft-warning");
            alert.html("Unknown email");
          }
          // alert the error if any error occured
          // alert(response["responseJSON"]["error"]);
        }
      });
    }

  });

  $("#ajax-signup-submit").click(function(e){
    e.preventDefault()
    if($("#ajax-signup").valid()){
      $("#ajax-signup-submit").attr("disabled",true);
      const csrftoken = $("input[name=csrfmiddlewaretoken]").val();
      $.ajax({
        method: 'POST',
        url: "/signupajax/",
        headers:{
          "X-CSRFToken": csrftoken
        },
        data: $("#ajax-signup").serialize(),
        success: function (response) {
            let alert = $("#signup-message").addClass("alert alert-soft-info");
            alert.html("Check your email inbox or spam verification link");
        },
        error: function (error) {
          if(error.status == 400){
            let alert = $("#signup-message").addClass("alert alert-soft-warning");
            alert.html("User not registered");
            // console.log("error")
          }
        }
      });
    }
  });

  $("#ajax-login-btn").click(function(e){
    e.preventDefault();
    if($("#ajax-login").valid()){
      $(this).attr("disabled",true);
      const csrftoken = $("input[name=csrfmiddlewaretoken]").val();
      $.ajax({
        method: 'POST',
        url: "/ajaxlogin/",
        headers:{
          "X-CSRFToken": csrftoken
        },
        data: $("#ajax-login").serialize(),
        success: function (response) {
            let alert = $("#login-message").addClass("alert alert-soft-success");
            alert.html("Login successful");
            setTimeout(function(){ window.location=`profile/${response.userid}/`;}, 3000);
            console.log(response);
        },
        error: function (error) {
          if(error.status == 400){
            let alert = $("#login-message").addClass("alert alert-soft-warning");
            alert.html("Invalid login details");
            // console.log("error")
          }
        }
      });
    }
  })
});
