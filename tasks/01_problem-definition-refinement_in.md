<!-- The following refines the content generated from the previous step. -->


Lets take the outcome of `./tasks/00_problem-definition_out.md`, and make some refinements.

## "3.2. Agent-Assisted Maintenance"

  * A version history should be created and maintained as part of the process. The workflow should contain steps 
  * Semantic versioning should be used as part of the project.


## Workflow

Couple things that will be needed in the core workflow to ensure high quality results.

* Human In the Loop
  * Forgot to mention that we MUST figure out where there needs to be a human in the loop. There are too many places where

* Code Review
  * Once an agent has completed the code for a task, another instance of an agent with different instructions will need to review the code generated.

* TDD workflows
  * By default TDD should be used for each of the plugins being created. This workflow will need to be well designed, but can be validated indepentently.

<!-- GB NOTE: I've been working on building a TDD instruction set out in the day-to-day project I'm working on now. Will reuse parts of this probably -->


### 4.1. Technology Stack

"*   **Core System:** The primary infrastructure and agent logic will be developed in Python and Bash."
* NOTE: Bash is going to be used primariy to simplify this project.

### 4.2. Version Control

We'll want to include very specific workflows for the agents to use. We'll need to be careful they have the correct rights and access - to not mess somthing up too bad.

### 4.3. Global Templates & Configuration

"*   **Symlinks:**"
Symlinks are useful because a coding agent can then be executed in the plugin directory - without having access to anything outside of it. This helps with a variety of things from security to limiting the files available to the agent's context.


## 6. Tooling & Automation

In this project I don't want to use LangChain workflows - but that could be an option if our first attempt is unsuccessful.


## Addtionally

Wherever we talk about "Jira", we'll want to express that we will use an MCP server to manage all these projects. We'll probably use Shortcut for now - because I have a demo account we could use.


# ACTION

Please update the instructions and save them to `./tasks/01_problem-definition-refinement_out.md`

