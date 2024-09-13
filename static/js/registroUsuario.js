function buscarUsuario() {
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
        return response.text(); // Lee la respuesta como texto
    })
    .then(text => {
        try {
            const data = JSON.parse(text); // Intenta convertir el texto a JSON
            if (data.error) {
                document.getElementById('informacionUsuario').innerText = data.error;
            } else {
                document.getElementById('informacionUsuario').innerHTML = `
                    <strong>ID:</strong> ${data.IDUSER}<br>
                    <strong>Nombre:</strong> ${data.NOMBRE}<br>
                    <strong>Correo:</strong> ${data.CORREO}<br>
                    <strong>Rol:</strong> ${data.ROL}<br>
                    <strong>Registro:</strong> ${data.REGISTRO}
                `;
            }
        } catch (e) {
            document.getElementById('informacionUsuario').innerText = 'Error al procesar la respuesta del servidor.';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('informacionUsuario').innerText = 'Error al buscar el usuario.';
    });

    return false; // Evita la recarga de página
}
