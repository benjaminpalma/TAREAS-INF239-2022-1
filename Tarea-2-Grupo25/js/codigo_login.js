
var formulario_l = document.getElementById("formLogin");
formulario_l.addEventListener('submit', function(e){
    e.preventDefault();
    var form = new FormData(formulario_l);
    var email = form.get('email');
    var password = form.get('password');
    
    if(email.length == "" || password == ""){
    Swal.fire({
        type:'warning',
        title:'Debe ingresar un correo y/o password',
    });
    return false; 
    }else{
        fetch("login.php", {
        method: "POST",
        body: form
    })
    .then(res => res.json())
    .then(function(response) {
        if(response == 0){
            Swal.fire({
                type:'error',
                title:'Usuario y/o password incorrecta',
            });
        }else{
            Swal.fire({
                type:'success',
                title:'¡Credenciales correctas!',
                confirmButtonColor:'#204986',
                confirmButtonText:'Continuar'
            }).then((result) => {
                if(result.value){
                    //window.location.href = "vistas/pag_inicio.php";
                    window.location.href = "perfil.html";
                }
            })         
        }
    })
    }
});

var formulario_r = document.getElementById("formRegistro");
$('#formRegistro').submit(function(e){
    e.preventDefault();
    var form = new FormData(formulario_r);
    var email_registro = form.get('email_registro')
    var password_registro = form.get('password_registro')
    var nombre_registro = form.get('nombre_registro')

    if(email_registro.replace(/\s+/g, '').length == "" || password_registro.replace(/\s+/g, '') == "" ||nombre_registro.replace(/\s+/g, '') == ""){
        Swal.fire({
            type:'warning',
            title:'Algunos campos son obligatorios',
        });
        return false; 
    }else{
        fetch("registro.php", {
        method: "POST",
        body: form
    })
    .then(res => res.json())
    .then(function(response) {
        if(response.correcto){
            Swal.fire({
                type:'success',
                title: response.mensaje,
                confirmButtonColor:'#204986',
                confirmButtonText:'Iniciar sesión'
            }).then((result) => {
                if(result.value){
                    window.location.href = "sign.html";
                }})
            } else {
                Swal.fire({
                    type:'warning',
                    title:response.mensaje,
                    });
                }
    })
    }
});


