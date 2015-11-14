//Funciones para la autenticación del usuario en el sistema
function login(){
    var user = document.getElementById("inputUser").value;
    var password = document.getElementById("inputPassword").value;
    var data = {"user": user, "password":password};
    if (user !== "" && password !== ""){
        $.ajax({
            data: data,
            type: "GET",
            url: "http://localhost:8080/login",
            datatype: 'json',
        }).done(function (dataSet){
            //alert("sali");
        });
    }
}

function logout(){
    $.ajax({
        type: "GET",
        url: "http://localhost:8080/logout",
        datatype: 'json',
    }).done(function (dataSet){
        //alert("sali");
    });
}
