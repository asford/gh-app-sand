import * as debug from "debug";
import * as express from "express";
import * as create_github_app from "github-app";
import * as fs from "fs";
import { Request, Response } from "express";
import { set_zen, handler as zen_handler} from './zen';
import { handler as github_handler, emitter as github_events } from './webhooks/github';
import { handler as buildkite_handler, emitter as buildkite_events } from './webhooks/buildkite';

const logger = debug("gh-app-sand:server")

const github_app_config = {
  id: fs.readFileSync("secrets/github-app.id").toString().trim(),
  cert: fs.readFileSync('secrets/github-app.private-key.pem')
}
const github_app = create_github_app(github_app_config)
logger("github_app.id: ", github_app_config.id)

let service = express()
const port = 3000

service.post("/webhooks/github", github_handler)
service.post("/webhooks/buildkite", buildkite_handler)
github_events.on("ping", function(body) {
  logger("received zen:", body.zen)
  set_zen(body.zen)
})

service.get('/zen', zen_handler)

service.listen(port, function() {
  console.log('Express server listening on port ' + port)
})
