var express = require('express');
var app = express();

app.get('/', function (req, res) {
  console.log(req);

  res.send('Hello World!');
});

app.post(function(req, res){
  console.log(req);

  res.status(400);
  res.send();
});

app.listen(3000, function () {
  console.log('Example app listening on port 3000!');
});
