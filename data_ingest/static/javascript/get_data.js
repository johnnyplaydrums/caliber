$(function() {
    setInterval(function() {
      $.ajax({
        type: 'get',
        url: 'http://monitorcaliber.com/get_data',
        dataType: "json"
      })
      .done(function(response) {
        console.log(response);
        $("#data").append(response);
        $("#data").append('<br>');
      })
      .always(function() {
        console.log("data received");
      });
    }, 5000);
});
