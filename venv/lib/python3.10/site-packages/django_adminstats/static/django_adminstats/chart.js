document.addEventListener('DOMContentLoaded', function() {
    var chartElement = document.getElementById('chart');
    var dataElement = document.getElementById('chart-data');
    if (!chartElement) {
        var content = document.getElementById('content-main');
        chartElement = document.createElement('div');
        chartElement.id = 'chart';
        content.insertBefore(chartElement, dataElement);
    }
    // set up axis
    var axisCells = dataElement.querySelectorAll('#chart-axis th[scope=col]');
    var columns = [];
    var hasAxis = false;
    if (axisCells.length) {
        var axixRow = ['_axis'];
        for (var idx = 0; idx < axisCells.length; idx++) {
            axixRow.push(axisCells[idx].dataset.value);
        }
        columns.push(axixRow)
        hasAxis = true;
    }
    var lines = dataElement.querySelectorAll('.chart-line');
    for (var idx = 0; idx < lines.length; idx++) {
        var label = lines[idx].querySelector('th');
        var cells = lines[idx].querySelectorAll('td');
        var row = [label.textContent];
        for (var jdx = 0; jdx < cells.length; jdx++) {
            row.push(cells[jdx].textContent);
        }
        columns.push(row);
    }
    opts = {
        bindto: chartElement,
        data: {
            columns: columns,
            type: dataElement.dataset.chartType,
            onclick: function (d, _) {
                // d.index corresponds to the table row when 1-d and
                // the table column when 2-d,
                // let's see if we find a link
                if (hasAxis) {
                    if (axisCells.length > d.index){
                        var labelLink = axisCells[d.index].querySelector(':link');
                        if (labelLink) {
                            window.location = labelLink.href;
                        }
                    }
                } else {
                    var tableRow = lines[d.index];
                    var labelLink = tableRow.querySelector('th :link');
                    if (labelLink) {
                        window.location = labelLink.href;
                    }
                }
            },
        },
    };
    if (hasAxis) {
        opts['data']['x'] = '_axis';
        opts['data']['xFormat'] = '%Y-%m-%dT%H:%M:%S';
        opts['axis'] = {
               x: {
                type: 'timeseries',
                label: { text: 'Time'}
            }
        };
    }

    var chart = c3.generate(opts);
});
