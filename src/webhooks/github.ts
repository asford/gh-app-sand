import * as express from "express";
import * as co_body from "co-body";
import { Request, Response } from "express";

import * as sign from '@octokit/webhooks/sign'
const secret = 'mysecret';

async function handler(req: Request, res: Response, next) {
  try {

    // Get body (and raw body for validation), unpack content type
    let { parsed: body, raw: raw_body } = await co_body(req, {returnRawBody: true})

    if (req.header["content-type"] == "application/x-www-form-urlencoded") {
      body = body["payload"]
    }

    // Validate request body via signature
    const sig = req.headers['x-hub-signature']
    const local_sig = sign(secret, raw_body)
    console.log("x-hub-sig: ", sig)
    console.log("payload-sig: ", local_sig)

    if(sig !== local_sig){
      console.log("Invalid signature.")

      res.status(400).send({"error": "Invalid x-hub-signature."})
      return
    }

    const name = req.headers['x-github-event']
    const id = req.headers['x-github-delivery']

    console.log("name: ", name)
    console.log("id: ", id)
    console.log(body)

    res.status(200).send()
  } catch(e) {
    next(e)
  }
}

export { handler }
