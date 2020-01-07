function fn1() {
  var ajax = new XMLHttpRequest();
  // 第二步： 设置状态监听函数
  ajax.onreadystatechange = function() {
    // 第五步：在监听函数中，判断readyState=4 && status=200表示请求成功
    if (ajax.readyState == 4 && ajax.status == 200) {
      // 第六步： 使用responseText、responseXML接受响应数据，并使用原生JS操作DOM进行显示
      js1 = JSON.parse(ajax.responseText);
      // console.log(js1.code);

      if (js1.code === 0) {
        alert("提示:您的账号在其他地方登录，若非本人操作，请立刻修改密码。");
        window.location = "/accounts/logout/?" + "o=1";
        // console.log(JSON.parse(ajax.responseText));
      } else if (js1.code === 2) {
        console.log(11111);
        if (document.querySelector("#code2")) {
          document.querySelector("#code2").className =
            "alert alert-warning alert-dismissible show";
        }
        confirm("不支持单一账号多浏览器登录");
        window.location = "/accounts/logout/?" + "o=1";
      } else {
        if (document.querySelector("#code2")) {
          document.querySelector("#code2").className =
            "alert alert-warning alert-dismissible hidden";
        }
      }
    }
  };
  // 第三步： open一个链接
  ajax.open("GET", "/catalog/isthatone/", true); //true异步请求，false同步

  // 第四步： send一个请求。 可以发送对象和字符串，不需要传递数据发送null
  ajax.send(null);
}
fn1();
