function buscarUsuarioBD() {
    const registro = document.getElementById('buscarRegistro').value;

    fetch('/buscarUsuario', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ registro: registro, usuario: false })
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
        
        if (data.mensaje) {
            document.getElementById('informacionUsuario').innerText = data.mensaje;
            btnAsignarApps.classList.add('disabled');
            btnDesvincularApps.classList.add('disabled');
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
                ${aplicacionesHtml}
            `;

            btnAsignarApps.classList.remove('disabled');
            btnDesvincularApps.classList.remove('disabled');
        } else {
            document.getElementById('informacionUsuario').innerText = 'Error al buscar el usuario.';
            btnAsignarApps.classList.add('disabled');
            btnDesvincularApps.classList.add('disabled');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('informacionUsuario').innerText = 'Error al buscar el usuario.';
        const btnAsignarApps = document.getElementById('btnAsignarApps');
        const btnDesvincularApps = document.getElementById('btnDesvincularApps');
        btnAsignarApps.classList.add('disabled');
        btnDesvincularApps.classList.add('disabled');
    });

    return false; // Evita la recarga de página
}
