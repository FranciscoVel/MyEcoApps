// Función para buscar usuario y mostrar aplicaciones
function buscarUsuarioBD() {
    const registro = document.getElementById('buscarRegistro').value;

    fetch('/buscarUsuario', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ registro: registro, usuario: true })
    })
    .then(response => response.json())
    .then(data => {
        if (data.mensaje) {
            // Mostrar mensaje de error si existe
            mostrarMensaje(data.mensaje);
        } else {
            // Mostrar aplicaciones si no hay mensaje de error
            mostrarAplicaciones(data.APLICACIONES, data.NOMBRE);
        }
    })
    .catch(error => console.error('Error:', error));

    return false; // Evita la recarga de página
}

// Función para mostrar las tarjetas de aplicaciones
function mostrarAplicaciones(aplicaciones, nombre_usuario) {

    // Convertir solo la primera letra en mayúscula y el resto en minúsculas
    const nombreFormateado = nombre_usuario.charAt(0).toUpperCase() + nombre_usuario.slice(1).toLowerCase();

    // Actualizar el título con el nombre del usuario formateado
    const tituloElement = document.getElementById('tituloAplicaciones');
    tituloElement.textContent = `Tus Aplicaciones ${nombreFormateado}`;
    
    const aplicacionesRow = document.getElementById('aplicacionesRow');
    aplicacionesRow.innerHTML = ''; // Limpiar el contenedor

    aplicaciones.forEach(app => {
        const card = `
            <div class="col-sm-6 col-md-4 col-lg-3">
                <div class="card border-dark h-100" data-id="${app.IDAPP}">
                    <img src="${app.IMAGEN}" class="card-img-top" alt="${app.NOMBRE}">
                    <div class="card-body card-body-center texto-negro">
                        <h5 class="card-title card-title-center">${app.NOMBRE}</h5>
                        <p class="card-text">Descarga el archivo para instalación</p>
                        <a href="${app.RUTA}" class="btn btn-outline-success descargar-btn" data-idapp="${app.IDAPP}">Descargar</a>
                    </div>
                </div>
            </div>
        `;
        aplicacionesRow.insertAdjacentHTML('beforeend', card);
    });

    // Agregar eventos de click a los botones de descarga después de generar las tarjetas
    descargarAplicacion();
}

// Función para agregar eventos de descarga al boton y desvincular la app del usuario
function descargarAplicacion() {
    const botonesDescarga = document.querySelectorAll('.descargar-btn');
    botonesDescarga.forEach(boton => {
        boton.addEventListener('click', (event) => {
            event.preventDefault(); // Evita que la página se recargue inmediatamente
            const idApp = boton.getAttribute('data-idapp');
            alert(`ID de la app: ${idApp}`);
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
                    window.location.href = boton.getAttribute('href');


                    //buscarUsuarioBD(); ACTIVARLO SI SE DESEA QUE APNEAS SE DESCARGUE SE ACTUALICEN LAS APLICACIONES
                } else {
                    alert('Error al descargar la aplicacion. Problema en la Base de Datos');
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
