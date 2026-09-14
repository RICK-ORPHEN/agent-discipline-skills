# Investigation note — <subject> / <date>

Fill this in before anything ships. If a field is empty, **filling that field is the first
task.** Do not fill it with a guess. Write "unknown" and go and close the unknown.

---

## 0. The reported symptom

> <the user's own words>

The report is an entrance, not a scope. Everything below is decided from data.

---

## 1. The population

Window: `<from>` – `<to>`

Query used:

```sql
<the query you actually ran, verbatim>
```

| Kind of error / action | Rows | Subjects | Last seen |
|---|---|---|---|
|  |  |  |  |

**Number of distinct faults: <n>**

### Is anything that ended in success actually missing data?

| Subject | Marked complete | Amount actually processed | Missing |
|---|---|---|---|
|  |  |  |  |

- [ ] Opened something recorded as "complete" and checked it

---

## 2. A case that works

Healthy example: `<id>`

- [ ] Verified from data that this example **really is healthy** (no partial loss)

| Aspect | Broken case | Working case |
|---|---|---|
| path |  |  |
| input format / size |  |  |
| filename / MIME sent |  |  |
| how it was produced (when, by which step) |  |  |
| other differences |  |  |

Write every difference. Narrowing to one comes after.

---

## 3. Observation

Where will you later be able to tell whether your change executed?

- Destination: `<audit log action / table / where it can be read>`
- Values recorded: `<branch taken / input shape / decision result>`
- [ ] Confirmed the main work does not stop if recording fails
- [ ] Emitting to **somewhere you can read later**, not `console.log`

Do not ship a fix without this.

---

## 4. Cause

Facts backed by observation:

- <fact 1> — evidence: <which data>
- <fact 2> — evidence: <which data>

Still hypotheses (say so):

- <hypothesis> — how to settle it: <what would confirm it>

**Is this specific to this subject, or to the whole path? <which>**

---

## 5. Scope of the fix

| # | What to fix | Kind (data loss / display / performance) | Doing it now? |
|---|---|---|---|
| 1 |  |  |  |

**Is anything involving data loss placed ahead of display problems? <yes / no>**

---

## 6. How you will know it is fixed

After the deploy, **what will you look at** to say "changed / unchanged"?

- Where: `<query / screen>`
- What counts as changed: `<a specific value moving>`
- Where you will look next if it did not change: `<decide this in advance>`

Do not report "it should be fixed." Report the before and after values side by side.
