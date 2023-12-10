document.addEventListener('DOMContentLoaded', function () {
    var form = document.getElementById('formulario_contacto');

    form.addEventListener('submit', function (event) {
        var nombre = document.getElementById('nombre').value;
        var email = document.getElementById('email').value;
        var telefono = document.getElementById('celular').value;
        var mensaje = document.getElementById('mensaje').value;

        if (nombre.trim() === '' || mensaje.trim() === '') {
            alert('Por favor, complete los campos obligatorios (nombre y mensaje).');
            event.preventDefault();
            return;
        }

        var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            alert('Por favor, ingrese un correo electrónico válido.');
            event.preventDefault();
            return;
        }

        var telefonoRegex = /^\d{10}$/;
        if (telefono.trim() !== '' && !telefonoRegex.test(telefono)) {
            alert('Por favor, ingrese un número de celular válido (10 dígitos).');
            event.preventDefault();
            return;
        }
    });
});
