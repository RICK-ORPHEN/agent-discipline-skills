# How to re-run this

0. `python3 calibration/check.py` must exit 0.
1. Seed a baseline once: `python3 seed.py <somewhere>/baseline prescriptive --prompt-out /dev/null`.
2. Per session: `python3 seed.py <run-dir> <style> --prompt-out <file>` and give the agent the
   text of `<file>` as its whole prompt. The instruction file's text is inside that prompt on
   purpose: a sub-agent does not load `CLAUDE.md` by itself.
3. `python3 check.py <somewhere>/baseline <run-dir>` per session.

Write down the model and date, what the agent is (a sub-agent of a chat session here), and
whether any tool call was refused. See `PRE-REGISTERED.md` for what this test does not cover.
