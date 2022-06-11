<?php
require('../db_config.php');
require('../php/validar.php');

// Recepción de los datos enviados mediante POST desde el JS   

$nombre = (isset($_POST['nombre'])) ? $_POST['nombre'] : '';
$imagen = (isset($_POST['imagen'])) ? $_POST['imagen'] : '';
$fecha = (isset($_POST['fecha'])) ? $_POST['fecha'] : '';
$id = (isset($_POST['id'])) ? $_POST['id'] : '';
$opcion = (isset($_POST['opcion'])) ? $_POST['opcion'] : '';
$mensaje = '';

switch($opcion){
    case 1: //alta, añadir nuevo album
        $sql_statement = "INSERT INTO ALBUMES (nombre, imagen, fecha_lanzamiento)  VALUES ($1, $2, $3)";
        $result = pg_query_params($dbconn, $sql_statement, array($nombre, $imagen, $fecha));
        if(!$result){
            echo pg_last_error($dbconn);
        }else{
            $mensaje = 'Album añadido con éxito';
        }
        break;
    case 2: //editar album
        $sql_statement = "UPDATE Albumes SET nombre=$1, imagen=$2, fecha_lanzamiento=$3 WHERE id=$4";
        $result = pg_query_params($dbconn, $sql_statement, array($nombre, $imagen, $fecha, $id));	
        if(!$result){
            echo pg_last_error($dbconn);
        }else{
            $mensaje = 'Album modificado con éxito';
        }	
        break;        
    case 3://baja, borrar
        $sql_statement = "DELETE FROM Albumes WHERE id=$1";		
        $result = pg_query_params($dbconn, $sql_statement, array($id));	 
        if(!$result){
            echo pg_last_error($dbconn);
        }else{
            $mensaje = 'Album eliminado con éxito';
        }
        break;   
    default:
        echo pg_last_error($dbconn);    
}

echo json_encode($mensaje);
