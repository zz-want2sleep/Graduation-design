$(function() {
  $(".nav .sidebar-top li").click(function() {
    $(".nav .sidebar-top li")
      .eq($(this).index())
      .addClass("active")
      .siblings()
      .removeClass("active");
  });
  // console.log(location.pathname.substring(0, 14));
  if (location.pathname.substring(0, 16) == "/catalog/author/") {
    $(".li2").addClass("active");
  } else if (location.pathname.substring(0, 14) == "/catalog/book/") {
    $(".li1").addClass("active");
  }
});
// window.onload = function() {
//   document
//     .querySelector(".btn .btn-default")
//     .addEventListener("click", function(e) {
//       e.preventDefault();
//       window.location.href =
//         window.location.pathname +
//         "?page=" +
//         document.querySelector(".form-control").value;
//     });
// };

$(document).ready(function() {
  $("button.btn.btn-default.pagination1").click(function(e) {
    e.preventDefault();
    if (
      Number(
        $(".pages")
          .val()
          .trim()
      ) <
      Number(
        $("#paginator")
          .val()
          .trim()
      )
    ) {
      $(location).attr(
        "href",
        window.location.pathname + "?page=" + $(".pages").val()
      );
    } else {
      $(location).attr(
        "href",
        window.location.pathname +
          "?page=" +
          $("#paginator")
            .val()
            .replace(/[~'!<>@#$%^&*()-+_=:/?]/g, "")
            .trim()
      );
    }
  });
  // ------------
  $("button.authorFilter").on("click", function(e) {
    // console.log(1);
    e.preventDefault();
    if (
      !$("input.form-control.authorFilter")
        .val()
        .replace(/[~'!<>@#$%^&*()-+_=:/?]/g, "")
        .trim()
    ) {
      $(location).attr("href", window.location.pathname);
    } else {
      if (window.location.pathname.lastIndexOf("/") != 18) {
        $(location).attr(
          "href",
          window.location.pathname +
            "s/" +
            $("input.form-control.authorFilter")
              .val()
              .replace(/[~'!<>@#$%^&*()-+_=:/?]/g, "")
              .trim()
        );
      } else {
        $(location).attr(
          "href",
          window.location.pathname.substring(0, 19) +
            $("input.form-control.authorFilter")
              .val()
              .replace(/[~'!<>@#$%^&*()-+_=:/?]/g, "")
              .trim()
        );
      }
    }
  });

  // ------------
  $("button.bookFilter").on("click", function(e) {
    // console.log(1);
    e.preventDefault();
    if (
      !$("input.form-control.bookFilter")
        .val()
        .replace(/[~'!<>@#$%^&*()-+_=:/?]/g, "")
        .trim()
    ) {
      $(location).attr("href", window.location.pathname);
    } else {
      if (window.location.pathname.lastIndexOf("/") != 16) {
        $(location).attr(
          "href",
          window.location.pathname +
            "s/" +
            $("input.form-control.bookFilter")
              .val()
              .replace(/[~'!<>@#$%^&*()-+_=:/?]/g, "")
              .trim()
        );
      } else {
        $(location).attr(
          "href",
          window.location.pathname.substring(0, 17) +
            $("input.form-control.bookFilter")
              .val()
              .replace(/[~'!<>@#$%^&*()-+_=:/?]/g, "")
              .trim()
        );
      }
    }
  });
  // ------------------------
  $("button.bookGenre").on("click", function(e) {
    // console.log(1);
    e.preventDefault();
    if (
      !$("input.form-control.bookGenre")
        .val()
        .replace(/[~'!<>@#$%^&*()-+_=:/?]/g, "")

        .trim()
    ) {
      $(location).attr("href", window.location.pathname);
    } else {
      if (window.location.pathname.lastIndexOf("/") === 14) {
        $(location).attr(
          "href",
          window.location.pathname +
            "/s/" +
            $("input.form-control.bookGenre")
              .val()
              .replace(/[~'!<>@#$%^&*()-+_=:/?]/g, "")
              .trim()
        );
      } else {
        var num = window.location.pathname.lastIndexOf("/") + 1;
        $(location).attr(
          "href",
          window.location.pathname.substring(0, num) +
            $("input.form-control.bookGenre")
              .val()
              .replace(/[~'!<>@#$%^&*()-+_=:/?]/g, "")
              .trim()
        );
      }
    }
  });

  //-------------------------
  $("button.borrowerFilter").on("click", function(e) {
    // console.log(1);
    e.preventDefault();
    if (
      !$("input.form-control.borrowerFilter")
        .val()
        .replace(/[~'!<>@#$%^&*()-+_=:/?]/g, "")
        .trim()
    ) {
      $(location).attr("href", window.location.pathname);
    } else {
      if (window.location.pathname.lastIndexOf("/") != 18) {
        $(location).attr(
          "href",
          window.location.pathname +
            "s/" +
            $("input.form-control.borrowerFilter")
              .val()
              .replace(/[~'!<>@#$%^&*()-+_=:/?]/g, "")
              .trim()
        );
      } else {
        $(location).attr(
          "href",
          window.location.pathname.substring(0, 19) +
            $("input.form-control.borrowerFilter")
              .val()
              .replace(/[~'!<>@#$%^&*()-+_=:/?]/g, "")
              .trim()
        );
      }
    }
  });

  //-----------------------
  $("button.allBorrowerFilter").on("click", function(e) {
    // console.log(1);
    e.preventDefault();
    if (
      !$("input.form-control.allBorrowerFilter")
        .val()
        .replace(/[~'!<>@#$%^&*()-+_=:/?]/g, "")
        .trim()
    ) {
      $(location).attr("href", window.location.pathname);
    } else {
      if (window.location.pathname.lastIndexOf("/") != 19) {
        $(location).attr(
          "href",
          window.location.pathname +
            "s/" +
            $("input.form-control.allBorrowerFilter")
              .val()
              .replace(/[~'!<>@#$%^&*()-+_=:/?]/g, "")
              .trim()
        );
      } else {
        $(location).attr(
          "href",
          window.location.pathname.substring(0, 20) +
            $("input.form-control.allBorrowerFilter")
              .val()
              .replace(/[~'!<>@#$%^&*()-+_=:/?]/g, "")
              .trim()
        );
      }
    }
  });
  // ------------------------------send email
  $("button.send_email").on("click", function(e) {
    e.preventDefault();
    // console.log(1);
    var vals = "";
    if (!$("span.send_email")) {
      $(location).attr("href", window.location.pathname);
    } else {
      $("span.send_email").each(function() {
        // let this = $(this);
        vals += $(this)
          .text()
          .trim();
      });
      console.log(vals);
      $(location).attr("href", "/catalog/send_email/" + vals);
    }
  });
  // // -----------------------------------appointment
  // $("button.appointmentFilter").on("click", function(e) {
  //   e.preventDefault();
  //   // console.log(1);
  //   if (
  //     !$("input.form-control.appointmentFilter")
  //       .val()
  //       .trim()
  //   ) {
  //     // console.log(11);
  //     $(location).attr("href", window.location.pathname);
  //   } else {
  //     // console.log(22);
  //     if (window.location.pathname.lastIndexOf("/") != 25) {
  //       $(location).attr(
  //         "href",
  //         window.location.pathname +
  //           "s/" +
  //           $("input.form-control.appointmentFilter")
  //             .val()
  //             .trim()
  //       );
  //     } else {
  //       $(location).attr(
  //         "href",
  //         window.location.pathname.substring(0, 26) +
  //           $("input.form-control.appointmentFilter")
  //             .val()
  //             .trim()
  //       );
  //     }
  //   }
  // });

  // //-----------------------
  // $("button.allAppointmentFilter").on("click", function(e) {
  //   // console.log(11111111);
  //   // console.log(1);
  //   if (
  //     !$("input.form-control.allAppointmentFilter")
  //       .val()
  //       .trim()
  //   ) {
  //     $(location).attr("href", window.location.pathname);
  //   } else {
  //     if (window.location.pathname.lastIndexOf("/") != 22) {
  //       $(location).attr(
  //         "href",
  //         window.location.pathname +
  //           "s/" +
  //           $("input.form-control.allAppointmentFilter")
  //             .val()
  //             .trim()
  //       );
  //     } else {
  //       $(location).attr(
  //         "href",
  //         window.location.pathname.substring(0, 23) +
  //           $("input.form-control.allAppointmentFilter")
  //             .val()
  //             .trim()
  //       );
  //     }
  //   }
  // });
});

// window.onload = function() {
//   document.querySelector("button.appointmentFilter").click(function(e) {
//     e.preventDefault();
//     if (
//       !document
//         .querySelector("input.form-control.appointmentFilter")
//         .val()
//         .trim()
//     ) {
//       location.href = window.location.pathname;
//     } else {
//       if (window.location.pathname.lastIndexOf("/") != 25) {
//         location.href =
//           window.location.pathname +
//           "s/" +
//           document
//             .querySelector("input.form-control.appointmentFilter")
//             .val()
//             .trim();
//       } else {
//         location.href =
//           window.location.pathname.substring(0, 26) +
//           document
//             .querySelector("input.form-control.appointmentFilter")
//             .val()
//             .trim();
//       }
//     }
//   });
// };
// -----------------------------------
// $(function callbackFun() {
//   $.ajax({
//     url: "/catalog/isthatone/",
//     type: "GET",
//     dataType: "json",
//     success: function(j) {
//       console.log(1);
//       if (j.code === 0) {
//         alert(
//           "下线提示:" + "您的账号在其他地方登录，若非本人操作，请重新登录。"
//         );
//         window.location.href = "/accounts/login/";
//       } else {
//         setTimeout(callbackFun, 1000);
//         //延时递归调用自己,间隔调用时间,单位毫秒这里是每过一秒向后台发送一次请求
//       }
//     }
//   });
// });
// -------------------------------------------returned
$(function() {
  $(".returned").on("click", function(e) {
    var returned = window.confirm("单击“确定”继续还书。单击“取消”停止还书。");
    if (!returned) {
      e.preventDefault();
    }
  });
});
$(function() {
  $(".createauthor").on("click", function(e) {
    // console.log($("#id_date_of_birth").val());
    if ($("#id_date_of_birth").val() && $("#id_date_of_death").val()) {
      if ($("#id_date_of_birth").val() >= $("#id_date_of_death").val()) {
        window.confirm("注意：出生日期一定要小于死亡日期！");
        e.preventDefault();
      }
    }
  });
});
