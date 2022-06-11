<?php
function hash_password($password) {
    //funcion de la ayudantia, realiza el hash de la contraseña
 $options = array('cost' => 12);
 $password_hashed = password_hash($password, PASSWORD_BCRYPT, $options);
 return $password_hashed;
}
?>
