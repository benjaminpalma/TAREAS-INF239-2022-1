<?php
session_start();
if (!isset($_SESSION["email"])) {
    header("Location: sign.html");
    exit("Página Privada");
}
?>