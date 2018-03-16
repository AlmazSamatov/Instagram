$("#register_btn").click(function () {
   $("#login-form").attr("class", "d-none");
   $("#register-form").removeClass('d-none');
   $("#msg_login").attr("class", "d-none");
   $("#msg_reg").removeClass('d-none');
   document.title = "Register in Instagram";
   return false;
});

$("#login_btn").click(function () {
   $("#login-form").removeClass('d-none');
   $("#register-form").attr("class", "d-none");
   $("#msg_login").removeClass('d-none');
   $("#msg_reg").attr("class", "d-none");
   document.title = "Log in to Instagram";
   return false;
});

