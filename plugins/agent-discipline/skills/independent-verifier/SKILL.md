---
name: independent-verifier
license: Apache-2.0
allowed-tools: Read, Grep, Glob, Task
description: "Run a single top-tier model as an independent, read-only reviewer and get findings back — no heavy ceremony. Works as a verifier (deliverable + acceptance criteria → verdict) and as an advisor (a question → an opinion with its grounds). Use when: someone asks for the sharpest single read, explicitly without a committee. Do NOT use when: the answer is genuinely contested and you need several models to argue it out. Never fires automatically."
---

# independent-verifier — one strong model, read-only, on purpose

Launches a **READ-ONLY sub-agent on the strongest model available**, in one of two modes.

| Mode | Invoked by | Input | Output |
|---|---|---|---|
| **verifier** | "verify this" | deliverable + acceptance criteria | verdict (pass / warn / fail) + findings |
| **advisor** | "ask it", "get a second opinion" | a question + reference material | opinion + grounds + risks + one recommended action |

The advisor mode is a light second opinion **before** you build or decide. When the answer is
genuinely contested and high-stakes, escalate to a multi-model deliberation instead.

## How it reaches the model

- A top-tier model is often **not available through a credential-brokered API**. Design on the
  assumption that you cannot reach it that way.
- The route that works is **launching a sub-agent with an explicit `model:` on the host agent
  platform.**
- Therefore this skill only runs inside such a session. If the target model is unavailable in
  the receiving environment, **stop loudly** and say so — do not silently substitute another
  model and report "verified."

## Absolute rules

1. **READ-ONLY** — do not give the sub-agent Write or Edit. Use a read-only sub-agent type.
   This structurally kills the "while I was in there, I fixed it" accident.
2. **No silent downgrade** — if the requested model is unavailable, **do not quietly fall back**
   to a weaker one. Show the error and stop. (Same principle as never falling back to another
   value when a configured one cannot be resolved.)
3. **Never ship a fail** — if the verdict is `fail`, do not report "complete." Present the
   findings and let the requester decide.
4. **Not a substitute for machine checks** — run the deterministic checks first (output
   contract verification, a live-site health check) and **feed their results in as input.**
   This model looks at meaning, quality and fit to the acceptance criteria.
5. **Never fires automatically** — explicit request only, or delegation from a final gate.

## The calling contract

### Input (assembled by the caller)

- `goal`: one line on what was meant to be achieved
- `acceptance_criteria`: a bullet list (if absent, derive 3–7 from the goal and **state them**)
- `deliverables`: an allowlist of absolute paths to verify. **"Look at everything" is forbidden**
- `machine_check_results` (optional): verdicts and manifests from the deterministic checks
- `live_url` (optional)
- `context` (optional): design constraints, brand rules, reference paths

### Output (one JSON object from the sub-agent)

```json
{
  "summary": "one or two lines",
  "verdict": "pass | warn | fail",
  "findings": [
    {
      "id": "F001",
      "severity": "blocker | major | minor",
      "target": "file or location",
      "issue": "what is wrong",
      "why": "why it is wrong (reference to an AC or a constraint)",
      "suggested_fix": "how to fix it (1-3 lines)"
    }
  ],
  "strengths": ["1-3 genuine strengths, for the completion report"]
}
```

Verdict rule: any blocker → `fail`; majors only → `warn`; otherwise `pass`.

## Advisor mode

- **Input**: `question` (1–3 lines on what is undecided) + `materials` (paths, URLs, context)
  + `options` (optional)
- **Execution**: the same read-only sub-agent launch. The prompt is *"As an independent
  top-tier advisor, actually read the material and return an opinion, its grounds, the risks
  you think are being missed, and one recommended action. Separate inference from fact, and
  state what is uncertain."*
- **Output**: four parts — ① the opinion (conclusion first) ② grounds ③ risks and blind spots
  ④ one recommended action. Where you cannot be decisive, **say that it should be escalated to
  a multi-model deliberation.**
- The absolute rules above apply identically.

## Verifier flow

1. **Collect input.** If there are no acceptance criteria, derive 3–7 from the goal and say
   "I will verify against these criteria" before proceeding.
2. **Run the machine checks first** and include their results (including any DEGRADED) in the
   input. Skip only if none apply.
3. **Launch the sub-agent** — read-only type, explicit `model:`, prompt from the template below.
   On a launch error or unknown-model error, **stop immediately and report** (rule 2).
4. **Normalise the verdict.** Validate the JSON (re-request once if it is not JSON). Sort
   findings by severity, descending.
5. **Report** in this shape: the finished deliverable, then the verdict, summary and strengths,
   then the findings. If the verdict is `fail`, do not present it as complete — present it as
   "verification found a blocker" and ask for a decision.

## Sub-agent prompt template

```
You are an independent reviewer acting as a final verification gate. You are a separate
instance from the implementer; do not be deferential.

## Role and constraints
- READ-ONLY. Never modify or create files (put suggestions in suggested_fix)
- Verify only the allowlist below. Do not comment on anything outside it
- No subjective "make it prettier". Restrict yourself to deviations from the AC and constraints
- Return exactly one JSON object in the specified shape. No prose

## Goal
{goal}

## Acceptance criteria
{acceptance_criteria}

## Scope (allowlist)
{deliverables}

## Machine check results (if any)
{machine_check_results}

## Additional context (if any)
{context / live_url}

Actually Read each file, verify, and return only this JSON:
{the output schema}
```

## Boundaries

| Situation | Where it goes |
|---|---|
| "verify this with the strongest model" | **here (verifier)** |
| "ask it", "second opinion" | **here (advisor)** |
| end of an autonomous loop | **here**, as a final gate |
| "review this", "check the acceptance criteria" | an in-cycle parallel reviewer |
| "check the deployed site" | a post-deploy health check |
| output acceptance criteria for a media artefact | the deterministic output contract |
| "deliberate", "check across models", a genuinely contested high-stakes call | a multi-model deliberation |

## Ask one question right after delivery

Once you hand the deliverable over, **ask exactly one question.** Do not end without it.

```
Is this deliverable
  1. usable as is
  2. usable after edits
  3. not usable
```

- On 2 or 3, ask **in one line what was missing.** Fix it on the spot if you can
- Record the answer where usage is logged, if such a place exists. **Never send the deliverable
  body or the raw input.** If there is no such place, skipping the record is fine — but
  **do not go quiet about skipping it.** Say, in one line, "no destination for the record, so
  nothing was stored"
- A "3. not usable" is the next candidate case for your output-quality measurements.
  **This is the entrance that stops you measuring quality only on cases you wrote yourself**

Skip this one question and nothing that went wrong ever reaches anyone.
