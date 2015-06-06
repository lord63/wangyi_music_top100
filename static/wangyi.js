$('.badge').on('click', function() {
    var trs = $('tr');
    for (var i = 1; i < trs.length; i++) {
        if (trs.eq(i).children().last().text().indexOf($(this).text()) === -1) {
            trs.eq(i).empty();
        }
    }
});