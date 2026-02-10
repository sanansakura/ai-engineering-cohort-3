# Phase 1: Audio Capture Pipeline — ExecPlan

This ExecPlan is a living document. As tasks are completed, update the Progress section: change `- [ ]` to `- [x]` for that task.

This document follows MULTI_AGENT_WORKFLOW_GUIDE.md at the repository root.

---

## Purpose / Big Picture

Prove that real-time microphone capture works on macOS and produces 16 kHz mono, 16-bit audio chunks suitable for an ASR backend (Whisper, etc.). After this phase, you will have a pipeline that captures microphone input, converts or resamples to the target format, and streams or buffers chunks. Success is observable: run the pipeline, speak into the microphone, and observe audio data being produced (e.g., chunks written to a file, or a byte count incrementing).

---

## Progress

*As each task completes, check it off: change `- [ ]` to `- [x]`.*

- [ ] Agent 1 (Development): Step 1.1 — Create spike project directory and structure
- [ ] Agent 1 (Development): Step 1.2 — Implement AVAudioEngine capture with installTap
- [ ] Agent 1 (Development): Step 1.3 — Add format conversion to 16 kHz mono, 16-bit
- [ ] Agent 1 (Development): Step 1.4 — Buffer or stream chunks; add minimal CLI to run and output
- [ ] Agent 1 (Development): Step 1.5 — Add entitlements and microphone permission handling
- [ ] Agent 1 (Development): Step 1.6 — Document build, run, and verification steps
- [ ] Agent 1 (Development): Step 1.7 — Commit and push
- [ ] Agent 2 (Verification): Step 2.1 — Run pipeline and confirm audio chunks are produced
- [ ] Agent 2 (Verification): Step 2.2 — Verify format (16 kHz mono, 16-bit) and chunk size
- [ ] Agent 2 (Verification): Step 2.3 — Record outcomes and update Decision Log

---

## Surprises & Discoveries

*(None yet.)*

---

## Decision Log

- **Decision:** Use native Swift/AVAudioEngine for the audio capture spike.
  **Rationale:** Phase 0 used Swift for text injection; staying in Swift keeps the spike stack minimal. AVAudioEngine is the standard macOS API for real-time audio. The parent implementation plan recommends it. Electron + Node addon or Python process add complexity; can be explored in a later iteration.
  **Date/Author:** Initial plan.

- **Decision:** Output chunks to a file or stdout for verification.
  **Rationale:** Verification agent must observe that audio data is produced. Writing raw PCM to a file (or piping to stdout) allows inspection (e.g., `ffprobe`, or byte count). ASR integration is Phase 2.
  **Date/Author:** Initial plan.

---

## Outcomes & Retrospective

*(To be filled when complete.)*

---

## Context and Orientation

### Source Documents

- `capstone/voice-dictation/plan-of-work/phase-1-audio-capture-pipeline.md` — Original phase scope
- `capstone/voice-dictation/voice-dictation-macos-implementation-plan.md` — macOS architecture; AVAudioEngine, 16 kHz mono, 16-bit format
- `MULTI_AGENT_WORKFLOW_GUIDE.md` — Multi-agent ExecPlan structure

### What We Are Building

A pipeline that captures microphone input in real time and produces 16 kHz mono, 16-bit PCM chunks. Whisper and similar ASR models expect this format. The pipeline will run as a standalone tool or small app; Phase 2 will connect it to an ASR backend.

### Key Terms

- **AVAudioEngine:** AVFoundation API for real-time audio. `inputNode` provides microphone input; `installTap` captures buffers as they arrive.
- **16 kHz mono, 16-bit:** Common format for speech recognition. Sample rate 16000 Hz, one channel, 16-bit signed integer samples.
- **PCM:** Pulse-code modulation; raw audio samples without compression.
- **installTap:** Registers a callback that runs whenever a new audio buffer is available from the input node.

---

## Workflow Orchestration and Agent Coordination

### Initial Trigger (Human Action)

1. Ensure macOS with Xcode or Xcode Command Line Tools.
2. Ensure microphone is connected and working.
3. Create or confirm the spike directory: `capstone/voice-dictation/plan-of-work/phase-1-spike/`

### Agent Execution Sequence

**Agent 1 (Development) — Steps 1.1–1.6**

