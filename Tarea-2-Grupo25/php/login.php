<?php
require('../db_config.php');
require('../php/hash_password.php');

//recepción de datos enviados mediante POST desde ajax
$email = (isset($_POST['email'])) ? $_POST['email'] : '';
$password = (isset($_POST['password'])) ? $_POST['password'] : '';

// Obtenemos la contraseña hasheada del usuario de la BD.
$sql_statement = "SELECT id,password,tipo FROM Personas WHERE email = $1;";
$result = pg_query_params($dbconn, $sql_statement, array($email));

// Si no se pudo obtener la contraseña... Pánico.
if (!$result) {
 exit();
}

$arr = pg_fetch_array($result, 0, PGSQL_NUM);
$password_hashed = $arr[1];

if (password_verify($password, $password_hashed)) {
    session_start();
    $_SESSION["email"] = $email;
    $_SESSION["success"] = 1;
    $_SESSION["id"] = $arr[0];
    $_SESSION["rol"] = $arr[2];
    echo 1;
} else {
    echo 0;
}

?>
