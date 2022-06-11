<?php
require('../db_config.php');
require('../php/validar.php');

//Realiza el READ del CRUD del album
if(isset($_POST["id"]))
{
    $id = $_POST["id"];
    $output = array();
    $statement = "SELECT * FROM Albumes WHERE id = $1";
    $result = pg_query_params($dbconn, $statement, array($id));
    $data = pg_fetch_all($result);
    foreach($data as $row)
    {
    $output["nombre"] = $row["nombre"];
    $output["imagen"] = $row["imagen"];
    $output["fecha"] = $row["fecha_lanzamiento"];
    }
    echo json_encode($output);
}
?>