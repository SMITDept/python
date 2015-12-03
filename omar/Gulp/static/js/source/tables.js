//Verifica si el día o el mes tiene un solo dígito agrega 0 
function format_date(data){
  if (data.length === 1){
    data = "0" + data;
  }
  return data;
}

//Obtiene las ordenes de venta por una fecha
function get_by_date(){
    var date = document.getElementById("datepicker").value;
    if (date !== ""){
        $.ajax({
            type: "GET",
            url: "http://localhost:8080/get_orders",
            datatype: 'json',
        }).done(function (dataSet){
            var json = JSON.parse(dataSet);
            var values = json.values;
            insert_orders(values, date);

        });
    }
    else{
        alert("Selecciona una fecha");
    }
}


//Inserta las ordenes de ventas en la tabla
function insert_orders(values, date){
    var split_date = date.split("/");
    var day = format_date(split_date[0]);
    var month = format_date(split_date[1]);

    var new_date = day + "/" + month + "/" + split_date[2];
    
    var t = $('#orders').DataTable({
    "footerCallback": function ( row, data, start, end, display ) {
        var api = this.api();
        // Remove the formatting to get integer data for summation
        var intVal = function ( i ) {
            return typeof i === 'string' ?
                i.replace(/[\$,]/g, '')*1 :
                typeof i === 'number' ?
                    i : 0;
        };
        // Total over this page
        pageTotal = api
            .column( 7, { page: 'current'} )
            .data()
            .reduce( function (a, b) {
                return intVal(a) + intVal(b);
            }, 0 );
        // Update footer
        $( api.column( 7 ).footer() ).html(
            '$'+pageTotal
        );
    },
    "bDestroy": true
    } );
    t.clear();
    var aler_product = false;
    for (var i = 0; i < values.length; i++) {
        var total = ""; 
        out = [];
        var bandera = false;
        for (var j = 0; j < values[i].length; j++) {
            if (values[i][6] === new_date){
                aler_product = true;
                bandera = true;
                if (j === 0){
                    out.push("<a onClick='get_products("+ values[i][j] +");'>" + values[i][j] + "</a>");
                }
                if (j === 1){
                     total = values[i][j];
                }
                if (j !== 0 && j !== 1){
                     out.push(values[i][j]);
                }
            }
        }
        if (bandera === true){
            out.push(total);
            t.row.add(out).draw( false );
        } 
    }
    if (aler_product === false){
        alert("No hay ordenes de venta");
    }
}


$(document).ready(function() {
    $.ajax({
        type: "GET",
        url: "http://localhost:8080/get_orders",
        datatype: 'json',
    }).done(function (dataSet){
        var json = JSON.parse(dataSet);
        var values = json.values;

        var today = new Date();
        var day = format_date(today.getDate());
        var month = format_date((today.getMonth()+1).toString());
        var year = today.getFullYear();
        var date = day + "/" + month + "/" + year;

        insert_orders(values, date);

    }); 
} );

//Obtiene los productos de la orden de venta
function get_products(order) {
    window.scrollTo(0, 600000);
    $.ajax({
        data: {'order': order},
        type: "GET",
        url: "http://localhost:8080/get_products",
        datatype: 'json',
    }).done(function (dataSet){
        //window.location.reload();
        var json = JSON.parse(dataSet);
        var values = json.values;
        $('#products').DataTable( {
        //"bServerSide": true,
        data: values,
        columns: [
            { title: "Nombre" },
            { title: "Cantidad" },
            { title: "Precio" },
            { title: "Orden" }
        ],
        "bDestroy": true
        } );
    });
}
