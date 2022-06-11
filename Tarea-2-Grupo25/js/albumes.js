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

    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl)
    }) 
});

$(document).ready(function(){

$("#btnNuevo").click(function(){    
    document.getElementById("formAlbumes").reset();
    document.querySelector(".modal-header").style.backgroundColor = "#eb5e92";
    document.querySelector(".modal-header").style.color = "white";
    document.querySelector(".modal-title").textContent = "Nuevo Album";          
    $("#modalCRUD").modal("show");        
    id=null;
    opcion = 1; 
});    
    
//botón EDITAR    
$(document).on("click", ".btnEditar", function(){
    id = $(this).val();
    opcion = 2 //editar
    $.ajax({
        url:"../php/getData_albums.php",
        method:"POST",
        data:{id:id},
        dataType:"json",
        success:function(data)
        {
         document.getElementById("nombre").value = data.nombre;
         document.getElementById("imagen").value = data.imagen;
         document.getElementById("fecha").value = data.fecha;
         document.querySelector(".modal-header").style.backgroundColor = "#204986";
         document.querySelector(".modal-header").style.color = "white";
         document.querySelector(".modal-title").textContent = "Editar Album";
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
            url: "../php/crud_album.php",
            type: "POST",
            dataType: "json",
            data: {opcion:opcion, id:id},
            success: function(response){
                window.alert(response);
                location.reload();
            }
        });
    }   
});
    
$("#formAlbumes").submit(function(e){
    e.preventDefault();    
    nombre = document.getElementById("nombre").value.trim();
    fecha = document.getElementById("fecha").value.trim();
    imagen = $.trim($("#imagen").val());

    if(nombre.replace(/\s+/g, '') == "") {
        window.alert('El album debe tener un nombre');
    }else{
    $.ajax({
        url: "../php/crud_album.php",
        type: "POST",
        dataType: "json",
        data: {nombre:nombre, fecha:fecha, imagen:imagen, id:id, opcion:opcion},
        success: function(response){  
            mensaje = response;
            window.alert(mensaje);
            location.reload();
        },     
        error: function(){
            window.alert('error');
        }
    })
    $("#modalCRUD").modal("hide");}
});

