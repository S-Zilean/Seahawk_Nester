$(document).ready(function() {
    // Initialisation de Socket.IO avec une meilleure gestion des WebSockets
    var socket = io({
        transports: ['websocket', 'polling'],  // Forcer WebSockets
        reconnection: true,                    // Autoriser la reconnexion automatique
        reconnectionAttempts: 5,               // Nombre max de tentatives de reconnexion
        reconnectionDelay: 1000                // Délai entre les tentatives
    });

    var sortOrder = {}; // Stocker l'ordre de tri pour chaque colonne

    // Initialiser le tableau et décocher toutes les checkboxes
    $('tbody').empty();
    $('input[type=checkbox]').prop('checked', false);

    // Écouter les changements sur les checkboxes et envoyer la requête au serveur
    $('input[type=checkbox]').change(function() {
        var selectedFranchises = $('input[type=checkbox]:checked').map(function() {
            return $(this).val();
        }).get();

        socket.emit('update_table', { franchises: selectedFranchises });
    });

    // Réception des données mises à jour et mise à jour du tableau
    socket.on('table_updated', function(response) {
        $('tbody').empty();
        response.harvesters.forEach(function(group) {
            group.data.forEach(function(row) {
                var tr = $('<tr>').append($('<td class="franchise-column">').text(group.franchise));
                row.forEach(function(cell) {
                    tr.append($('<td>').text(cell));
                });
                $('tbody').append(tr);
            });
        });
    });

    // Fonction pour trier les données
    function sortTable(columnIndex, order) {
        var rows = $('tbody tr').get();
        rows.sort(function(a, b) {
            var A = $(a).children('td').eq(columnIndex).text().trim().toUpperCase();
            var B = $(b).children('td').eq(columnIndex).text().trim().toUpperCase();
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

    // Gestion des erreurs WebSocket
    socket.on('connect_error', function(err) {
        console.error("⚠️ Erreur de connexion WebSocket : ", err);
    });

    socket.on('disconnect', function() {
        console.warn("⚠️ WebSocket déconnecté !");
    });

    socket.on('reconnect_attempt', function(attempt) {
        console.log(`🔄 Tentative de reconnexion WebSocket (${attempt}/5)...`);
    });

    socket.on('reconnect_failed', function() {
        console.error("❌ Échec de la reconnexion WebSocket après 5 tentatives.");
    });

    socket.on('connect', function() {
        console.log("✅ WebSocket connecté !");
    });
});
