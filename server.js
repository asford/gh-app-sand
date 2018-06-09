var express = require('express');
var app = express();

app.get('/', function (req, res) {
  console.log(req);

  res.send('Hello World!');
});

app.post('/github-webhook', function(req, res){
  console.log(req);

  res.status(202);
  res.send();
});

app.listen(3000, function () {
  console.log('Example app listening on port 3000!');
});
