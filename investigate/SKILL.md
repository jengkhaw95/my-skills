---
name: investigate
description: Investigate how a system works, why a decision was made, or what causes an observed problem. Use for evidence-based explanations, runtime diagnosis, trace analysis, and recommendations without product changes.
---

# Investigate

Produce an answer supported by evidence.
Do not change the product or persistent external state during investigation.
Use disposable artifacts for experiments that preserve the original environment.

## Required language

Use ASD-STE100 Simplified Technical English for all prose, including replies, notes, and instructions for other agents.
Use approved words with their approved meanings and parts of speech.
Use permitted technical nouns and technical verbs consistently.
Limit procedure sentences to 20 words and descriptive sentences to 25 words.
Use active voice and direct commands. Put conditions before actions.
Keep code, commands, identifiers, and direct quotations exact.
Check the official rules and dictionary when available.
If a vocabulary check is unavailable, report that gap. Do not claim full STE compliance without evidence.

## Frame the question

1. State the question and the evidence that could answer it.
2. Identify the relevant version, configuration, environment, and affected path.
3. Inspect repository instructions, implementation, tests, and available operational evidence.
4. Ask only about material information that you cannot establish from available evidence.

For a behavior question, trace the entry point, data model, state changes, dependencies, and observable output.
For a rationale question, inspect history and decision records. Label inferred intent when no record confirms it.
For a defect, distinguish the reported symptom from a reproduced result.

## Test explanations

1. Reproduce the symptom through the interface where it occurs, when safe and possible.
2. List plausible causes and the observations that would distinguish them.
3. Choose the smallest observation that eliminates the most uncertainty.
4. Read actual errors and state. Add temporary instrumentation only in an isolated environment.
5. Trace the failure to the first incorrect decision or unhandled legitimate state.
6. If two attempts fail under the same assumption, test that assumption before another attempt.
7. Check whether the same mechanism explains related symptoms.

For live failures, use suitable runtime measurements.
For saved traces, record the capture conditions and the limits of what the trace can prove.
Locate the hot path, retained objects, or blocked operation as appropriate.
Map the finding to source. Label a cause as a hypothesis until evidence confirms the mechanism.
Keep profiler overhead separate from performance measurements.
Treat absent reproduction, missing credentials, and unavailable instrumentation as evidence gaps.

## Give the answer

Lead with the answer or diagnosis and its confidence.
Explain the relevant flow and ownership at the level the question needs.
Support material claims with inspected code, records, runtime observations, or captured artifacts.
Separate observations, inferences, and unresolved hypotheses.

For a recommendation, compare viable options against the user's goal and explain your choice.
If the evidence contradicts the premise, say so directly.
Name the next observation that would resolve any material uncertainty.
Return the diagnosis without implementing a fix unless the user also requested implementation.
