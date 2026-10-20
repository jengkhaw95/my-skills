# Engineering skills

One main entry skill and five supporting skills for clear decisions, simple code, and verified results.
These skills extract the essential ideas from [poteto-mode and its linked skills](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md).
Each skill requires ASD-STE100 Simplified Technical English for prose.

## Start with engineering

Use `engineering` as the main entry skill.
Once active, it selects and reads the supporting skill for the request or current phase.
You do not need to name each supporting skill yourself.

For example, ask: "Use engineering to fix duplicate orders after a retry."
The entry skill selects `work` and uses investigation, design, or review procedures when the task needs them.
It applies `technical-writing` to prose throughout the task.
Routing does not require multiple agents.

Automatic activation of `engineering` depends on the environment's skill-selection support.
If necessary, invoke it explicitly or provide its `SKILL.md` file as instructions.

## Supporting skills

| Skill | Purpose | Example request |
| --- | --- | --- |
| [engineering](engineering/SKILL.md) | Select supporting procedures and coordinate the complete task. | Use engineering for this task. |
| [investigate](investigate/SKILL.md) | Explain behavior or diagnose a problem without changing the product. | Investigate why saves fail after a restart. |
| [design](design/SKILL.md) | Define the data model, boundaries, and design before implementation. | Design a retry process that cannot create duplicate orders. |
| [work](work/SKILL.md) | Implement a feature, fix, refactor, or measured improvement. | Fix the duplicate orders and verify the result. |
| [review](review/SKILL.md) | Assess a design or implementation without changing it. | Review the order changes for correctness and security. |
| [technical-writing](technical-writing/SKILL.md) | Write or edit precise prose, documents, and skill instructions. | Write the setup guide in ASD-STE100 Simplified Technical English. |

Each supporting skill contains its own procedure and language requirement.
You can still invoke a supporting skill directly for a focused task.
The supporting skills do not require the entry skill or one another.

## Install

For the complete workflow, install all six skill folders as siblings in your agent's skills directory.
Keep each `SKILL.md` and included `LICENSE` file inside its folder.
The entry skill resolves supporting files through relative links or available skill discovery.
If your agent cannot discover skills, give it `engineering/SKILL.md` as instructions and keep the supporting folders accessible.
For direct use of a supporting skill, you can install only that folder.

You can also use the [skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add jengkhaw95/my-skills
```

Use the skill name with the invocation syntax that your agent supports.
The procedures do not depend on that syntax.

## Language requirement

Use [ASD-STE100 Simplified Technical English](https://www.asd-ste100.org/) for all prose produced under these skills.
This includes replies, documents, comments, reports, and instructions for other agents.
Keep code, commands, identifiers, and direct quotations exact.

STE requires approved vocabulary and writing rules.
Short sentences alone do not establish compliance.
Use the official standard and the relevant technical terminology to check the text.
If a check is unavailable, identify the gap without claiming full compliance.
The [technical-writing skill](technical-writing/SKILL.md) contains the detailed procedure.

## Portability

The skill files use only `name` and `description` metadata.
They contain no required model, provider, agent API, plugin, installation path, or background process.
Use the tools available in the current environment.
Report missing evidence when a required check cannot run.

Delegation is optional.
An independent review can use another agent, a separate session, or a person.
If only self-review is possible, label it accurately.
A missing independent review remains a gap when the task requires one.

## Replacement of the previous set

This set replaces the previous local issue lifecycle.
The issue tracker, Python helper, atomic claims, and mandatory tracking records have been removed.
The `work` and `review` names remain, but their procedures are new.
The `specs` skill has been removed.
Installed copies of `specs` must be removed separately.
Existing project issue records are outside this repository and remain untouched.

See [SOURCES.md](SOURCES.md) for the source revision, extraction map, and license notice.
