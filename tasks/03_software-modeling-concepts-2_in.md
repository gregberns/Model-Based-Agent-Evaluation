<!-- Parent: 02_software-modeling-concepts_out.md -->

## Comments

The model should define its inputs and outputs - functions and parameters to the model.

I like the "agent playbook" termininology. Lets use that.

### MCP Spec

Lets use the MCP (Model Context Protocol) specification as the API model. Instead of actually building some API server, we should just define 'tool calls' that will take a specific structured input. Search the internet for the MCP spec so we can use it.

This is a basic example of a tool call. This is probably enough to get started. Its general enough to handle most of the structures we'll need.

```
{
  "name": "ask_question",
  "description": "Ask a question about a specified software repository.",
  "parameters": {
    "repoName": { "type": "string", "description": "Name of the repo" },
    "question": { "type": "string", "description": "The user question" }
  },
  "output": {
    "type": "string",
    "description": "The answer to the user question."
  }
}
```

But we'll want to extend this a bit - every plugin should be able to define multiple tool calls.


## Next Steps

There are some great ideas in there - but lets put some real structure around those ideas - what's the model and its structures and supporting code and scripts.

Make sure to go into great detail so there are concrete ideas to execute on. We should probably focus on building out the concepts at this point - implementation details aren't crucial. But if its helpful to add code snippets or example structures to explore ideas definitely do whatever will be helpful for future iterations to expand on the details you provide.

Be creative and also make sure to utilize existing information on the internet - the more data and examples we can get, the better the output will be.

Outfile: 03_software-modeling-concepts-2_out.md
