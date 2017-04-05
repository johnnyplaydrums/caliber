$(function() {
    setInterval(function() {
      $.ajax({
        type: 'get',
        url: 'http://34.205.150.122/get_data',
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
