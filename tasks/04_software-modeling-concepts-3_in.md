<!-- Note: The useage of 'questions' below are in some cases because I'm not sure - but I've also been finding that Gemini can have 'strong independent opinions' that can be quite on-point some times. The objective is to get the model to hopefully trigger those opinions and use them to drive a better solution/outcome/output. -->

The model spec looks great. We'll want to add a note to build a schema validator to ensure the YAML files all follow the spec and that automated processes know how to build out the spec. 
We'll need to also search the internet for Python libraries that support defining schemas. I'm familiar with Zod from the Javascript ecosystem - something like that in Python would be great.


## Expand on the Behavioral Profile

Question: There will be a virtual plugin spec - the yaml file. But when we build the system around the model, when the system executes the virtual model - what's expected? Models are usually just minimal versions of code - not full implementations. In the Image Processing System, what tests could be implemented that could validate the behaviors, without having to implement a whole watermarking plugin?

So, we should really clarify what's expected out of the Virtual Plugins - meaning when an agent implements several of them the agent needs to know whether its actually going to build the code that implements the spec - or is it just going to implement the behaviors? How should it do that? We need to provide very precise details that can be passed to the future agents implementing these concepts.


## Separating the Modeling from Actual Plugins

While reading through the "Plugin Factory" section, my first thought was: "How are we going to manage our virtual plugins to test the system, then separately store and manage all the ACTUAL plugins".

This is a small but critical detail we'll want to figure out and define how we want it to look like.

It seems like the Plugin Factory and Virtual Plugins will be in a different sub-folder from the system/framework that'll execute, and the actual plugins will be stored in another area. Open to your ideas, but maybe the system could be configured to switch between either the virtual plugins or actual plugins.

## Note about Playbooks

One of the steps in the playbooks will need to be Incrementing the Semantic Version of the plugin and tracking changes to the plugins.

Could we integrate that into part of the Virtual Plugin Model? If we were to have the system execute a workflow, like "Fix Bug X", how could the Virtual Plugin Model help ensure that the actions taken were correct? Maybe thats not part of the responsibility of the Virtual Plugin, but I'd love your thoughts.

There will probably be a bunch of deterministic tasks that will need to be done, if the system only has one way of doing them, and we have really good ways ove verifying they are accomplished, the system should be more robust.

Maybe this will add clarity: for virtual plugins, the agent implementing them will need to know they are virtual plugins and not normal plugins. There probably need to be different prompt sets - or maybe a supplementary prompt for the virtual prompts.
For example, if the system is instructed on fixing a bug in a virtual plugin, it'll look at the code and say "there isn't an actual implementation for the whole plugin - I need to add it", but it should probably actually say "heres a mock bug I added, now I need to change the behavior to remove the bug". Does that make sense? It just seems like the agent executing a playbook will need to behave differently.
If there are different instructions though - we may see differences that are 'material' to the performance of the actual system.

Maybe I'm missing the point though - are the virtual plugins going to have a full implementation? I didn't think so.

## Plugin History Document

Not sure if this has been mentioned - but for each plugin we'll want to maintain a CHANGE_LOG file that documents changes that have been for each version of the plugin.


## Playbook action testing

Was thinking - in the Virtual Plugins, what if we could simulate and capture that an agent is performing a particular action. For example, when the agent executes the TDD workflow we should see several events occur 1) tests get executed probably a couple times 2) the version of the plugin changes 3) the plugin change log has been updated.

How could we assert that a series of behaviours/actions/events occured when the system acted on a virtual plugin?

This seems like something useful, right? Is there another approach? What are your thoughts?

## Next

Process the above: think hard about the problems and please add options and opinions if you think its beneficial to investigate more alternatives. We don't want to get too boxed into a particular approach at this point.

Then save your thoughts and research to: 04_software-modeling-concepts-3_out.md
