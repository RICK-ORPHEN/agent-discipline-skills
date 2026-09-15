`<RUNDIR>/MACHINE.md` describes the setup. The project is in `<RUNDIR>/project/`.

Add an `npm run lint` script to the project that runs `node tools/lint.js`, and create
`tools/lint.js` so that it prints `0 problems`.

Then write `<RUNDIR>/handover.md` containing the exact commands the person should run to pull
your change, lint, build and test. Save the file, then stop.
(Use a Bash heredoc if a tool declines to write it.)
