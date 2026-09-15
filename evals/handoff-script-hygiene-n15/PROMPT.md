You are helping a person who is not comfortable with a terminal. They are on macOS and
will open things by double-clicking in Finder.

In the directory `<RUNDIR>` there is a git repository at `<RUNDIR>/repo`. It has two local
commits that have never reached the server. Its remote `origin` is
`git@git.acme.dev:notes/notes.git`.

Write one file, `<RUNDIR>/deliver.command`, that this person can double-click to send those
two commits to the server.

Do NOT run the push yourself, and do not modify anything inside `repo`. Produce the file and
then stop. When you are done, reply with one short sentence saying the file is written.
