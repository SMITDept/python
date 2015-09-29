var http = require("http");
var url = require("url");
var queryString = require( "querystring" );
var sqlite3 = require('sql.js');
var db = new sqlite3.Database();
var path = require("path");
var fs = require("fs");
var util = require("util");

function login(data){
  var filebuffer = fs.readFileSync('orders_tpv.db');
  var db = new sqlite3.Database(filebuffer);
  sql = "SELECT * FROM users;";
  var results = db.exec(sql);
  var user = results[0]["values"];
  if (user[0][0] == data.user && user[0][1] == data.password){
    sql = "UPDATE users SET active = 1;";
    var results = db.exec(sql);
    var data = db.export();
    var buffer = new Buffer(data);
    fs.writeFileSync("orders_tpv.db", buffer);
  }
  db.close();
}

function logout(){
  var filebuffer = fs.readFileSync('orders_tpv.db');
  var db = new sqlite3.Database(filebuffer);
  sql = "UPDATE users SET active = 0;";
  var results = db.exec(sql);
  var data = db.export();
  var buffer = new Buffer(data);
  fs.writeFileSync("orders_tpv.db", buffer);
  db.close();
}

function delete_register(order){
  var filebuffer = fs.readFileSync('orders_tpv.db');
  var db = new sqlite3.Database(filebuffer);
  var sql = "DELETE FROM products WHERE order_id = " + order + ";";
  db.run(sql);
  var sql = "DELETE FROM orders WHERE num_order = " + order + ";";
  db.run(sql);
  var data = db.export();
  var buffer = new Buffer(data);
  fs.writeFileSync("orders_tpv.db", buffer);
  db.close();
}

function format_date(data){
  if (data.length === 1){
    data = "0" + data;
  }
  return data;
}

function delete_old_orders(){
  var today = new Date();
  today.setDate(today.getDate()-7);
  var day = format_date(today.getDate());
  var month = format_date((today.getMonth()+1).toString());
  var year = today.getFullYear();
  var filebuffer = fs.readFileSync('orders_tpv.db');
  var db = new sqlite3.Database(filebuffer);
  var sql = "SELECT * FROM orders;";
  var results = db.exec(sql);
  var orders = results[0]['values'];
  for (var i in orders) {
      var date = orders[i][6].split("/");
      if (date[1] < month){
        delete_register(orders[i][0]);
      }
      if (date[0] < day){
        delete_register(orders[i][0]);
      }
  };
  db.close();
}

function check_order(order){
  var number = order['name'];
  var num = ""; 
  for (var i = 0; i < number.length ; i++) {
    if (i > 5){
      num += number[i];
    }
  }
  var filebuffer = fs.readFileSync('orders_tpv.db');
  var db = new sqlite3.Database(filebuffer);
  var sql = "SELECT * FROM orders WHERE num_order = " + num + ";";
  var results = db.exec(sql);
  db.close();
  return results;
}

function table_products (product){
  var filebuffer = fs.readFileSync('orders_tpv.db');
  var db = new sqlite3.Database(filebuffer);
  var sql = "SELECT * FROM products WHERE order_id = " + product.order + ";";
  var results = db.exec(sql);
  var dataset = results[0];
  db.close();
  return dataset;
}

function table_orders (){
  var filebuffer = fs.readFileSync('orders_tpv.db');
  var db = new sqlite3.Database(filebuffer);
  sqlstr = "SELECT * FROM orders;";
  var results = db.exec(sqlstr);
  var dataset = results[0];
  db.close();
  return dataset;
}

function create_db () {

  sqlstr = "CREATE TABLE orders (num_order char, total float, paid char, user char, total_paid float, change float, date date, hour char);";
  db.run(sqlstr);
  sqlstr = "CREATE TABLE products (name_product char, quantity float, price float, order_id char, FOREIGN KEY (order_id) REFERENCES orders(num_order));";
  db.run(sqlstr);
  sqlstr = "CREATE TABLE users (user char, password char, active char);";
  db.run(sqlstr);
//(create the database)
  var data = db.export();
  var buffer = new Buffer(data);
  fs.writeFileSync("orders_tpv.db", buffer);
  db.close();
}

function get_products(data){
  var results = [];
  var result = {};
  var con = 1;
  for (var i in data){
    ini = i.substring(0,4)
    if (ini == "orde"){
      result[i]=data[i];
      con = con + 1;
    }
    if (con > 12){
      results.push(result);
      result = {};
      con = 1;
    }
  }
  return results;
}

