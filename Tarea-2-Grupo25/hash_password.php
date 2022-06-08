<?php
function hash_password($password) {

 $options = array('cost' => 12);
 $password_hashed = password_hash($password, PASSWORD_BCRYPT, $options);
 return $password_hashed;
}
?>
