document.addEventListener("DOMContentLoaded", function(event) {
    var dataTable = new DataTable("#tablaAlbumes", {
        searchable: true,
        fixedHeight: true,
        lastText: "Último",
        firstText: "Primero",
        prevText: "Anterior",
        nextText: "Siguiente",
        labels: {
              placeholder: "Buscar...",
              info: "Mostrando registros del {start} al {end}",
              noRows: "Mostrando registros del 0 al 0 de un total de 0 registros",
              perPage: "Mostrar {select} albumes por página",
        }
        ,
        columns: [
            {
                select: 2,
                render: function(data, cell, row) {
                    return (data == "") ? '<img style="width:90px;height:90px;" src="/img/cd-icon.png">' : '<img style="width:90px;height:90px;" src=' + data + ' class="img-thumbnail">'
                }
            }
        ]
    });
});

$(document).ready(function(){

$('[data-toggle="tooltip"]').tooltip();
$("body").tooltip({ selector: '[data-toggle=tooltip]' });

$("#btnNuevo").click(function(){
    $("#formAlbumes").trigger("reset");
    $(".modal-header").css("background-color", "#eb5e92");
    $(".modal-header").css("color", "white");
    $(".modal-title").text("Nuevo Album");            
    $("#modalCRUD").modal("show");        
    id=null;
    opcion = 1; //alta
});    
    
  
//botón EDITAR    
$(document).on("click", ".btnEditar", function(){
    id = $(this).val();
    opcion = 2 //borrar
    $.ajax({
        url:"getData_albums.php",
        method:"POST",
        data:{id:id},
        dataType:"json",
        success:function(data)
        {
         $('#nombre').val(data.nombre);
         $('#imagen').val(data.imagen);
         $('#fecha').val(data.fecha);
         $(".modal-header").css("background-color", "#204986");
         $(".modal-header").css("color", "white"); 
         $('.modal-title').text("Editar Album");
         $('#modalCRUD').modal('show');
        }
        
       })  
      });           
});

//botón BORRAR
$(document).on("click", ".btnBorrar", function(){    
    fila = $(this);
    id = $(this).val();
    opcion = 3 //borrar
    var respuesta = confirm("¿Está seguro de eliminar el registro: "+id+"? Deberá actualizar las canciones que pertenecían a este álbum");
    if(respuesta){
        $.ajax({
            url: "crud_album.php",
            type: "POST",
            dataType: "json",
            data: {opcion:opcion, id:id},
            success: function(){
                location.reload();
            }
        });
    }   
});
    
$("#formAlbumes").submit(function(e){
    e.preventDefault();    
    nombre = $.trim($("#nombre").val());
    fecha = $("#fecha").val();
    imagen = $.trim($("#imagen").val());    
    $.ajax({
        url: "crud_album.php",
        type: "POST",
        dataType: "json",
        data: {nombre:nombre, fecha:fecha, imagen:imagen, id:id, opcion:opcion},
        success: function(){  
            location.reload();   
        }        
    });
    $("#modalCRUD").modal("hide");    
    
}); 

