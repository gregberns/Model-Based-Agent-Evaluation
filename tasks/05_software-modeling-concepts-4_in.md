<!-- The Agent still hasn't been able to coherently and explicity describe how we're going to tie together the virtual plugin modeling system into the system AND have it run the prod plugins. If it doesn't explicity define its path, we could get into implementation and everything fails because it can't connect the two. -->

## File Structure

In the file structure, in Python, should we be using a root `packages` dir to store the source code? 

What about scripts and code relating to the virtual plugins? You mentioned a file `plugin-profile.yaml`. I assume we don't want to put that all in `framework`. Lets make sure to define that as well - if it hasn't already.

## Verifying Agent Actions

I love the ideas you presented in "Verifying Agent Actions" - but how does that actually occur? 

So in the `The Virtual Plugin: A "Process Mock"` section it seems to suggest that there will need to be a separate playbook or set of instructions for a virtual plugin. 

When the framework executes against the virtual plugin or virtual plugin's playbook, is it going to call a 'mock agent' that somehow triggers those events? Or is the real agent going to execute the virtual plugin playbook - but how do the events get logged, assuming the real agent doesn't know how to log? Or does it need to know how to log?

If Gemini CLI is used as the real agent and used to modify the virtual plugin, how would we get logs to trigger?

> Its purpose is to test the *agent's ability to follow a playbook*, not to test the plugin's logic itself.

That is helpful to clarify, but lets assume the agent is "very good" - it can follow arbitraty instructions. It seems like the question then is how we put the playbooks under test or "evaluation". It seems like the "real" playbook(s) need to be evaluated to see how well the instructions in them are executed.

If we have one set of playbooks for the virtual plugins that say "change the yaml file", "call event 'write file'", etc, then another set of playbooks for the real plugins that say "debug the code, fix it, then change the version" then those are not tested at all.

I'm missing something here. How do we get from "A virtual plugin playbook can be executed with a particular set of instructions" to "Those same instructions can be used to execute against a real plugin".

Anything you can do to help me figure this out would be very appreciated.

If you can please write your thoughts to: 05_software-modeling-concepts-4_out.md
