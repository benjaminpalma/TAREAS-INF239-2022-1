<?php
require("db_config.php");
require("validar.php");

// Recepción de los datos enviados mediante POST desde el JS   

$id_cancion = (isset($_POST['id'])) ? $_POST['id'] : '';
$nombre = (isset($_POST['nombre'])) ? $_POST['nombre'] : '';
$fecha = (isset($_POST['fecha'])) ? $_POST['fecha'] : '';
$letra = (isset($_POST['fecha'])) ? $_POST['letra'] : '';
$opcion = (isset($_POST['opcion'])) ? $_POST['opcion'] : '';
$id_albums = (isset($_POST['album'])) ? $_POST['album'] : '';
$id_artista = $_SESSION['id'];
$mensaje = '';

switch($opcion){
    case 1: //alta, añadir nueva cancion
        $sql_statement = "INSERT INTO Canciones (nombre, letra, fecha_composicion)  VALUES ($1, $2, $3) RETURNING id";
        $result = pg_query_params($dbconn, $sql_statement, array($nombre, $letra, $fecha));
        $arr = pg_fetch_array($result, 0, PGSQL_NUM);
        $id_cancion = $arr[0];
        if(!$result){
            echo pg_last_error($dbconn);
        } else {
            //se agrega el id de la cancion en la tabla artista_compuso_cancion, a traves del id de la persona que tiene la sesion iniciada
            $sql_statement2 = "INSERT into Artista_compuso_cancion (id_artista, id_cancion)  VALUES ($1, $2)";
            $result2 = pg_query_params($dbconn, $sql_statement2, array($id_artista, $id_cancion));
            
            //por cada id de album seleccionado, se agrega la relacion a la tabla album_tiene_cancion
            $sql_statement3 = "INSERT into Album_tiene_cancion (id_album, id_cancion)  VALUES ($1, $2)";
            foreach($id_albums as $id){
                $result3 = pg_query_params($dbconn, $sql_statement3, array($id, $id_cancion));
            }

            if(!$result2 || !$result3){
                echo pg_last_error($dbconn);
            }else{
                $mensaje = 'Canción registrada con éxito';
            }
        }
        break;
    case 2: //editar cancion
        //se actualizan los datos
        $sql_statement = "UPDATE Canciones SET nombre=$1, fecha_composicion=$2, letra=$3 WHERE id=$4";
        $result = pg_query_params($dbconn, $sql_statement, array($nombre, $fecha, $letra, $id_cancion));    
        if(!$result){
            echo pg_last_error($dbconn);
        }
        else{
            //actualizar albumes a los que pertenece
            $deleteAlbums = "DELETE FROM Album_tiene_cancion WHERE id_cancion=$1";
            $result = pg_query_params($dbconn, $deleteAlbums, array($id_cancion));
            if(!$result){
                echo pg_last_error($dbconn);
            }else{
                $addAlbums = "INSERT into Album_tiene_cancion (id_album, id_cancion)  VALUES ($1, $2)";
                foreach($id_albums as $id){
                    $result3 = pg_query_params($dbconn, $addAlbums, array($id, $id_cancion));
                    if(!$result3){
                        echo pg_last_error($dbconn); 
                    }else{
                        $mensaje = 'Canción editada con éxito';
                    }
                }
            }
        }   	
        break;
    case 3://baja, borrar
        $sql_statement = "DELETE FROM Canciones WHERE id=$1";
        $result = pg_query_params($dbconn, $sql_statement, array($id_cancion)); 
        if(!$result){
            echo pg_last_error($dbconn);
        }
        else{
            $mensaje = 'Canción eliminada con éxito';
        }                
        break;   
    default:
        echo pg_last_error($dbconn);    
}
echo json_encode($mensaje);
