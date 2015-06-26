var https = require('https')
var fs = require('fs')

var options = {
	key: fs.readFileSync('server.key'),
	cert: fs.readFileSync('server.crt')
}

var server = https.createServer(options, function (request, response) {
	response.writeHead(200, {"Content-Type": "text/plain"})
	response.end("Hello World!\n")
})

server.listen(8888)

console.log("Server is up and running!")