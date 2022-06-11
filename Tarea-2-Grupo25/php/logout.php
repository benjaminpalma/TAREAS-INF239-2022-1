<?php
//codigo de la ayudantia, cierra la sesión que esta abierta
//luego redirige a la vista de iniciar sesion/registrarse
 session_start();
 session_destroy();
 unset($_SESSION['email']);
 header("location: ../html/sign.html");
?>
