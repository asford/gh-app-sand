import * as express from "express";
import * as bodyParser from "body-parser";
import { Request, Response } from "express";

class App {

  constructor() {
    this.app = express();
    this.config();
    this.routes();
  }

  public app: express.Application;

  private config(): void {
    this.app.use(bodyParser.json());
    this.app.use(bodyParser.urlencoded({ extended: false }));
  }

  private routes(): void {
    const router = express.Router();

    router.get('/', (req: Request, res: Response) => {

      console.log(req.url);
      console.log(req.body);

      res.status(200).send({
        message: 'Hello World!'
      })
    });

    router.post('/github-webhook', (req: Request, res: Response) => {
      console.log(req.url);
      console.log(req.body);

      res.status(202).send();
    });

    this.app.use('/', router)
  }
}

let main = new App();

const port = 3000;

main.app.listen(port, function() {
  console.log('Express server listening on port ' + port);
});
