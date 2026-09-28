# Copilot effort: live launch validation

## Isolation and scope

Real Firstmate scripts, Treehouse, tmux, jq, and OpenCode 1.18.32 were exercised in a marked disposable FM_HOME and throwaway Git project. HOME and all XDG roots were inside the worktree; the tmux socket was private. The attached pty was 120×35 and drained. No operator credentials, configuration, fleet, or external inference service was used. OpenCode’s built-in Copilot catalog was enabled by an empty provider models configuration, without supplying model records or credentials.

The OpenCode observer forwarded to the installed executable unchanged. For the timeout/abort faults it stopped a real catalog process; for directory failure a narrowly scoped mktemp shim rejected only the variant-output directory. All other tools and endpoints were real.

These checks prove emitted launch configuration, its presence in running worker processes, and its resolution by `opencode debug agent build --pure`. They do not claim successful model inference or rendered-TUI validation. The change affects CLI dispatch/configuration rather than visual layout.

## Observed launch behavior

### listed

Model: `github-copilot/claude-opus-4.7`; requested effort: `xhigh`.

```text
fm-gate-refuse: gate agent lifecycle permitted only against lab home /home/kumarpawa/.no-mistakes/worktrees/c936b9d8764d/01M3MFYGY4G18KEGCRZ56T9817/.test-tmp/live/fm
spawned copilot-live-listed harness=opencode kind=scout window=fm-lab-copilot:fm-copilot-live-listed worktree=/home/kumarpawa/.no-mistakes/worktrees/c936b9d8764d/01M3MFYGY4G18KEGCRZ56T9817/.test-tmp/live/pool/.treehouse/project-d990a1/1/project
```

Resolved build agent (real OpenCode consumer):
```json
{
  "name": "build",
  "model": {
    "providerID": "github-copilot",
    "modelID": "claude-opus-4.7"
  },
  "variant": "xhigh"
}
```
Catalog invocations: 1; spawn elapsed: 4.02s.
Running worker environment contained exactly the emitted launch JSON. Requested effort remained in task metadata. No temporary variant output directory remained.

### unlisted

Model: `github-copilot/gpt-5-mini`; requested effort: `max`.

```text
fm-gate-refuse: gate agent lifecycle permitted only against lab home /home/kumarpawa/.no-mistakes/worktrees/c936b9d8764d/01M3MFYGY4G18KEGCRZ56T9817/.test-tmp/live/fm
notice: OpenCode lists no 'max' variant for 'github-copilot/gpt-5-mini' (its variants: low medium high); effort=max is recorded but omitted from the launch
spawned copilot-live-unlisted harness=opencode kind=scout window=fm-lab-copilot:fm-copilot-live-unlisted worktree=/home/kumarpawa/.no-mistakes/worktrees/c936b9d8764d/01M3MFYGY4G18KEGCRZ56T9817/.test-tmp/live/pool/.treehouse/project-d990a1/2/project
```

Resolved build agent (real OpenCode consumer):
```json
{
  "name": "build"
}
```
Catalog invocations: 1; spawn elapsed: 4.07s.
Running worker environment contained exactly the emitted launch JSON. Requested effort remained in task metadata. No temporary variant output directory remained.

### none

Model: `github-copilot/gpt-5.4-nano`; requested effort: `high`.

```text
fm-gate-refuse: gate agent lifecycle permitted only against lab home /home/kumarpawa/.no-mistakes/worktrees/c936b9d8764d/01M3MFYGY4G18KEGCRZ56T9817/.test-tmp/live/fm
notice: OpenCode lists no 'high' variant for 'github-copilot/gpt-5.4-nano' (its variants: none listed); effort=high is recorded but omitted from the launch
spawned copilot-live-none harness=opencode kind=scout window=fm-lab-copilot:fm-copilot-live-none worktree=/home/kumarpawa/.no-mistakes/worktrees/c936b9d8764d/01M3MFYGY4G18KEGCRZ56T9817/.test-tmp/live/pool/.treehouse/project-d990a1/1/project
```

Resolved build agent (real OpenCode consumer):
```json
{
  "name": "build"
}
```
Catalog invocations: 1; spawn elapsed: 4.21s.
Running worker environment contained exactly the emitted launch JSON. Requested effort remained in task metadata. No temporary variant output directory remained.

### noeffort

Model: `github-copilot/claude-opus-4.7`; requested effort: `None`.

```text
fm-gate-refuse: gate agent lifecycle permitted only against lab home /home/kumarpawa/.no-mistakes/worktrees/c936b9d8764d/01M3MFYGY4G18KEGCRZ56T9817/.test-tmp/live/fm
spawned copilot-live-noeffort harness=opencode kind=scout window=fm-lab-copilot:fm-copilot-live-noeffort worktree=/home/kumarpawa/.no-mistakes/worktrees/c936b9d8764d/01M3MFYGY4G18KEGCRZ56T9817/.test-tmp/live/pool/.treehouse/project-d990a1/2/project
```

