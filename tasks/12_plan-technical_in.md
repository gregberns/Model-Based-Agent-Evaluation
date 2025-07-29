The plan looks like its coming together in `docs/project-plan`.

Now we need to add very detailed, well defined technical specifications.

For each document, like `01_plugin_model_and_structure_plan.md`, lets add a new file with a name ending in `__tech`, like `01_plugin_model_and_structure_plan__tech.md`.

The technical plans should discuss 
* How the actual sub-system is going to be built out
* Files, Classes, and generally the Methods that will be implemented.
* Dive into the order in which components are going to be built out and developed

All code should be following best practices:
* Code should be testable - without complex mocks and stubs
* DRY principle
* Solid abstractions should be used
* "Library First" - functionality should be composable and re-usable

You do not have to actually do TDD - but all code should have associated tests... I mean this is Python, if its not tested it doesn't work.

If there are any other Best Practices that should be used, please make sure to include details in the technical specifications.

The goal here is to capture as many requirements as possible and translate them to a technical specification.

We want to catch as many problems with architecture durring this planning phase - instead of later in the development phase where it will be harder to change structures.

Once complete, create a new file with a summary in `12_plan-technical_out.md`

<!-- Once the technical specs are written, we need to create an ordered task list -->

