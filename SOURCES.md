# Sources and extraction map

The starting point is [poteto-mode](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/SKILL.md).
The linked skills and playbooks were read as source material for this rewrite.
Their procedures were not invoked to perform the rewrite.

The source snapshot was read on 2026-10-20.
The pinned repository revision is `ddf824aff1e55ba14bd666b30bce3fc69962abe6`.
Use the [pinned source tree](https://github.com/cursor/plugins/tree/ddf824aff1e55ba14bd666b30bce3fc69962abe6/pstack/skills) to inspect the extracted material.

## Extraction map

| Local skill | Source material | Retained essentials |
| --- | --- | --- |
| `engineering` | `poteto-mode`, its 24 principle skills, `swarm`, `show-me-your-work`, and `figure-it-out` | Main entry routing, shared principles, bounded delegation, verification units, and decision records. |
| `investigate` | `how` and the investigation, bug fix, runtime forensics, trace forensics, and session pickup playbooks | Trace behavior and ownership, test hypotheses, identify causes, and separate facts from inferred intent. |
| `design` | `architect`, `interrogate`, and the prototype playbook | Define usage and data first, compare consequential alternatives, test empirical choices, and challenge assumptions. |
| `work` | The feature, bug fix, refactoring, performance, hillclimb, visual parity, and skill authoring playbooks; `benchmark-checklist` | Small verified changes, behavior checks, root causes, fair measurements, and evidence-based review corrections. |
| `review` | `interrogate`, `no-comments`, and the verification principles | Inspect the candidate, challenge claims, identify concrete impact, and distinguish defects from preferences. |
| `technical-writing` | `technical-writing`, `unslop`, and the skill authoring playbook | Reader purpose, clear structure, exact technical terms, useful comments, and concise instructions. |

The source mode's principle leaves cover these areas:

- Simplicity: laziness protocol, subtraction, reader load, and user experience.
- Design: foundational thinking, domain models, types, boundaries, first principles, and alternatives.
- State: idempotence, caller migration, target architecture, and separate write ownership.
- Evidence: root causes, premise checks, real results, behavioral tests, and measurement limits.
- Execution: repeatable tools, verifiable units, context limits, autonomy, and structural enforcement of lessons.

The rewrite removes host commands, fixed models, agent types, internal transcript paths, plugin dependencies, and source-specific routing chains.
The `engineering` entry skill retains the coordinator pattern with five local supporting skills.
It selects procedures by task and phase. The supporting skills also remain available for direct use.
It does not reproduce the source's full orchestration, PR management, shipping, or cleanup systems.
Publication and external actions remain subject to the user's authorization.

## Language standard

ASD-STE100 Simplified Technical English is an explicit requirement added for this repository.
The source's prose guidance alone does not establish full STE compliance.

Use the [official standard website](https://www.asd-ste100.org/) and [official FAQ](https://www.asd-ste100.org/STE_faq.html).
The [Issue 9 standard](https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf) supplies the writing rules and controlled dictionary.
The local summaries do not reproduce the dictionary or certify a document's compliance.

## Upstream license

The source package is covered by the [MIT license](https://github.com/cursor/plugins/blob/ddf824aff1e55ba14bd666b30bce3fc69962abe6/pstack/LICENSE).
Its notice is retained in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
