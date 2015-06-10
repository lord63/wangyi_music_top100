filter = function (items, filter) {
    for (var i = 0; i < items.length; i++) {
        if (items.eq(i).children().last().text().indexOf(filter) === -1) {
            items.eq(i).hide();
        }
    }
};

// Click and filter the songlists.
$('.badge').on('click', function() {
    var trs;
    trs = $('tbody tr:visible');
    if ($('.undo').text().indexOf($(this).text()) === -1) {
        $('thead tr td').last().append('<span class="badge undo"><span>' + $(this).text() + '</span><span class="glyphicon glyphicon-remove-sign"></span></span>');
        filter(trs, $(this).text());
    }
});

// Undo the filter.
$('td').on('click', 'span.undo', function() {
    var i;
    $(this).remove();
    if ($('.undo').length == 0) {
        $('tbody tr').show();
    }
    else {
        $('tbody tr').show();
        for (i=0; i<$('.undo').length; i++) {
            filter($('tbody tr:visible'), $('.undo span').eq(2*i).text());
        }
    }
});