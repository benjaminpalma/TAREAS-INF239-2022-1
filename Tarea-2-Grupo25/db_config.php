<?php
/* Detalles de la conexión */
$conn_string = "host=localhost port=5432 dbname=tarea2v22 user=postgres password=cacahuate";
// Recuerde reemplazar "<contraseña>" por su contraseña y "<nombre_db>" por el nombre de su BD. No se incluyen los "<>".
// Establecemos una conexión con el servidor postgresSQL
$dbconn = pg_connect($conn_string);

// Verificamos la conexión.
if (!$dbconn) {
    echo("Error: No se ha podido conectar a la base de datos\n");
   }
/* Para incluir la configuración de este archivo en otro archivo .php utilice 
<?php include $_SERVER['DOCUMENT_ROOT'].'/db_config.php'; ?>
*/
?>