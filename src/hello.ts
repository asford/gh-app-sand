import * as express from "express";
import { Request, Response } from "express";

function hello(): string {
  return 'Hello cruel world!';
}

function handler(req: Request, res: Response) {
  console.log(req.url)
  console.log(req.body)

  res.status(200).send({
    message: hello()
  })
}

export {hello, handler};
