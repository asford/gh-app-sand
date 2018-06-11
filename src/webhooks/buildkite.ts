import * as debug from "debug";
import * as express from "express"
import * as co_body from "co-body"
import { EventEmitter } from 'events'
import { Request, Response } from "express"
import * as fs from "fs"


const logger = debug("gh-app-sand:webhooks:buildkite")
const secret: string = fs.readFileSync("secrets/webhooks/buildkite").toString().trim()

const emitter = new EventEmitter

async function handler(req: Request, res: Response, next) {
  try {

    // Get body (and raw body for validation), unpack content type
    let body = await co_body.json(req)
    logger("content-type: ", req.get("content-type"))
    logger("body: ", body)

    // Validate request token
    const token = req.get('X-Buildkite-Token')

    if(token !== secret){
      logger("invalid X-Buildkite-Token: ", token)

      res.status(400).send({"error": "Invalid X-Buildkite-Token."})
      return
    }

    const name = req.get('X-Buildkite-Event')
    logger("name: ", name)

    emitter.emit(name, body)

    res.status(200).send()
  } catch(e) {
    next(e)
  }
}


export { handler, emitter }
