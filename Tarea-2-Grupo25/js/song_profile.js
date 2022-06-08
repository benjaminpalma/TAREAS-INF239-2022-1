
 document.addEventListener("DOMContentLoaded", function(event) {
    var dataTable = new DataTable("#listaCanciones",{
        sortable: false,
        lastText: "Último",
        firstText: "Primero",
        prevText: "Anterior",
        nextText: "Siguiente",
        labels: {
              placeholder: "Buscar...",
              info: "",
              noRows: "No hay resultados",
              perPage: "Mostrar {select} canciones por página",
        }
    });

    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl)
    }) 
});

$(document).on("click", ".btnMas", function(){
        id = $(this).val();
        $.ajax({
            url:"listSongs.php",
            method:"POST",
            data:{id:id},
            dataType:"json",
            success:function(data)
            {   
                document.getElementById("nombre_cancion").innerHTML = data.nombre_cancion;
                document.getElementById("letra").innerHTML = data.letra;
                document.getElementById("fecha").innerHTML = data.fecha;
                document.getElementById("albumes").innerHTML = data.albumes;
                document.getElementById("artistas").innerHTML = data.artistas;
                document.getElementById("imagenid").src=data.imagen
                document.querySelector(".modal-title").textContent = data.nombre_cancion;
                $('#modalPROFILE').modal('show');
            }
           })

          })
