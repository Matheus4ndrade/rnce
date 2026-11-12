(function () {
  "use strict";

  var logo = document.getElementById("logo");

  logo.addEventListener("mouseenter", function () {
    logo.classList.remove("go");
    void logo.offsetWidth;
    logo.classList.add("go");
  });
})();
