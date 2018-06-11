import * as express from "express";
import * as bodyParser from "body-parser"; 
import { Request, Response } from "express";

import * as sign from '@octokit/webhooks/sign'
const secret = 'mysecret'; 

function verify_signature(req: Request, res: Response, buf: Buffer, encoding) {
  const sig = req.headers['x-hub-signature']
  const local_sig = sign(secret, buf.toString())
  console.log("x-hub-sig: ", sig)
  console.log("payload-sig: ", sign(secret, buf))

  if(sig !== local_sig){
    console.log("Invalid signature.")

    res.status(400)
      .send({"error": "Invalid x-hub-signature."})

    throw "Invalid signature."
  }
}

function process_hook(req: Request, res: Response) {
  const name = req.headers['x-github-event']
  const id = req.headers['x-github-delivery']

  console.log("name: ", name)
  console.log("id: ", id)
  console.log(req)

  // Extract payload from body if needed.

  res.status(200).send()
}

//handler.on('*', ({id, name, payload}) => {
//  console.log("event: ", name);
//})
//
const handler = [
  bodyParser.json({verify: verify_signature}),
  bodyParser.urlencoded({extended: true, verify: verify_signature}),
  process_hook,
]

export { handler }
