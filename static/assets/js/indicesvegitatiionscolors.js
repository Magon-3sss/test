function updateColorTable() {
    const selectElement = document.getElementById('filtre-select');
    const selectedFilter = selectElement.value;
    const tableContainer = document.getElementById('color-reference-table');

    // Si un filtre est sélectionné, afficher le tableau
    if (selectedFilter) {
        fetch(`/get-colors?filter=${selectedFilter}`)
            .then(response => response.json())
            .then(data => {
                const table = document.getElementById('reference-table');
                table.innerHTML = ''; // Clear existing table contents

                data.colors.forEach(color => {
                    const row = table.insertRow();
                    const colorCell = row.insertCell(0);
                    const valueCell = row.insertCell(1);
                    
                    const descCell = row.insertCell(2);

                    valueCell.textContent = color.value;
                    colorCell.style.backgroundColor = color.color_css;
                    colorCell.classList.add('color-cell'); // Ajoutez cette ligne
                    descCell.textContent = color.description;
                });

                // Afficher le tableau une fois les données ajoutées
                tableContainer.classList.remove('hidden');
            });
    } else {
        // Si aucun filtre n'est sélectionné, masquer le tableau
        tableContainer.classList.add('hidden');
    }
}