import * as express from "express";
import { Request, Response } from "express";

import { handler as hello_handler} from './hello';
import { handler as github_handler } from './webhooks/github';

let app = express()
const port = 3000

app.post("/webhooks/github", github_handler)
app.get('/hello', hello_handler);

app.listen(port, function() {
  console.log('Express server listening on port ' + port)
})
