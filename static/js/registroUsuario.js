function buscarUsuarioBD() {
    const registro = document.getElementById('buscarRegistro').value;

    fetch('/buscarUsuario', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ registro: registro})
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Convertir la respuesta a JSON
    })
    .then(data => {
        const btnAsignarApps = document.getElementById('btnAsignarApps');
        const btnDesvincularApps = document.getElementById('btnDesvincularApps');
        const btnRegistrarUsuario = document.getElementById('btnRegistrarUsuario')
        
        if (data.mensaje) {
            document.getElementById('informacionUsuario').innerText = data.mensaje;
            btnAsignarApps.classList.add('disabled');
            btnDesvincularApps.classList.add('disabled');
            btnRegistrarUsuario.classList.add('disabled');
        } else if (data.IDUSER || data.NOMBRE || data.CORREO || data.ROL || data.REGISTRO) {
            let aplicacionesHtml = '';
            if (data.APLICACIONES && data.APLICACIONES.length > 0) {
                aplicacionesHtml = '<strong>Aplicaciones:</strong><ul>';
                data.APLICACIONES.forEach(app => {
                    aplicacionesHtml += `<li><strong>Nombre:</strong> ${app.NOMBRE}</li>`;
                });
                aplicacionesHtml += '</ul>';
            }

            document.getElementById('informacionUsuario').innerHTML = `
                ${data.IDUSER ? `<strong>ID:</strong> ${data.IDUSER}<br>` : ''}
                ${data.NOMBRE ? `<strong>Nombre:</strong> ${data.NOMBRE}<br>` : ''}
                ${data.CORREO ? `<strong>Correo:</strong> ${data.CORREO}<br>` : ''}
                ${data.ROL ? `<strong>Rol:</strong> ${data.ROL}<br>` : ''}
                ${data.REGISTRO ? `<strong>Registro:</strong> ${data.REGISTRO}<br>` : ''}
                ${data.directorio ? `<div class="alert alert-danger"><strong>Advertencia:</strong> ${data.directorio}</div>` : ''}
                ${aplicacionesHtml}
            `;

            btnAsignarApps.classList.remove('disabled');
            btnDesvincularApps.classList.remove('disabled');
            btnRegistrarUsuario.classList.add('disabled');
            //Si viene del directorio activo, activar el boton de registrar
            if(data.directorio){
                console.log(data.directorio)
                btnRegistrarUsuario.classList.remove('disabled');
                btnAsignarApps.classList.add('disabled');
                btnDesvincularApps.classList.add('disabled');
            }
            
        } else {
            document.getElementById('informacionUsuario').innerText = 'Error al buscar el usuario.';
            btnAsignarApps.classList.add('disabled');
            btnDesvincularApps.classList.add('disabled');
            btnRegistrarUsuario.classList.add('disabled');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('informacionUsuario').innerText = 'Error al buscar el usuario.';
        const btnAsignarApps = document.getElementById('btnAsignarApps');
        const btnDesvincularApps = document.getElementById('btnDesvincularApps');
        btnAsignarApps.classList.add('disabled');
        btnDesvincularApps.classList.add('disabled');
        btnRegistrarUsuario.classList.add('disabled');
    });

    return false; // Evita la recarga de página
}

//Funcion para registrar usuario de directorio activo a la base de datos
function registrarUsuario() {
    
    fetch('/registrarUsuario', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    })
    .then(response => response.json()) // Procesa la respuesta como JSON
    .then(data => {
        if (data.success) {
            // Si el registro fue exitoso, muestra un alert de éxito
            alert('Usuario registrado con éxito.');
            document.getElementById('btnRegistrarUsuario').classList.add('disabled')
            document.getElementById('btnAsignarApps').classList.remove('disabled')
            document.getElementById('btnDesvincularApps').classList.remove('disabled')

        } else {
            // Si hubo algún error, muestra un alert con el mensaje de error
            alert(`Error: ${data.mensaje}`);
            document.getElementById('btnRegistrarUsuario').classList.remove('disabled')
            document.getElementById('btnAsignarApps').classList.add('disabled')
            document.getElementById('btnDesvincularApps').classList.add('disabled')
        }
    })
    .catch(error => {
        // Maneja errores de la llamada fetch (problemas de red, etc.)
        alert('Error en la solicitud: ' + error);
    });

}

// Agrega el evento al botón
document.getElementById('btnRegistrarUsuario').addEventListener('click', registrarUsuario);
