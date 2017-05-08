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
            list$ = $('<ol class="list">'),
            list_item,
            i;

        for (var i = 0; i < recent.length; i++) {
            color = get_color(recent[i].rating);
            list_item = $('<li class="item">').append(
                recent[i].address + ' : ' + recent[i].updated_at,
                $('<br>'),
                recent[i].mean + ' : ',
                $('<span>').css('color', color).append(recent[i].rating)
            )

            list$.append(list_item);

        }

        column$.append(list$)
        $('#recent').html(column$);

        column$ = $('<div>');
        list$ = $('<ol class="list">');
        for (var i = 0; i < worst.length; i++) {
            color = get_color(worst[i].rating);
            list_item = $('<li class="item">').append(
                worst[i].address + ' : ' + worst[i].updated_at,
                $('<br>'),
                worst[i].mean + ' : ',
                $('<span>').css('color', color).append(worst[i].rating)
            )

            list$.append(list_item);
        }

        column$.append(list$);
        $('#worst').html(column$);
    }

    function get_color(rating) {
        if (rating === 'Good') {
            return 'green'
        } else if (rating === 'Fair') {
            return 'orange'
        } else if (rating === 'Bad') {
            return 'red'
        }
    }
});
