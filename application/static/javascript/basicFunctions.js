function popupLoad() {
  window.on('pageshow', function () {
    var delayMs = 1500; // delay in milliseconds

    setTimeout(function () {
      $('#myModal').modal('show');
    }, delayMs);
  });
}
