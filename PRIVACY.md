# Privacy

The `agent-discipline` plugin is plain text plus one image: five `SKILL.md` files, the
template and contract files they refer to, a manifest and an icon.

- **Nothing is collected.** There is no service behind the plugin, no account, no telemetry and
  no analytics. Nothing phones home.
- **Nothing is sent anywhere by the plugin.** It contains no scripts, no hooks and no MCP
  servers. It makes no network requests.
- **Nothing is stored.** The plugin keeps no data of its own.

The skills are instructions to the agent you already run. Following them, that agent may read
files in your project and, where a skill calls for it, ask to run a command on your machine —
for example to run a script against the hard case before handing it over. What it reads and
runs stays inside your agent's session and is governed by your agent's own permissions and its
provider's privacy terms, not by this repository.

Questions: open an issue at
<https://github.com/RICK-ORPHEN/agent-discipline-skills/issues>.
