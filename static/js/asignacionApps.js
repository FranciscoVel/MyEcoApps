document.addEventListener('DOMContentLoaded', function() {
    let counter = 1; // Contador para generar IDs únicos
    let allApplications = []; // Variable para almacenar las aplicaciones

    // Función para obtener todas las aplicaciones desde el backend
    function fetchApplications() {
        fetch('/getAplicaciones')
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error('Error al obtener las aplicaciones:', data.error);
                } else {
                    allApplications = data.aplicaciones;  // Guardar aplicaciones
                    populateDropdown('appSeleccion1', allApplications);
                }
            })
            .catch(error => console.error('Error:', error));
    }

    // Función para llenar el dropdown con aplicaciones
    function populateDropdown(selectId, aplicaciones, excludeApps = []) {
        const select = document.getElementById(selectId);
        if (!select) return;

        // Limpiar el contenido actual del dropdown
        select.innerHTML = '';

        // Agregar las opciones disponibles, excluyendo las seleccionadas
        aplicaciones.forEach(app => {
            if (!excludeApps.includes(String(app.IDAPP))) {
                const option = document.createElement('option');
                option.value = app.IDAPP;
                option.textContent = app.NOMBRE;
                select.appendChild(option);
            }
        });

        // Actualizar el estado del botón después de llenar el dropdown
        checkAddButtonStatus();
    }

    // Función para agregar un nuevo dropdown dinámicamente
    function addDropdown() {
        const container = document.getElementById('appContainer');
        if (!container) return;

        // Clonar el primer elemento de lista desplegable
        const originalSelect = container.querySelector('.mb-3');
        const newSelect = originalSelect.cloneNode(true);

        counter++;  // Incrementar el contador para IDs únicos

        // Actualizar el ID del nuevo select
        const newSelectElement = newSelect.querySelector('select');
        newSelectElement.setAttribute('id', `appSeleccion${counter}`);

        // Agregar el nuevo select al contenedor
        container.appendChild(newSelect);

        // Llenar el nuevo select, excluyendo las aplicaciones ya seleccionadas
        const selectedApps = getSelectedApplications();
        populateDropdown(`appSeleccion${counter}`, allApplications, selectedApps);

        // Deshabilitar los dropdowns existentes, exceptuando el nuevo
        disablePreviousDropdowns();
    }

    // Función para obtener las aplicaciones seleccionadas en los dropdowns actuales
    function getSelectedApplications() {
        const selects = document.querySelectorAll('select');
        const selectedApps = Array.from(selects).map(select => select.value).filter(value => value !== '');
        return [...new Set(selectedApps)]; // Usar Set para valores únicos
    }

    // Función para verificar si el botón de agregar debe estar habilitado
    function checkAddButtonStatus() {
        const selectedApps = getSelectedApplications();
        const addButton = document.getElementById('addButton');
        if (!addButton) return;

        // Deshabilitar el botón si el número de aplicaciones seleccionadas es igual al total de aplicaciones
        if (selectedApps.length >= allApplications.length ) {
            addButton.disabled = true;
        } else {
            addButton.disabled = false;
        }
    }

    // Función para deshabilitar los dropdowns existentes, exceptuando el último
    function disablePreviousDropdowns() {
        const selects = document.querySelectorAll('select');
        selects.forEach((select, index) => {
            // Habilitamos el último select (el más reciente) y deshabilitamos los anteriores
            if (index < selects.length - 1) {
                select.disabled = true; // Deshabilitar todos menos el último
            } else {
                select.disabled = false; // Asegurarse de que el último permanezca habilitado
            }
        });
    }
    

    // Evento para agregar un nuevo dropdown
    const addButton = document.getElementById('addButton');
    if (addButton) {
        addButton.addEventListener('click', addDropdown);
    }   
    
    // Cargar las aplicaciones al cargar la página
    fetchApplications();
});

function enviarAplicacionesSeleccionadas() {
    const selects = document.querySelectorAll('select');
    const aplicacionesSeleccionadas = Array.from(selects).map(select => {
        const selectedOption = select.options[select.selectedIndex];
        return {
            IDAPP: selectedOption.value,
            NOMBRE: selectedOption.textContent
        };
    }).filter(app => app.IDAPP); // Filtrar opciones no seleccionadas

    fetch('/asignarAplicaciones', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            aplicaciones: aplicacionesSeleccionadas
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Aplicaciones asignadas correctamente.');
            // Redirigir solo después de que la asignación sea exitosa
            window.location.href = "/registroUsuario";
        } else {
            alert('Error al asignar aplicaciones.');
        }
    })
    .catch(error => console.error('Error:', error));
}

// Añadir el evento al botón "Asignar"
document.addEventListener('DOMContentLoaded', function() {
    const asignarButton = document.getElementById('asignarButton');
    if (asignarButton) {
        asignarButton.addEventListener('click', enviarAplicacionesSeleccionadas);
    }
});
