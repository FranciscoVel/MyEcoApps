function redirigir() {
    window.location.href = "/registroUsuario";
}

document.addEventListener('DOMContentLoaded', function() {
    let counter = 1; // Contador para generar IDs únicos

    function addDropdown() {
        // Obtener el contenedor donde se agregarán las nuevas listas desplegables
        const container = document.getElementById('appContainer');
        
        if (!container) {
            console.error('Elemento con id "appContainer" no encontrado');
            return;
        }

        // Clonar el primer elemento de lista desplegable
        const originalSelect = container.querySelector('.mb-3');
        const newSelect = originalSelect.cloneNode(true);

        // Incrementar el contador para cada nuevo elemento
        counter++;
        
        // Asegurarse de que el nuevo elemento tenga un ID único
        const newSelectElement = newSelect.querySelector('select');
        newSelectElement.setAttribute('id', `appSeleccion${counter}`);

        // Añadir el nuevo elemento al contenedor
        container.appendChild(newSelect);
    }

    // Añadir el evento al botón para agregar más listas desplegables
    const addButton = document.getElementById('addButton');
    if (addButton) {
        addButton.addEventListener('click', addDropdown);
    } else {
        console.error('Elemento con id "addButton" no encontrado');
    }
});


