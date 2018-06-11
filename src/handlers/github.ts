import * as debug from "debug";
import * as create_app from "github-app";
import * as fs from "fs";

const logger = debug("gh-app-sand:handlers:github")

const app_config = {
  id: fs.readFileSync("secrets/github-app.id").toString().trim(),
  cert: fs.readFileSync('secrets/github-app.private-key.pem')
}
const app = create_app(app_config)
logger("app id: ", app_config.id)

export { app }
