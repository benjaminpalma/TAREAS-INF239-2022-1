<?php
require('../db_config.php');
require('../php/validar.php');

//Realiza el READ del CRUD de las canciones
if(isset($_POST["id"])){
 $id = $_POST["id"];
 $output = array();
 $albums = array();
 $statement = "SELECT * FROM Canciones LEFT JOIN Album_tiene_cancion ON Album_tiene_cancion.id_cancion = Canciones.id WHERE id = $1";
 $result = pg_query_params($dbconn, $statement, array($id));
 if(!$result){
    echo pg_last_error($dbconn);
 }
 else
 $data = pg_fetch_all($result);
 
 foreach($data as $row)
 {
  $output["nombre"] = $row["nombre"];
  $output["letra"] = $row["letra"];
  $output["fecha"] = $row["fecha_composicion"];
  $albums[] = $row["id_album"];
 }
 $output["albumes"] = $albums;
 echo json_encode($output);
}

?>