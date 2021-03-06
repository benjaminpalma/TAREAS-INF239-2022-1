<?php
require('../db_config.php');
require('../php/hash_password.php');

  //modificación del codigo visto en ayudantia, maneja el registro de un usuario
  //creación de un array que tendrá un mensaje y un bool que almacena si se llevó a cabo o no el registro
  $respuesta["mensaje"]   = "";
  $respuesta["correcto"]  = FALSE;

  //se recibe el email, se revisa si es que no esta registrado
  //si es que esta registrado, se actualiza el mensaje de 'respuesta'
  $email = filter_var($_POST["email_registro"], FILTER_SANITIZE_EMAIL);
  $sql = "SELECT email FROM Personas WHERE email=$1";
  $exists = pg_query_params($dbconn, $sql, array($email));
  if (pg_num_rows($exists) > 0) {
    $respuesta["mensaje"] = "El email ingresado ya existe";
  } else {
    //si es que no esta registrado, se hashea la contraseña y se almacena en la base de datos

    $nombre = filter_var($_POST["nombre_registro"], FILTER_SANITIZE_FULL_SPECIAL_CHARS);
    $apellido = filter_var($_POST["apellido_registro"], FILTER_SANITIZE_FULL_SPECIAL_CHARS);
    $password = $_POST["password_registro"];
    $password_hashed = hash_password($password);

    if((isset($nombre)&&!empty($nombre)) || (isset($email)&&!empty($email)) || (isset($password)&&!empty($password))){
      $password_hashed = hash_password($password);
      $query = "INSERT INTO Personas(email, password, nombre, apellido) VALUES ($1, $2, $3, $4);";
      $result = pg_query_params($dbconn, $query, array($email, $password_hashed, $nombre, $apellido));
      if($result){
        //si todo sale bien, se actualiza el bool 'correcto' a TRUE, y se cambia el mensaje
        $respuesta["correcto"]  = TRUE;
        $respuesta["mensaje"] = "¡Usuario creado con éxito!";
      } 
    }else{
      $respuesta["mensaje"] = "Algunos campos son obligatorios";
    }
  }
  echo json_encode($respuesta);
?>
