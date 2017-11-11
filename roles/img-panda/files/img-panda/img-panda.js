var http = require('http');
var fs = require('fs');
var config = require('./config.json');
var HttpDispatcher = require('httpdispatcher');
var dispatcher = new HttpDispatcher();

function handleRequest(request, response){
    try {
        console.log("Requested URL: " + request.url);
        dispatcher.dispatch(request, response);
    } catch(err) {
        console.log(err);
    }
}
function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min)) + min;
}
dispatcher.onGet("/", function(req, res) {
	var img = fs.readFileSync(__dirname + '/resources/' + getRandomInt(1, 7) + '.jpg');
	res.writeHead(200, {'Content-Type': 'image/gif'});
	res.end(img, 'binary');
});

dispatcher.onError(function(req, res) {
        res.writeHead(404);
        res.end("404 - Page Does not exists");
});

http.createServer(handleRequest).listen(config.port, function(){
    console.log("Server listening on: http://localhost:%s", config.port);
});
