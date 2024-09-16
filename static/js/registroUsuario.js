function buscarUsuarioBD() {
    const registro = document.getElementById('buscarRegistro').value;

    fetch('/buscarUsuario', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ registro: registro })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Convertir la respuesta a JSON
    })
    .then(data => {
        if (data.error) {
            document.getElementById('informacionUsuario').innerText = data.error;
        } else {
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
                ${data.mensaje ? `<strong>Mensaje:</strong> ${data.mensaje}<br>` : ''}
                ${aplicacionesHtml}
            `;
        }
    })   
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('informacionUsuario').innerText = 'Error al buscar el usuario.';
    });

    return false; // Evita la recarga de página
}
