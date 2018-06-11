import * as debug from "debug";
import * as express from "express";
import { Request, Response } from "express";
import { set_zen, handler as zen_handler} from './zen';
import { handler as github_handler, emitter as github_events } from './webhooks/github';

const logger = debug("gh-app-sand:server")

let app = express()
const port = 3000

app.post("/webhooks/github", github_handler)
github_events.on("ping", function(body) {
  logger("received zen:", body.zen)
  set_zen(body.zen)
})

app.get('/zen', zen_handler)

app.listen(port, function() {
  console.log('Express server listening on port ' + port)
})
