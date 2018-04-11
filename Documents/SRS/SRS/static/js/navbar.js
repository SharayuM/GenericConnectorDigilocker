  $(document).ready(function() {
    $("#SignUpBtn").click(function() {
      $("#SignUp").modal();
    });
  });
  $(document).ready(function() {
    $("#SignInBtn").click(function() {
      $("#SignIn").modal();
    });
  });
  $(document).ready(function() {
    $("#signupsubmit").click(function() {
var a=document.getElementById("Sign_Up").elements[1].value;
        var b=document.getElementById("Sign_Up").elements[2].value;
        var c=document.getElementById("Sign_Up").elements[3].value;
        var d=document.getElementById("Sign_Up").elements[4].value;
        if (a==null || a=="",b==null || b=="",c==null || c=="",d==null || d=="")
        {
            alert("Please Fill All Required Field");
            return false;
        }

        else
            {
                var email = document.getElementById("Sign_Up").elements[1].value;
        var passwd = document.getElementById("Sign_Up").elements[2].value;
        var mobile = document.getElementById("Sign_Up").elements[4].value;
        var arg;
        arg = '{"Email":"' + email + '","Password":"' + passwd + '","Mobile":"' + mobile + '"}';
        arg = JSON.parse(arg);
        $.ajax({
            type: "POST",
            url: "/signup",
            data: arg,
            async: false,
            success: function (data) {

                $("#otp").modal();
            },
            error: function (data) {
                alert("Some error occured.");
            }
        });
    }
    }



    );

    });

