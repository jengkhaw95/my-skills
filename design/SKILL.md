---
name: design
description: Design data models, interfaces, ownership, and system boundaries before implementation. Use for architecture decisions, unfamiliar interactions, consequential alternatives, and small prototypes that resolve empirical questions.
---

# Design

Produce the smallest design that meets the user outcome and can be verified.
A design request does not by itself authorize production implementation.

## Required language

Use ASD-STE100 Simplified Technical English for all prose, including replies, design notes, and instructions for other agents.
Use approved words with their approved meanings and parts of speech.
Use permitted technical nouns and technical verbs consistently.
Limit procedure sentences to 20 words and descriptive sentences to 25 words.
Use active voice and direct commands. Put conditions before actions.
Keep code, commands, identifiers, and direct quotations exact.
Check the official rules and dictionary when available.
If a vocabulary check is unavailable, report that gap. Do not claim full STE compliance without evidence.

## Understand the constraints

1. State the user outcome, non-goals, observable requirements, and compatibility obligations.
2. Read the affected system and its documented rationale.
3. Sketch how a caller or user will use the result.
4. Identify unknown facts, product preferences, and decisions that are expensive to reverse.

Measure observable facts instead of asking the user to guess.
Ask the user about consequential product preferences that evidence cannot resolve.
For a small change with an established pattern, use that pattern without unnecessary design work.

## Model the problem

- Define the domain entities, valid states, transitions, and ownership.
- Choose structures that fit the access patterns and prevent invalid combinations.
- Derive types from an authoritative schema when one exists.
- Keep validation at external boundaries and business rules independent of framework details.
- Define errors, side effects, cancellation, retries, and recovery where relevant.
- Design repeatable operations to tolerate interruption and re-execution.
- Separate concurrent write targets before adding coordination to a shared target.
- Keep interfaces small enough to hide meaningful complexity.
- Account for all callers, migration steps, and required compatibility.

Consider the design as if the new requirement had existed from the start.
Remove unnecessary layers before introducing new ones.
Do not add abstractions for hypothetical future uses.

## Compare consequential alternatives

For a novel or consequential decision, sketch two or three structurally different options.
Compare user experience, correctness, simplicity, compatibility, operational cost, and ease of verification.
Include a simpler option or the current design when viable.

If an empirical question decides the choice, build the smallest disposable prototype outside production source.
State the question and success criteria before the experiment.
For visual choices, inspect each variant and exercise its interactions.
For behavior or timing choices, capture the actual output or measurements.
Keep prototype code separate from the production deliverable.

Challenge the preferred option with a failure scenario and evidence that would reject it.
Use an independent perspective when available and useful.
Do not require a particular model or multiple agents.

## Deliver the design

Return the usage sketch, data model, key signatures, ownership boundaries, and chosen option.
Explain the deciding evidence and material tradeoffs.
List the implementation units and their verification criteria.
Identify unresolved choices and label prototype artifacts as disposable.

If implementation was also requested, proceed within that authorization.
If repeated workarounds reveal a flawed model, revise the model before adding more exceptions.
