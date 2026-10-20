---
name: technical-writing
description: Write and edit prose using required ASD-STE100 Simplified Technical English. Use for replies, technical documents, guides, design notes, review reports, comments, change descriptions, and portable skill instructions.
---

# Technical writing

Write the information the reader needs to act or understand.
Use ASD-STE100 Simplified Technical English for all prose produced under this skill.
This requirement includes replies and instructions for other agents.

## Establish the document

1. Identify the reader, goal, scope, and sources.
2. Choose the document type.
3. Verify the facts, identifiers, paths, commands, and examples against the actual system.
4. Draft only the information that changes the reader's action or understanding.

| Type | Content |
| --- | --- |
| Tutorial | A learning sequence with a visible result at each step. |
| How-to | The steps and conditions for a specific practical outcome. |
| Reference | Exact facts, options, limits, errors, and interfaces for lookup. |
| Explanation | The context, mechanism, rationale, and tradeoffs for one topic. |

Separate and link sections when they serve different purposes.
Lead a change description with the problem and resulting user behavior.
Include implementation details only when they explain a choice or help a reviewer assess it.

## Apply the STE requirement

Use the [official ASD-STE100 rules and dictionary](https://www.asd-ste100.org/) as the authority.
The rules below are an operational summary. They do not replace the complete standard.

- Use dictionary-approved words only with their approved meanings and parts of speech.
- Use permitted technical nouns and technical verbs for domain concepts.
- Select one technical term for each concept and use it consistently.
- Use approved verb forms and simple tenses.
- Write instructions as direct commands in active voice.
- Limit each procedure sentence to 20 words.
- Limit each descriptive sentence to 25 words.
- Give each sentence one instruction, except when actions must occur at the same time.
- Put a required condition or warning before the affected action.
- Keep one topic in each paragraph.
- Keep articles and other words needed for correct grammar.
- Make each pronoun refer to one clear noun.
- Break up long noun groups with articles and prepositions.
- Use American English spelling unless an applicable directive requires another form.
- Remove idioms, figurative language, decorative phrasing, and needless abbreviations.

Keep code, command syntax, identifiers, file paths, UI labels, and direct quotations exact.
Treat exact literals separately from the prose that explains them.
Define unfamiliar technical terms at first use.
Do not invent a synonym for an existing symbol or product concept.

## Make the text useful

State who does what and what the reader can observe.
Keep facts, inferences, and estimates distinct.
Remove vague claims, unsupported praise, filler, repeated conclusions, and excessive qualification.
Keep necessary detail instead of compressing the text into fragments.

Use numbered lists for ordered steps and bullets for parallel items.
Use tables when they make a comparison easier to inspect.
Use descriptive link text and code formatting for exact literals.
Write headings in sentence case.
Avoid long dashes, decorative symbols, and repeated bold labels.

Keep a code comment when it explains a non-obvious reason that the code cannot express.
Prefer an executable check for an enforceable constraint.
Preserve necessary legal notices, public API documentation, and external compatibility explanations.

For skill instructions, state when the skill applies, what to do, how to verify, and what to report.
Use capability descriptions instead of product-specific APIs, model names, or installation paths.
Keep only instructions that affect a decision or result.
Check metadata and every referenced file after an edit.

## Verify the text

1. Check each material claim against its source.
2. Exercise commands and examples in a safe environment when practical.
3. Check vocabulary against the official dictionary and permitted technical terminology.
4. Check sentence length, grammar, terminology, and the other applicable STE rules.
5. Inspect the rendered document when layout affects meaning or usability.
6. Remove redundant text without removing requirements, evidence, or material limits.

Do not describe a sentence-length check as full STE validation.
If the official vocabulary or a suitable check is unavailable, state which checks remain unverified.
Return the requested text and any material evidence gaps.
