$(function() {
    setInterval(function() {
      $.ajax({
        type: 'get',
        url: '/get_data',
        dataType: "json"
      })
      .done(function(response) {
        console.log(response);
      })
      .always(function() {
        console.log("data received");
      });
    }, 5000);
});
