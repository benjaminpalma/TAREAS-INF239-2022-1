
 document.addEventListener("DOMContentLoaded", function(event) {
    var dataTable = new DataTable("#tablaCanciones",{
        fixedHeight: true,
        lastText: "Último",
        firstText: "Primero",
        prevText: "Anterior",
        nextText: "Siguiente",
        labels: {
              placeholder: "Buscar...",
              info: "Mostrando registros del {start} al {end}",
              noRows: "Mostrando registros del 0 al 0 de un total de 0 registros",
              perPage: "Mostrar {select} canciones por página",
        }
    });

    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl)
    }) 
});

//botón EDITAR

var mySelect = new SlimSelect({
    select: '#album',
    placeholder: 'Elegir Album'
  })


$("#btnNuevo").click(function(){
    document.getElementById("formCanciones").reset();
    document.querySelector(".modal-header").style.backgroundColor = "#eb5e92";
    document.querySelector(".modal-header").style.color = "white";
    document.querySelector(".modal-title").textContent = "Nueva Canción";   

    $("#modalCRUD_song").modal("show");        
    id=null;
    opcion = 1; //alta
  });  

$(document).on("click", ".btnEditar", function(){
    id = $(this).val();
    opcion = 2 //editar
    $.ajax({
        url:"getData_songs.php",
        method:"POST",
        data:{id:id},
        dataType:"json",
        success:function(data)
        {
            document.getElementById("nombre").value = data.nombre;
            document.getElementById("letra").value = data.letra;
            document.getElementById("fecha").value = data.fecha;
            document.getElementById("album").value = data.albumes;
            document.querySelector(".modal-header").style.backgroundColor = "#204986";
            document.querySelector(".modal-header").style.color = "white";
            document.querySelector(".modal-title").textContent = "Editar Canción";
            mySelect.set(data.albumes)
            $('#modalCRUD_song').modal('show');
        }
       })  
      })

//botón BORRAR
$(document).on("click", ".btnBorrar", function(){    
    id = $(this).val();
    opcion = 3 //borrar
    var respuesta = confirm("¿Está seguro de eliminar el registro: "+id+"?");
    if(respuesta){
        $.ajax({
            url: "crud_song.php",
            type: "POST",
            dataType: "json",
            data: {opcion:opcion, id:id},
            success: function(response){
                window.alert(response);
                location.reload()
            }
        });
    }   
});
    
$("#formCanciones").submit(function(e){
    e.preventDefault();    
    nombre  = $.trim($("#nombre").val());
    fecha   = $.trim($("#fecha").val());
    letra   = $.trim($("#letra").val());
    album   = mySelect.selected();

    if((nombre.replace(/\s+/g, '') == "") || (album.length == 0)) {
        window.alert('La canción debe tener un nombre y pertenecer a un album');
    }else{
    $.ajax({
        url: "crud_song.php",
        type: "POST",
        dataType: "json",
        data: {nombre:nombre, fecha:fecha, letra:letra, id:id, opcion:opcion, album:album},
        success: function(response){  
            mensaje = response;
            window.alert(mensaje);
            location.reload()  
        },
        error: function(){
            window.alert('error');
        }
    })
    $("#modalCRUD_song").modal("hide");
    }
}); 


