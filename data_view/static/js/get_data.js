$(function() {
    setInterval(function() {
        $.ajax({
            type: 'get',
            url: '/get_data',
            dataType: 'json'
        })
        .done(function(response) {
            console.log(response)
            update_view(response);
        })
        .always(function() {
            console.log('data received');
        });
    }, 5000);

    function update_view(data) {
        var recent = data.recent,
            worst = data.worst,
            column$ = $('<div>'),
            line,
            num,
            i;

        for (var i = 0; i < recent.length; i++) {
            num = i + 1
            line = $('<div class="line">').text(
                num +  '. ' +
                recent[i].address + ' : ' + recent[i].updated_at + ' : ' +
                recent[i].mean + ' : '  + recent[i].rating
            )
            column$.append(line)
        }

        $('#recent').html(column$);

        column$ = $('<div>');
        for (var i = 0; i < worst.length; i++) {
            num = i + 1
            line = $('<div class="line">').text(
                num +  '. ' +
                worst[i].address + ' : ' + worst[i].updated_at + ' : ' +
                worst[i].mean + ' : '  + worst[i].rating
            )
            column$.append(line)
        }

        $('#worst').html(column$);
    }
});
