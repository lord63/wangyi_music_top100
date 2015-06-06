$('.badge').on('click', function() {
        var filted_list, trs;
        filted_list = [];
        trs = $('tr');
        for (var i = 0; i < trs.length; i++) {
            if ($('tr').eq(i).children().last().text().indexOf($(this).text()) !== -1) {
                filted_list.push($('tr').eq(i).html());
            }
        }
        $('tbody').empty();
        for (var j = 0; j < filted_list.length; j++) {
            $('tbody').append('<tr>' + filted_list[j] + '</tr>');
        }
    }
);