- Creates the spike project
- Implements AVAudioEngine capture, format conversion, chunk output
- Adds entitlements and microphone permission handling
- Documents build and run steps
- Commits to feature branch (e.g., `feature/phase-1-audio-capture-spike`)
- **Checkpoint:** Pipeline builds and runs; README documents how to run and what to expect

**Agent 2 (Verification) — Steps 2.1–2.3**

- Runs the pipeline, speaks into microphone
- Verifies chunks are produced and format is correct
- Documents outcomes, updates Progress
- **Checkpoint:** Acceptance criteria met; results documented

### Agent Communication Protocol

- Work is in Git. Development Agent pushes to feature branch; Verification Agent pulls and tests.
- Checkpoint = branch pushed with working pipeline and README.

### Work Tree Management

- Optional: `git worktree add /tmp/phase1-spike -b feature/phase-1-audio-capture-spike` for isolated work.
- Can also develop in main work tree.

### Error Handling and Recovery

- If microphone permission denied: User must grant in System Settings → Privacy & Security → Microphone. Document this.
- If AVAudioEngine produces zero samples: Ensure input node is connected; check format compatibility; see Surprises & Discoveries.
- Recovery: Re-run the pipeline; no persistent state. If crash, fix and rebuild.

### Automation Requirements

- Swift compiler (`swiftc` or `swift build`), Xcode CLI tools
- Git for version control

---

## Plan of Work

Create a minimal Swift project that:

1. Creates an `AVAudioEngine`, gets `inputNode`, installs a tap on bus 0
2. Converts or configures the input format to 16 kHz mono, 16-bit (or resamples if hardware uses different format)
3. Buffers or streams chunks (e.g., 2048 samples per chunk) and outputs them (file or stdout)
4. Handles microphone permission: request if needed, handle denial gracefully
5. Runs for a fixed duration (e.g., 5 seconds) or until interrupted, for verification

Provide a README with: prerequisites, how to build, how to run, expected output, how to verify format.

---

## Concrete Steps

### Agent 1 (Development)

**Step 1.1 — Create spike project directory and structure**

Working directory: repository root.

    mkdir -p capstone/voice-dictation/plan-of-work/phase-1-spike
    cd capstone/voice-dictation/plan-of-work/phase-1-spike

Create:

    phase-1-spike/
    ├── main.swift
    ├── README.md
    └── (optional) phase1spike.entitlements

**Step 1.2 — Implement AVAudioEngine capture with installTap**

In `main.swift`:

- Import `AVFoundation`
- Create `AVAudioEngine()`, access `engine.inputNode`
- Get `inputNode.inputFormat(forBus: 0)`
- Call `inputNode.installTap(onBus: 0, bufferSize: 2048, format: nil) { buffer, time in ... }`
- In the callback, process `buffer.floatChannelData` or `buffer.int16ChannelData` (format-dependent)
- Start the engine with `engine.prepare()` and `try engine.start()`

Expected: No compile errors; tap callback fires when microphone is active.

**Step 1.3 — Add format conversion to 16 kHz mono, 16-bit**

- If hardware format is not 16 kHz mono, use `AVAudioConverter` or a manual resample to 16000 Hz, 1 channel
- Convert samples to 16-bit signed integer (Int16)
- Output format: 16000 Hz, mono, 16-bit PCM

Expected: Chunks are valid 16 kHz mono 16-bit PCM.

**Step 1.4 — Buffer or stream chunks; add minimal CLI to run and output**

- Accumulate samples into chunks (e.g., 2048 or 4096 samples per chunk)
- Write raw PCM to a file (e.g., `output.raw`) or to stdout
- Add a run duration (e.g., 5 seconds) or signal handler for clean shutdown

Example run:

    ./audio-capture --duration 5 --output output.raw

Expected: File is created and grows while speaking; or bytes appear on stdout.

**Step 1.5 — Add entitlements and microphone permission handling**

- Create `phase1spike.entitlements` with `com.apple.security.device.audio-input` if building an app
- For CLI: macOS may prompt for microphone access; document that user must grant it
- Handle `AVAudioSession` or equivalent permission check; print clear message if denied

Expected: On first run, user is prompted for microphone access; after granting, capture works.

**Step 1.6 — Document build, run, and verification steps**

In `README.md`:

