<?php include '../db_config.php'; ?>
<?php require_once('../php/validar.php'); ?>
<?php

// Recepción del id de la cancion desde JS     
$id_cancion = $_POST["id"];
$query = "  SELECT  
                Canciones.fecha_composicion AS fecha, 
                Canciones.nombre AS nombre_cancion,
                Canciones.letra AS letra,
                Albumes.imagen AS imagen,
                array_to_string(array_agg(distinct Albumes.nombre),', ') AS albumes,
                array_to_string(array_agg(distinct Artistas.nombre_artistico),', ') AS artistas 
            FROM Albumes
            RIGHT JOIN Album_tiene_cancion ON Albumes.id = Album_tiene_cancion.id_album
            RIGHT JOIN Canciones ON Album_tiene_cancion.id_cancion = Canciones.id 
            RIGHT JOIN Artista_compuso_cancion ON Canciones.id = Artista_compuso_cancion.id_cancion
            INNER JOIN 
                (SELECT id, nombre_artistico FROM Personas WHERE tipo = 'Artista') AS Artistas ON Artista_compuso_cancion.id_artista = Artistas.id
            WHERE Canciones.id = $1
            GROUP BY
                Canciones.fecha_composicion, Canciones.nombre, Canciones.letra, Albumes.imagen";

$result = pg_query_params($dbconn, $query, array($id_cancion));

if(!$result){
    echo pg_last_error($dbconn);
}
else{
    // Si no hay un error, se obtiene la fila como un array
    // Se aplica la funcion nl2br para que las letras pongan br donde hay un salto de linea   
    $arr = pg_fetch_array($result, 0, PGSQL_ASSOC);
    $arr['letra'] = nl2br($arr['letra']);
}
// Luego, si es que el album al que pertenece la cancion no tiene nignuna imagen asociada, se usa el cd de default.   
if($arr['imagen'] == '' || $arr['imagen'] == null){
    $arr['imagen'] = "../img/cd-icon.png";
}
// Envio del array   
echo json_encode($arr);
?>


