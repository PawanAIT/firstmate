# Spawn freshness live validation

## Scope and environment

Validated `bin/fm-spawn.sh` through its executable CLI, with real Git 2.43.0, Treehouse 3.1.0 and tmux. All repositories, origin servers (`file://` bare repositories), configuration, homes and pool slots were disposable beneath this run worktree's `.l/`. `bin/fm-lab-home.sh create "$PWD/.l/home"` minted the lifecycle-authorized home. No lifecycle bypass was used for live checks. No Herdr session was accessed.

The private tmux server was started with `TMUX_TMPDIR=.l/tmux tmux -f /dev/null -L fm-lab new-session -d -s primary -x 120 -y 40 -c "$PWD" -e FM_HOME="$PWD/.l/home" opencode`, with HOME/XDG paths isolated beneath `.l/user` and gate/path overrides removed from its environment. Spawn commands used only that private socket, real Treehouse allocation and the real OpenCode 1.18.32 launch command. These checks validate the spawn CLI through worktree refresh and task metadata publication, not an authenticated LLM response, agent completion, or credential availability. No login was attempted or fabricated.

An upload-pack observer logged each connection and then executed real `git upload-pack`. Connections made by Treehouse in the project checkout are separate from the freshness connections made by fm-spawn in the allocated worktree: the fast path used **one freshness connection**, while Treehouse independently made an earlier fetch. The late-advance case pushed a real new origin commit after Treehouse allocation, immediately before serving the freshness fetch; the allocated worktree moved from `0ea6bb944f9a99eb172e479cf44ecc49771c0e48` to `a8d71ff08f8f66cbc87e4174818cd962ee30ceea` using that single freshness connection.

## Evidence

- `live-spawn.log`: real spawn CLI transcripts, observed HEADs, origin/HEAD, timestamps, metadata, and origin contacts for the live scenarios.
- `live-*.json`: individual persisted-state observations.
- `live-shared.log` and `live-shared.json`: a real direct-PR ship in a second Treehouse slot reuses the first slot's successfully written clone-wide marker, with one freshness connection and no extension of the timestamp.
- `pool-base-regression.log`: targeted `FM_TEST_EVIDENCE=1 bash tests/fm-spawn-pool-base-freshen.test.sh` run. This suite passed, but mocks tmux/Treehouse and is **supplementary non-live coverage**, not the live proof above.
- `live-spawn-driver.py` and `shared-marker-driver.py`: exact evidence-producing drivers used in this run.

## Results

- Fresh timestamps: one freshness contact, correct new base, no probe ref left behind, timestamp unchanged; an equal-tip default-name switch remains bounded by the existing marker.
- Missing/expired/future/invalid markers: three freshness contacts, correct default name and current persisted timestamp.
- Marker path blocked by a directory: full refresh succeeds and the directory is preserved; inability to persist the marker does not fail spawn.
- Refresh settings: zero disables the fast path; empty/nonnumeric use the default window; a 30-second window expires a 60-second-old timestamp.
- Default switched to a different commit or old default deleted: fallback follows trunk and removes the probe ref.
- Unresolvable remote default with missing/fresh/expired marker: spawn refuses, does not publish task metadata and does not create or advance the marker.
- Origin inaccessible after allocation: both freshness fetch attempts fail and spawn refuses without metadata or marker changes. The accepted double-contact tradeoff is preserved.
- Separate pool slots share the same marker path and reuse its timestamp.

The first unreachable-origin fixture made origin unavailable before Treehouse could allocate a slot. It correctly refused during allocation, so it did not exercise the intended freshness failure. This setup limitation and assertion are retained in `live-spawn.log`/`live-unreachable.json`; `unreachable-after-allocation` fixes the fixture by routing only the later freshness connections to a genuinely absent Git repository. That re-drive reached the intended refusal and passed. No product code change was needed.

No UI was changed; CLI transcripts and persisted Git state are the evidence. No claim is made about model output or the blank initial OpenCode viewport. The private tmux server and all disposable worktree fixtures were removed after validation.
