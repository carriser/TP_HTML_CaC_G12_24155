// Validación de datos del formulario

window.addEventListener('load', e=>{
    const formulario = document.getElementById("form");
    const nombre = document.getElementById('nombreApellido');
    const correo = document.getElementById("correoElectronico");
    const telefono = document.getElementById("telefono");
    const mensaje = document.getElementById("mensaje");

    formulario.addEventListener("submit", e=>{
        e.preventDefault();
        validaCampos();
    })

    // capturamos los valores ingresados
    const validaCampos = () => {
       const nombreValor = nombre.value.trim();
       const correoValor = correo.value.trim();
       const telefonoValor = telefono.value.trim();

       // validando campo nombre
       // validando en forma ternaria
       // (!nombreValor || nombreValor.length < 2) ? alert('Nombre vacío o muy corto') : validaOk(nombre)
       
       // validando con if
       if (!nombreValor || nombreValor.length < 2) {
            document.getElementById('nombreApellido').focus();
            alert('Nombre vacío o muy corto');
            e.stopPropagation();
       }

       // validando campo correo electrónico
        if (document.getElementById('radio-email').checked) {
            if (!correoValor) {
                document.getElementById('correoElectronico').focus();
                alert('Si el contacto es por email ingrese su dirección de correo electrónico');
            } 
        }

        if (correoValor && !validaEmail(correoValor)) {
            alert('La dirección de correo electrónico no es válida');
        }

        // validando campo teléfono
        if (document.getElementById('radio-whatsapp').checked 
            || document.getElementById('radio-telefono').checked) {
            if (!telefonoValor) {
                document.getElementById('telefono').focus();
                alert('Si el contacto es por teléfono o whatsapp ingrese un número de teléfono');
            }
        }
    }

   const validaEmail = (correo) => {
    return /^[-\w.%+]{1,64}@(?:[A-Z0-9-]{1,63}\.){1,125}[A-Z]{2,63}$/i.test(correo);
   }

})




