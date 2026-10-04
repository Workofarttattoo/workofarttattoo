(function () {
  var codes = [116,104,101,119,104,105,116,101,107,110,105,103,104,116,55,48,50,64,103,109,97,105,108,46,99,111,109];
  function address() {
    var out = "";
    for (var i = 0; i < codes.length; i++) out += String.fromCharCode(codes[i]);
    return out;
  }
  document.addEventListener("click", function (event) {
    var node = event.target && event.target.closest ? event.target.closest("[data-woa-email-us]") : null;
    if (!node) return;
    event.preventDefault();
    window.location.href = "mailto:" + address();
  });
})();
