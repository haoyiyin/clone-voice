---
name: qwen3-tts-voice-clone
description: >-
  Offline voice cloning using Qwen3-TTS 0.6B. Provide a reference audio sample
  and target text — outputs a cloned-voice WAV file. No GPU required (works on
  CPU, MPS, CUDA). Models auto-download from HuggingFace on first run.
---

# Qwen3-TTS Voice Cloning (0.6B)

Zero-shot offline voice cloning powered by Alibaba's Qwen3-TTS 0.6B model.
Provide a reference voice sample and the text you want it to speak — the tool
extracts the speaker's timbre and synthesizes matching speech.

## When to Use

- User wants to clone a voice from a `.wav` / `.mp3` / `.flac` audio file
- User provides a reference audio sample and target text (台词)
- User asks to "clone my voice", "模仿这个声音说话", "声音克隆"
- Offline / local-only operation is required (no cloud API calls)
- Target languages: Chinese, English, Japanese, Korean, German, French,
  Russian, Portuguese, Spanish, Italian

### Boundaries

- This skill does NOT handle video input — user must extract audio first
- This skill does NOT require the reference audio transcript (uses
  x_vector_only_mode)
- Reference audio should ideally be ~10 seconds, clean speech
- Quality is lower than the 1.7B model but runs on consumer hardware

## Hardware Support

| Platform | Device    | Speed   |
|----------|-----------|---------|
| macOS (Apple Silicon) | MPS       | Fast    |
| Linux / Windows (NVIDIA) | CUDA     | Fastest |
| Any (CPU fallback)  | CPU       | Slow    |

The script auto-detects the best available device: CUDA → MPS → CPU.

## Procedure

### Step 1: Install dependencies

```bash
pip install qwen-tts soundfile transformers accelerate torch
```

FlashAttention 2 is optional (CUDA only, for speed):

```bash
pip install flash-attn --no-build-isolation
```

### Step 2: Run the voice clone

Use the bundled `clone_voice.py` script located at this skill's directory:

```bash
python .pi/skills/qwen3-tts-voice-clone/clone_voice.py \
  --reference /path/to/speaker_sample.wav \
  --text "你好，这是克隆的声音。" \
  --output cloned_output.wav
```

Or let the agent invoke it — the agent should:

1. Locate `clone_voice.py` at the skill directory
2. Run it with the user's reference audio and text
3. Return the output file path to the user

### Language Control

- `--language Auto` (default) — auto-detects from text
- `--language Chinese` — force Chinese
- `--language English` — force English
- Also supports: Japanese, Korean, German, French, Russian, Portuguese,
  Spanish, Italian

### Agent Invocation Pattern

When the user says "克隆这个声音说：XXX":

1. Ensure `pip install qwen-tts soundfile transformers accelerate` has run
2. Find the reference audio file from user's message
3. Run:

   ```
   python .pi/skills/qwen3-tts-voice-clone/clone_voice.py --reference <audio> --text <台词> --output <output.wav>
   ```

4. Report the output file path and playable duration

First run will download ~1.2 GB of model files from HuggingFace — this is
one-time only.

## Pitfalls

- **First-run download**: The model (~1.2 GB) is downloaded from HuggingFace
  Hub on first use. This can take 5–15 minutes depending on network. Inform the
  user.
- **CPU is slow**: On CPU-only machines, generating 5 seconds of speech can
  take 30–60 seconds. Set expectations.
- **FlashAttention macOS**: `flash-attn` does NOT install on macOS. The script
  skips it automatically — it is CUDA-only.
- **Long text**: Very long text (>200 chars) may OOM on 8GB machines. Split
  into sentences and concatenate.
- **Reference audio quality**: Noisy, multi-speaker, or very short (<3s)
  reference audio produces poor cloning. Recommend clean, single-speaker, 10s+
  samples.
- **Python version**: Requires Python 3.10+. Check `python3 --version` before
  installing.

## Verification

- Output `.wav` file exists and is non-empty (>1 KB)
- Audio plays back with recognizable speaker characteristics from the reference
- Sample rate is 24000 Hz (verify with `ffprobe output.wav`)
- No Python traceback or CUDA/MPS errors in stderr
