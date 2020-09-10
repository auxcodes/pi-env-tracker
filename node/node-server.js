// Load the http module to create an http server.
const http = require('http');
const Database = require('better-sqlite3');
const dbfile = '../env-tracker.db';

const db = new Database(dbfile, { verbose: console.log });
 
// Configure our HTTP server to respond with Hello World to all requests.
let server = http.createServer(function (request, response) {
  response.writeHead(200, {"Content-Type": "text/plain"});
  response.end("Hello World\n");
});
 
// Listen on port 8000, IP defaults to 127.0.0.1
server.listen(8000);
 
// Put a friendly message on the terminal
console.log("Server running at http://127.0.0.1:8000/");

const stmt = db.prepare('SELECT * FROM readings').all();

console.log(stmt);

db.close();