- Prerequisites (Xcode CLI tools, Swift)
- Build command, e.g. `swiftc -o audio-capture main.swift -framework AVFoundation -framework Foundation`
- Run command and expected behavior
- How to verify: e.g., `ls -la output.raw` shows non-zero size; `ffprobe -f s16le -ar 16000 -ac 1 output.raw` shows format
- Microphone permission note

**Step 1.7 — Commit and push (checkpoint)**

    git add capstone/voice-dictation/plan-of-work/phase-1-spike/
    git commit -m "Phase 1: Audio capture pipeline spike for macOS"
    git push origin <branch>

---

### Agent 2 (Verification)

**Step 2.1 — Run pipeline and confirm audio chunks are produced**

Working directory: `capstone/voice-dictation/plan-of-work/phase-1-spike/`

1. Build the pipeline (e.g., `swiftc -o audio-capture main.swift -framework AVFoundation -framework Foundation`)
2. Run with a short duration (e.g., 5 seconds)
3. Speak into the microphone during the run
4. Observe: output file exists and has non-zero size, or stdout receives bytes

Success: Audio data is produced. Failure: Zero bytes, or crash — document in Surprises & Discoveries.

**Step 2.2 — Verify format (16 kHz mono, 16-bit) and chunk size**

- Use `ffprobe` or similar to verify the output file is 16 kHz, mono, 16-bit
- Or: Inspect byte count; for 5 seconds at 16 kHz mono 16-bit: 16000 * 2 * 5 = 160000 bytes

    ffprobe -f s16le -ar 16000 -ac 1 -i output.raw

Expected: Format is reported correctly.

**Step 2.3 — Record outcomes and update Decision Log**

- Update Progress: mark all steps complete
- If issues found: add to Surprises & Discoveries with evidence
- Add Outcomes & Retrospective entry: what worked, what did not, recommendations for Phase 2

---

## Validation and Acceptance

**Agent 1 completion:** Pipeline builds and runs. README explains build, run, and verification. Code is committed and pushed.

**Agent 2 completion:** Running the pipeline while speaking produces non-zero audio output. Format is verified as 16 kHz mono, 16-bit. Outcomes documented.

**Functional acceptance:** A human can build the pipeline, run it for 5 seconds while speaking, and observe a file (or stdout) containing valid 16 kHz mono 16-bit PCM data. This proves the audio capture path is viable for the voice dictation app.

---

## Idempotence and Recovery

- Steps can be repeated. Re-running the pipeline overwrites the output file or produces new output.
- If the spike directory exists, overwriting and rebuilding is safe.
- To start fresh: `rm -rf capstone/voice-dictation/plan-of-work/phase-1-spike` and re-run from Step 1.1.
- Git: Create a new branch if the first attempt is abandoned.

---

## Artifacts and Notes

### File locations

| File | Path |
|------|------|
| Spike directory | `capstone/voice-dictation/plan-of-work/phase-1-spike/` |
| Main script | `capstone/voice-dictation/plan-of-work/phase-1-spike/main.swift` |
| README | `capstone/voice-dictation/plan-of-work/phase-1-spike/README.md` |

### Example success transcript

    $ cd capstone/voice-dictation/plan-of-work/phase-1-spike
    $ swiftc -o audio-capture main.swift -framework AVFoundation -framework Foundation
    $ ./audio-capture --duration 5 --output output.raw
    Recording for 5 seconds...
    Done. Wrote 160000 bytes to output.raw.
    $ ffprobe -f s16le -ar 16000 -ac 1 -i output.raw
    Input #0, s16le, from 'output.raw':
      Duration: 00:00:05.00
      Stream #0:0: Audio: pcm_s16le, 16000 Hz, mono

---

## Interfaces and Dependencies

**Frameworks:**

- `AVFoundation` — AVAudioEngine, AVAudioFormat, AVAudioConverter
- `Foundation` — File I/O, CLI parsing (or manual `CommandLine.arguments`)

**Key APIs:**

- `AVAudioEngine`, `engine.inputNode`
- `inputNode.installTap(onBus:bufferSize:format:block:)`
- `AVAudioFormat(standardFormatWithSampleRate:channels:)` for 16 kHz mono
- `AVAudioConverter` (if resampling needed)

**Output format:**

- 16000 Hz sample rate
- 1 channel (mono)
- 16-bit signed integer (Int16) PCM
