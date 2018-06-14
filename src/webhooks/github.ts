import * as debug from "debug";
import * as express from "express"
import * as co_body from "co-body"
import * as crypto from "crypto"
import { EventEmitter } from 'events'
import { Request, Response } from "express"
import * as fs from "fs"


const logger = debug("gh-app-sand:webhooks:github")
const secret: string = fs.readFileSync("secrets/webhooks/github").toString().trim()

const emitter = new EventEmitter

async function handler(req: Request, res: Response, next) {
  try {

    // Get body (and raw body for validation), unpack content type
    let { parsed: body, raw: raw_body } = await co_body(req, {returnRawBody: true})
    logger("content-type: ", req.get("content-type"))
    if (req.get("content-type") == "application/x-www-form-urlencoded") {
      logger("parsing payload")
      body = JSON.parse(body.payload)
    }

    logger("body: %j", body)

    // Validate request body via signature
    // from @ocotokit/webhooks/sign/index.js
    const sig = req.get('x-hub-signature')
    const local_sig = 'sha1=' + crypto.createHmac('sha1', secret).update(raw_body).digest('hex')
    logger("x-hub-sig: ", sig)
    logger("payload-sig: ", local_sig)

    if(sig !== local_sig){
      logger("Invalid signature.")

      res.status(400).send({"error": "Invalid x-hub-signature."})
      return
    }

    const name = req.get('x-github-event')
    //const id = req.headers['x-github-delivery']

    logger("name: ", name)

    emitter.emit(name, body)

    res.status(200).send()
  } catch(e) {
    next(e)
  }
}


export { handler, emitter }
