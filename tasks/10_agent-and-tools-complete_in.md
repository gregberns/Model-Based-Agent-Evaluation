<!-- After a whole large detour, I've got an agent and tools I'd be happy moving forward with. -->

After quite a bit of work, we've gotten to where we can proceed.

First, you, Gemini CLI, should make sure you understand what we're trying to build. We've already done a lot of work to figure out what we're going to build.

You'll need to read through the following files to understand how we got to where we're at.

Around step `08_*` and `09_*` there were some investigations into the agent and tooling - which has already been completed.

```
tasks/00_problem-definition_in.md
tasks/00_problem-definition_out.md
tasks/01_problem-definition-refinement_in.md
tasks/01_problem-definition-refinement_out.md
tasks/02_software-modeling-concepts_in.md
tasks/02_software-modeling-concepts_out.md
tasks/03_software-modeling-concepts-2_in.md
tasks/03_software-modeling-concepts-2_out.md
tasks/04_software-modeling-concepts-3_in.md
tasks/04_software-modeling-concepts-3_out.md
tasks/05_software-modeling-concepts-4_in.md
tasks/05_software-modeling-concepts-4_out.md
tasks/06_software-modeling-concepts-5_in.md
tasks/06_software-modeling-concepts-5_out.md
tasks/07_software-modeling-concepts-6_in.md
tasks/07_software-modeling-concepts-6_out.md
tasks/08_software-modeling-concepts-7_in.md
tasks/08_software-modeling-concepts-7_out.md
tasks/09_software-modeling-concepts-8_in.md
tasks/09_software-modeling-concepts-8_out.md
```

After processing all that information, we need to do a couple things.

Figure out a way to break the project down into areas that can be worked on individually.

Then, for each part of the project, build a very detailed specification of what the part of the system should do. The specification should consider any conflicts, tradeoffs, options that were discused, and you can also include any other options that might be available.

You'll want to save each of these out into files, so they can be processed easily. Create a `docs/project-plan` folder to store these docs.

Also create a high level document that ties all the parts together, specifies the order in which aspects of the project need to be accomplished.

You can add some technical details only if they contribute to the plan. But there will be a separate time to dive into technical details.

Later on - we'll take those documents and build out technical specifications. To sort through the files more easily, consider naming the files with `*_plan` then we can add `*_tech` or something once we get there.

Once you've completed all the documentation, we'll dive deep into it, document by document, and discuss issues that may need to be clarified.


Also, please put together a summary of what you've done, some high level things that need to be accomplished, etc, and put it into: 10_project-plan_out.md