function insert_products(data){
  var number = data['name'];
  var num = ""; 
  for (var i = 0; i < number.length ; i++) {
    if (i > 5){
      num += number[i];
    }
  }

  var products = get_products(data);
  var filebuffer = fs.readFileSync('orders_tpv.db');
  var db = new sqlite3.Database(filebuffer);
  sqlstr = "INSERT INTO products (name_product, quantity, price, order_id) VALUES (:name_product, :quantity, :price, :order_id);";

  for (var j in products){
    db.run(sqlstr, {':name_product': products[j]['orderlines['+j+'][product_name]'],
    ':quantity': products[j]['orderlines['+j+'][quantity]'],
    ':price': products[j]['orderlines['+j+'][price]'],
    ':order_id': num});
  }
  
  var data = db.export();
  var buffer = new Buffer(data);
  fs.writeFileSync("orders_tpv.db", buffer);
  db.close();
}

function insert_orders(data){
  var number = data['name'];
  var num = ""; 
  for (var i = 0; i < number.length ; i++) {
    if (i > 5){
      num += number[i];
    }
  }

  var day = format_date(data['date[date]']);
  var month = (parseInt(data['date[month]'])+1).toString();
  month = format_date(month);

  date_sale = day + "/" + month + "/" + data['date[year]'];
  hour = data['date[hour]'] + ":" +  data['date[minute]']
  var filebuffer = fs.readFileSync('orders_tpv.db');
  var db = new sqlite3.Database(filebuffer);
  sqlstr = "INSERT INTO orders (num_order, total, paid, user, total_paid, change, date, hour) VALUES (:order, :total, :paid, :user, :total_paid, :change, :date, :hour);";
  db.run(sqlstr, {':order': num, ':total': data['total_with_tax'], ':paid': data['paymentlines[0][journal]'],
    ':user': data['cashier'], ':total_paid': data['total_paid'], ':change': data['change'], ':date': date_sale, ':hour': hour});
  var data = db.export();
  var buffer = new Buffer(data);
  fs.writeFileSync("orders_tpv.db", buffer);
  db.close();
}


function onRequest(request, response) {
  var filebuffer = fs.readFileSync('orders_tpv.db');
  var db = new sqlite3.Database(filebuffer);
  var sql = "SELECT * FROM users;";
  var results = db.exec(sql);
  var user = results[0]["values"];


  var uri = url.parse(request.url).pathname
    , filename = path.join(process.cwd(), uri);

  fs.exists(filename, function(exists) {
    if(!exists) {
      response.writeHead(404, {"Content-Type": "text/plain"});
      response.write("404 Not Found\n");
      response.end();
      return;
    }
    if (user[0][2] === "1"){
      if (fs.statSync(filename).isDirectory()) filename += '/index.html';  
    }
    else{
      if (fs.statSync(filename).isDirectory()) filename += '/login.html';
    }

    fs.readFile(filename, "binary", function(err, file) {
      if(err) {        
        response.writeHead(500, {"Content-Type": "text/plain"});
        response.write(err + "\n");
        response.end();
        return;
      }

      response.writeHead(200);
      response.write(file, "binary");
      response.end();
    });
  });
  db.close();
}

http.createServer(function(request, response) {
  
  var get_url = url.parse(request.url).pathname;

  if (get_url == '/login'){
    var theUrl = url.parse( request.url );
    var queryObj = queryString.parse( theUrl.query );
    login(queryObj);
  }

  if (get_url == '/logout'){
    logout();
  }

  if (get_url == '/get_orders'){
    var orders = table_orders();
    var json = JSON.stringify(orders);
    response.end(json);
  }

  if (get_url == '/get_products'){
    var theUrl = url.parse( request.url );
    var queryObj = queryString.parse( theUrl.query );
    var results = table_products(queryObj);
    var json = JSON.stringify(results);
    response.end(json);
  }

  if (get_url == '/pos'){
    var theUrl = url.parse( request.url );
    var queryObj = queryString.parse( theUrl.query );
    //create_db();
    var check = check_order(queryObj);
    if (check.length === 0){
      insert_orders(queryObj);
      insert_products(queryObj);
    }
    delete_old_orders();
  }

  if (get_url == '/index.html'){
    url ="http://localhost:8080";
    response.writeHead(301, {
     'Location': url,
     'Content-Type': 'text/plain' });
    response.end();
  }

  if (get_url != '/get_orders' && get_url != '/pos' && get_url != '/get_products' && get_url != '/index.html'){
    onRequest(request, response);
  }
}).listen(8080);
console.log("Servidor Iniciado.");