Resolved build agent (real OpenCode consumer):
```json
{
  "name": "build"
}
```
Catalog invocations: 0; spawn elapsed: 4.30s.
Running worker environment contained exactly the emitted launch JSON. Requested effort remained in task metadata. No temporary variant output directory remained.

### mktemp

Model: `github-copilot/claude-opus-4.7`; requested effort: `high`.

```text
fm-gate-refuse: gate agent lifecycle permitted only against lab home /home/kumarpawa/.no-mistakes/worktrees/c936b9d8764d/01M3MFYGY4G18KEGCRZ56T9817/.test-tmp/live/fm
injected variant-directory failure
notice: could not read the variants of 'github-copilot/claude-opus-4.7' from 'opencode models github-copilot --verbose --pure'; effort=high is recorded but omitted from the launch
spawned copilot-live-mktemp harness=opencode kind=scout window=fm-lab-copilot:fm-copilot-live-mktemp worktree=/home/kumarpawa/.no-mistakes/worktrees/c936b9d8764d/01M3MFYGY4G18KEGCRZ56T9817/.test-tmp/live/pool/.treehouse/project-d990a1/1/project
```

Resolved build agent (real OpenCode consumer):
```json
{
  "name": "build"
}
```
Catalog invocations: 0; spawn elapsed: 4.42s.
Running worker environment contained exactly the emitted launch JSON. Requested effort remained in task metadata. No temporary variant output directory remained.

### unavailable

Model: `github-copilot/claude-opus-4.7`; requested effort: `high`.

```text
fm-gate-refuse: gate agent lifecycle permitted only against lab home /home/kumarpawa/.no-mistakes/worktrees/c936b9d8764d/01M3MFYGY4G18KEGCRZ56T9817/.test-tmp/live/fm
notice: could not read the variants of 'github-copilot/claude-opus-4.7' from 'opencode models github-copilot --verbose --pure'; effort=high is recorded but omitted from the launch
spawned copilot-live-unavailable harness=opencode kind=scout window=fm-lab-copilot:fm-copilot-live-unavailable worktree=/home/kumarpawa/.no-mistakes/worktrees/c936b9d8764d/01M3MFYGY4G18KEGCRZ56T9817/.test-tmp/live/pool/.treehouse/project-d990a1/2/project
```

Resolved build agent (real OpenCode consumer):
```json
{
  "name": "build"
}
```
Catalog invocations: 1; spawn elapsed: 4.53s.
Running worker environment contained exactly the emitted launch JSON. Requested effort remained in task metadata. No temporary variant output directory remained.

### timeout

Model: `github-copilot/claude-opus-4.7`; requested effort: `high`.

```text
fm-gate-refuse: gate agent lifecycle permitted only against lab home /home/kumarpawa/.no-mistakes/worktrees/c936b9d8764d/01M3MFYGY4G18KEGCRZ56T9817/.test-tmp/live/fm
notice: 'opencode models github-copilot' did not answer within 1s; effort=high for 'github-copilot/claude-opus-4.7' is recorded but omitted from the launch
spawned copilot-live-timeout harness=opencode kind=scout window=fm-lab-copilot:fm-copilot-live-timeout worktree=/home/kumarpawa/.no-mistakes/worktrees/c936b9d8764d/01M3MFYGY4G18KEGCRZ56T9817/.test-tmp/live/pool/.treehouse/project-d990a1/1/project
```

Resolved build agent (real OpenCode consumer):
```json
{
  "name": "build"
}
```
Catalog invocations: 1; spawn elapsed: 4.77s.
Running worker environment contained exactly the emitted launch JSON. Requested effort remained in task metadata. No temporary variant output directory remained.

### anthropic

Model: `anthropic/claude-sonnet-4-5`; requested effort: `high`.

```text
fm-gate-refuse: gate agent lifecycle permitted only against lab home /home/kumarpawa/.no-mistakes/worktrees/c936b9d8764d/01M3MFYGY4G18KEGCRZ56T9817/.test-tmp/live/fm
spawned copilot-live-anthropic harness=opencode kind=scout window=fm-lab-copilot:fm-copilot-live-anthropic worktree=/home/kumarpawa/.no-mistakes/worktrees/c936b9d8764d/01M3MFYGY4G18KEGCRZ56T9817/.test-tmp/live/pool/.treehouse/project-d990a1/2/project
```

