//整个网页加载完毕后执行的函数
function BtnClick()
{
    $("#captchaBtn").click(function(event) {
        var $this = $(this);
        //阻止将表单数据提交到服务器
        event.preventDefault();
        
        var email = $("#email").val();
        
        $.ajax({
            url: "/auth/captcha?email=" + email, 
            method: "GET",
            success: function(result) {
                var code = result['code'];
                if (code == 200)
                {
                    var countdown = 5;
                    $this.off("click");
                    alert("验证码已发送至" + email + "，请查收");
                    var timer = setInterval(function (){
                        $this.text("( "+countdown+" )");
                        countdown--;

                        if (countdown <= 0)
                        {
                            clearInterval(timer);
                            $this.text("获取验证码");
                            BtnClick();
                        }

                    }, 1000);
                    
                }
            },
            fail: function(error) {
                alert("验证码发送失败，请重试");
                console.log(error);
            }
        });
    });
}

$(function() {
    BtnClick();
});