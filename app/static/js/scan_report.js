$(document).ready(function() {
    var socket = io();
    var sortOrder = {}; // Objet pour stocker l'ordre de tri pour chaque colonne

    // Initialiser le tableau vide et décocher toutes les checkboxes
    $('tbody').empty();
    $('input[type=checkbox]').prop('checked', false);

    // Écouter les changements sur les checkboxes
    $('input[type=checkbox]').change(function() {
        var selectedFranchises = $('input[type=checkbox]:checked').map(function() {
            return $(this).val();
        }).get();

        socket.emit('update_table', { franchises: selectedFranchises });
    });

    socket.on('table_updated', function(response) {
        console.log('Received scan reports:', response.scan_reports);  // Debugging line
        // Mettre à jour le tableau avec les nouvelles données
        $('tbody').empty();
        response.scan_reports.forEach(function(report) {
            var tr = $('<tr>').append($('<td class="franchise-column">').text(report.franchise));
            tr.append($('<td>').text(report.Harvester_ID));
            tr.append($('<td>').text(report.Scan_Date));
            var detailsTd = $('<td>');
            var ul = $('<ul>');
            report.entries.forEach(function(entry) {
                var li = $('<li>').text('IP: ' + entry.ip + ', Nom d\'Hôte: ' + entry.nom_hote + ', Ports Ouverts: ' + entry.ports_ouverts.join(', '));
                ul.append(li);
            });
            detailsTd.append(ul);
            tr.append(detailsTd);
            $('tbody').append(tr);
        });
    });

    // Fonction pour trier les données
    function sortTable(columnIndex, order) {
        var rows = $('tbody tr').get();
        rows.sort(function(a, b) {
            var A = $(a).children('td').eq(columnIndex).text().toUpperCase();
            var B = $(b).children('td').eq(columnIndex).text().toUpperCase();
            return (A < B ? -1 : A > B ? 1 : 0) * (order === 'asc' ? 1 : -1);
        });
        $.each(rows, function(index, row) {
            $('tbody').append(row);
        });
    }

    // Écouter les clics sur les têtes de colonnes pour trier les données
    $('th').click(function() {
        var columnIndex = $(this).index();
        var order = sortOrder[columnIndex] === 'asc' ? 'desc' : 'asc';
        sortOrder[columnIndex] = order;
        sortTable(columnIndex, order);

        // Mettre à jour les icônes de tri
        $('th').removeClass('sorted-asc sorted-desc');
        $('th .sort-icon').removeClass('fa-sort-up fa-sort-down').addClass('fa-sort');
        $(this).addClass(order === 'asc' ? 'sorted-asc' : 'sorted-desc')
               .find('.sort-icon').removeClass('fa-sort')
               .addClass(order === 'asc' ? 'fa-sort-up' : 'fa-sort-down');
    });
});