Resolved build agent (real OpenCode consumer):
```json
{
  "name": "build",
  "model": {
    "providerID": "anthropic",
    "modelID": "claude-sonnet-4-5"
  },
  "variant": "high"
}
```
Catalog invocations: 0; spawn elapsed: 4.71s.
Running worker environment contained exactly the emitted launch JSON. Requested effort remained in task metadata. No temporary variant output directory remained.

### openai

Model: `openai/gpt-5`; requested effort: `xhigh`.

```text
fm-gate-refuse: gate agent lifecycle permitted only against lab home /home/kumarpawa/.no-mistakes/worktrees/c936b9d8764d/01M3MFYGY4G18KEGCRZ56T9817/.test-tmp/live/fm
spawned copilot-live-openai harness=opencode kind=scout window=fm-lab-copilot:fm-copilot-live-openai worktree=/home/kumarpawa/.no-mistakes/worktrees/c936b9d8764d/01M3MFYGY4G18KEGCRZ56T9817/.test-tmp/live/pool/.treehouse/project-d990a1/1/project
```

Resolved build agent (real OpenCode consumer):
```json
{
  "name": "build",
  "model": {
    "providerID": "openai",
    "modelID": "gpt-5"
  },
  "variant": "xhigh"
}
```
Catalog invocations: 0; spawn elapsed: 4.97s.
Running worker environment contained exactly the emitted launch JSON. Requested effort remained in task metadata. No temporary variant output directory remained.

### abort

```text
fm-gate-refuse: gate agent lifecycle permitted only against lab home /home/kumarpawa/.no-mistakes/worktrees/c936b9d8764d/01M3MFYGY4G18KEGCRZ56T9817/.test-tmp/live/fm
error: window fm-lab-copilot:fm-copilot-live-abort already exists
```
The catalog was invoked; its stopped process was no longer running after the bound. No task metadata or variant output directory remained.

## Live configuration validation

Both public CLI validators were run against the following profiles. The resolver was deliberately given no rules, so accepted profiles returned `escalate: no rules to match` after schema validation without contacting Typesafe. A synthetic opt-in value enabled validation only; it was never used for authentication or transmitted. Invalid profiles exited 2 before any network call.

| Model | Effort | Bootstrap output | Resolver outcome |
|---|---|---|---|
| github-copilot/claude-opus-4.7 | low | accepted, rendered default profile | schema accepted; no rules |
| github-copilot/claude-opus-4.7 | medium | accepted, rendered default profile | schema accepted; no rules |
| github-copilot/claude-opus-4.7 | high | accepted, rendered default profile | schema accepted; no rules |
| github-copilot/claude-opus-4.7 | xhigh | accepted, rendered default profile | schema accepted; no rules |
| github-copilot/claude-opus-4.7 | max | accepted, rendered default profile | schema accepted; no rules |
| anthropic/claude-sonnet-4-5 | high | accepted, rendered default profile | schema accepted; no rules |
| anthropic/claude-sonnet-4-5 | max | accepted, rendered default profile | schema accepted; no rules |
| openai/gpt-5 | low | accepted, rendered default profile | schema accepted; no rules |
| openai/gpt-5 | xhigh | accepted, rendered default profile | schema accepted; no rules |
| github-copilot/ | high | invalid effort diagnostic | exit 2: unsupported effort/model |
| github-copilot/claude-opus-4.7 | ultra | invalid effort diagnostic | exit 2: unsupported effort/model |
| (omitted) | high | invalid effort diagnostic | exit 2: unsupported effort/model |
| anthropic/claude-sonnet-4-5 | medium | invalid effort diagnostic | exit 2: unsupported effort/model |
| openai/gpt-5 | max | invalid effort diagnostic | exit 2: unsupported effort/model |
| google/gemini-3.8-flash | high | invalid effort diagnostic | exit 2: unsupported effort/model |

## Supporting behavioral tests

- `bash tests/fm-spawn-dispatch-profile.test.sh`: passed, including mktemp failure with zero catalog calls, null/absent/empty variants, timeout, abort, and no-effort cases. This suite uses fake endpoints/catalogs and is supporting evidence, not the live proof above.
- `bash tests/fm-dispatch-resolve.test.sh`: passed, including concrete Copilot profile resolution against a stubbed Typesafe response.
- `bash tests/fm-bootstrap.test.sh`: passed, including dispatch profile validation.

The first spawn-suite attempt used worktree-local TMPDIR and encountered the pre-existing secondmate nesting restriction. Its normal harness-managed temporary directory resolved that setup issue; one retry exceeded the 240-second command budget, and the final run completed within a 600-second budget. No product failure was found.

All disposable lab homes, Git fixtures, private tmux sessions, and generated task temporary directories were removed. No source changes were made.
