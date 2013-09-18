(function ($) {
    $.fn.serializeObject = function () {
        var o = {};
        var a = this.serializeArray();
        $.each(a, function () {
            if (o[this.name] !== undefined) {
                if (!o[this.name].push) {
                    o[this.name] = [o[this.name]];
                }
                o[this.name].push(this.value || '');
            } else {
                o[this.name] = this.value || '';
            }
        });
        return o;
    };
    $.ajaxSettings.traditional = true;
    var cases = {
        'nomn': 'именительный',
        'gent': 'родительный',
        'datv': 'дательный',
        'accs': 'винительный',
        'ablt': 'творительный',
        'loct': 'предложный'
    };
    $(function () {
        $("form").submit(function (e) {
            e.preventDefault();
            var $this = $(this);
            var data = $this.serializeObject();
            $.post($this.prop("action"), data)
                .always(function() {
                   if ($('.panel').length === 0 ) {
                       $('form').append('<hr/>')
                   }
                })
                .done(function (data) {
                    var $result = $("<div class='panel panel-default' />");
                    $result.append($("<div class='panel-heading'/>").text(data.orig));
                    var $body =$("<p class='panel-body'/>");
                    for (var c in data) {
                        if (c != 'orig') {
                            $body.append($("<p/>").text(cases[c] + ": " + data[c]));
                        }
                    }
                    $result.append($body);
                    $this.append($result);
                })
                .fail(function (err) {

                    $this.append($("<div class='panel panel-danger'>" +
                        "<div class='panel-heading'>Ошибка</div>" +
                        "<div class='panel-body'>" + err.responseText + "</div>" +
                        "</div>"));
                });
        });

    });
})(jQuery);
