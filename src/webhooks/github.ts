const Middleware = require('@octokit/webhooks/middleware')
const handler = new Middleware({
  secret: 'mysecret',
  path: "/webhooks/github"
})

handler.on('*', ({id, name, payload}) => {
  console.log("event: ", name);
})

export { handler };
