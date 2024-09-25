
function obtenerUsuarioSession() {
    fetch('/traerUsuarioSession')
        .then(response => response.json())
        .then(data => {
            // Mostrar aplicaciones si no hay mensaje de error
            mostrarAplicaciones(data.APLICACIONES, data.NOMBRE);
        })
        .catch(error => console.error('Error:', error));

        return false;
}

document.addEventListener('DOMContentLoaded', function() {
    obtenerUsuarioSession();
});



// Función para mostrar las tarjetas de aplicaciones
function mostrarAplicaciones(aplicaciones, nombre_usuario) {

    // Convertir solo la primera letra en mayúscula y el resto en minúsculas
    const nombreFormateado = nombre_usuario.toLowerCase().replace(/\b\w/g, (c) => c.toUpperCase());

    // Actualizar el título con el nombre del usuario formateado
    const tituloElement = document.getElementById('tituloAplicaciones');
    tituloElement.textContent = `Desvincular Aplicaciones a: ${nombreFormateado}`;
    
    const aplicacionesRow = document.getElementById('aplicacionesRow');
    aplicacionesRow.innerHTML = ''; // Limpiar el contenedor

    if (aplicaciones.length === 0) {
        // Si la lista de aplicaciones está vacía, mostrar el mensaje de alerta
        const mensaje = `<div class="alert alert-danger" role="alert">No hay aplicaciones disponibles.</div>`;
        aplicacionesRow.insertAdjacentHTML('beforeend', mensaje);
    } else {
        // Si hay aplicaciones, generar las tarjetas
        aplicaciones.forEach(app => {
            const card = `
                <div class="col-sm-6 col-md-4 col-lg-3">
                    <div class="card border-dark h-100" data-id="${app.IDAPP}">
                        <img src="${app.IMAGEN}" class="card-img-top" alt="${app.NOMBRE}">
                        <div class="card-body card-body-center texto-negro">
                            <h5 class="card-title card-title-center">${app.NOMBRE}</h5>
                            <p class="card-text">Presionar el boton para desvincular al usuario de la aplicacion</p>
                            <a href="${app.RUTA}" class="btn btn-outline-success descargar-btn" data-idapp="${app.IDAPP}">Desvincular</a>
                        </div>
                    </div>
                </div>
            `;
            aplicacionesRow.insertAdjacentHTML('beforeend', card);
        });

        // Agregar eventos de click a los botones de descarga después de generar las tarjetas
        desvincularAplicacion();
    }
}


// Función para agregar eventos de descarga al boton y desvincular la app del usuario
function desvincularAplicacion() {
    const botonesDescarga = document.querySelectorAll('.descargar-btn');
    botonesDescarga.forEach(boton => {
        boton.addEventListener('click', (event) => {
            event.preventDefault(); // Evita que la página se recargue inmediatamente
            const idApp = boton.getAttribute('data-idapp');
            fetch('/desvincularApp', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    aplicacion: idApp
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    
                    // Redirigir solo después de que la desvinculacion sea exitosa
                    alert('Aplicacion desvinculada con exito')
                    // Recargar la pagina despues de desvincular la aplicacion 
                    
                    fetch('/recargarUsuario', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ registro: ''})
                    })
                    obtenerUsuarioSession();

                } else {
                    alert('Error al desvincular la aplicacion. Problema en la Base de Datos');
                }
            })
            .catch(error => console.error('Error:', error));
            // Redirigir a la ruta de descarga después de mostrar el ID
            
        });
    });
}

// Función para mostrar un mensaje de error
function mostrarMensaje(mensaje) {
    const aplicacionesRow = document.getElementById('aplicacionesRow');
    aplicacionesRow.innerHTML = `<div class="alert alert-danger" role="alert">${mensaje}</div>`;
}
