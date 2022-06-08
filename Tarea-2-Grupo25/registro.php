<?php
require("db_config.php");
require("hash_password.php");

  $respuesta["mensaje"]   = "";
  $respuesta["correcto"]  = FALSE;

    $email = filter_var($_POST["email_registro"], FILTER_SANITIZE_EMAIL);
    $sql = "SELECT email FROM Personas WHERE email=$1";
    $sql_statement = "SELECT password FROM Usuarios WHERE email = $1;";
    $exists = pg_query_params($dbconn, $sql, array($email));
    if (pg_num_rows($exists) > 0) {
      $respuesta["mensaje"] = "El email ingresado ya existe";
	
    } else {

      $nombre = filter_var($_POST["nombre_registro"], FILTER_SANITIZE_FULL_SPECIAL_CHARS);
      $apellido = filter_var($_POST["apellido_registro"], FILTER_SANITIZE_FULL_SPECIAL_CHARS);
      $password = $_POST["password_registro"];
      $password_hashed = hash_password($password);

      if((isset($nombre)&&!empty($nombre)) || (isset($email)&&!empty($email)) || (isset($password)&&!empty($password))){
        $password_hashed = hash_password($password);
        $query = "INSERT INTO Personas(email, password, nombre, apellido) VALUES ($1, $2, $3, $4);";
        $result = pg_query_params($dbconn, $query, array($email, $password_hashed, $nombre, $apellido));
        if($result){
          $respuesta["correcto"]  = TRUE;
          $respuesta["mensaje"] = "¡Usuario creado con éxito!";
        } 
      }else{
        $respuesta["mensaje"] = "Algunos campos son obligatorios";
      }
    }
    echo json_encode($respuesta);
    
  ?>
