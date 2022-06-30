(function($) {
    function findField(name, fieldType, parent=null) {
        var spec = '.field-' + name + ' ' + fieldType;
        if (parent===null) return $(spec);
        return parent.find(spec);
    }

    function findFieldRow(name, parent=null) {
        var spec = '.field-' + name;
        if (parent===null) return $(spec);
        return parent.find(spec);
    }

    function selectUntilType(elem) {
        var opt = elem.options[elem.selectedIndex];
        findFieldRow('until_date').toggle(opt.value == 's');
    }

    function initAutocomplete(autocomplete) {
        // find the stats selector
        var row = $(autocomplete).closest('.form-row');
        var statsSelector = row.find('.field-stats_key select')[0];
        var opts = {'ajax': {
            url: autocomplete.dataset['ajax-Url'],
            data: function(params) {
                return { term: params.term, page: params.page }; },
            transport: function (params, success, failure) {
                params.url = params.url + statsSelector.value;
                var $request = $.ajax(params);
                $request.then(success);
                $request.fail(failure);
                return $request;
            },
        }};
        $(autocomplete).select2(opts).on(
            'select2:unselecting',
            // work-around for issue #3320 in select2
            function (e) {
                // make sure we are on the list and not within input box
                if (e.params._type === 'unselecting') {
                    $(this).val([]).trigger('change');
                    e.preventDefault();
                }
        });
    }

    $(function() {
        // Initialize all autocomplete widgets except the one in the template
        // form used when a new formset is added.
        var acs = document.querySelectorAll('.adminstats-autocomplete');
        for (var idx=0; idx<acs.length; idx++) {
            initAutocomplete(acs[idx]);
        }

        // Hide Until date if Until type is not "Specific Date"
        var untilTypeField = findField('until_type', 'select');
        untilTypeField.on('change', function() {selectUntilType(this)});
        selectUntilType(untilTypeField[0]);
    });

    $(document).on('formset:added', function() {
        // go through criteria entries and set up autocomplete URLs
        var acs = this.querySelectorAll('.adminstats-autocomplete');
        for (var idx=0; idx<acs.length; idx++) {
            initAutocomplete(acs[idx]);
        }
    });
})(django.jQuery)
