<?php
//codigo de la ayudantia, valida que el usuario tenga una sesion abierta
//si no tiene una sesión abierta, lo redirige a la vista de iniciar sesion/registrarse
session_start();
if (!isset($_SESSION["email"])) {
    header("Location: ../index.html");
    exit("Página Privada");
}
?>
<?php
