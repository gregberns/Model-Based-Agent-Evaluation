
> We create a set of Python functions (`packages/framework/tools.py`) that will be exposed to the agent.

Your assumption that you can **just** create simple tools is fundamentally flawed. To get the tool descriptions, parameters, and even just the method in which the tool will work is a project in itself! Sure Read File is pretty easy - but what about specifying that you need an absolute path in the instructions, and what happens when the file is incredibly large? The Write File probably isn't too bad. But the Edit File is difficult and nuanced. Does the Model provide line numbers? Cause that doesn't work. If you just provide a snippet to replace thats ok, until there's a file with multiple lines that are the same and you try and replace that line.

This Agent is a Code Editor. If the File Edit tool is not good, the agent will have very poor performance.

We are not writing our own tools from scratch. The industry says "Its Easy" and yes its easy to write the code - but to get a well tuned tool set is non-trivial.

But if we want to go this direction, we may be able to find a tool set that exists in python, and add wappers around it.

LangChain has a File System tool, but there is no EditFile in there. 
https://python.langchain.com/docs/integrations/tools/filesystem/

Also I've seen issues with EditFile where once you start making changes to the file you have to figure out hoe to correctly update the cotext - otherwise writes can start overwriting the wrong part of the code.

I have not found a good edit file tool in a library. If you can find one we can move forward. Without a good set of tools, we cannot go this direction.
