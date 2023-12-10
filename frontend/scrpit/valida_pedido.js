function validarFormulario() {
    var nombre = document.getElementById("nombre").value;
    var apellido = document.getElementById("apellido").value;
    var telefono = document.getElementById("telefono").value;
    var email = document.getElementById("Email").value;
    var tipoPedido = document.getElementById("tipo_pedido").value;
    var cantidad = document.getElementById("cantidad").value;
    var fechaEntrega = document.getElementById("fecha_entrega").value;
    
    if (nombre.trim() === '' || apellido.trim() === '' || telefono.trim() === '' || email.trim() === '' || tipoPedido.trim() === '' || cantidad.trim() === '' || fechaEntrega.trim() === '') {
        alert("Por favor, complete todos los campos.");
        return false;
    }
    return true; 
}