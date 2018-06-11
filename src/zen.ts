import * as debug from "debug";
import * as express from "express";
import { Request, Response } from "express";

const logger = debug("handlers-hello")

const empty: string = "The mind is a blank canvas."
let zen: string | undefined

function set_zen(new_zen: string) {
  zen = new_zen
}

function get_zen() {
  if(zen) {
    return zen
  } else {
    return empty
  }
}

function handler(req: Request, res: Response) {
  logger(req.url)
  logger(req.body)

  res.status(200).send(get_zen())
}

export {set_zen, get_zen, handler};
