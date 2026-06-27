---
name: qwen3-tts-voice-clone
description: >-
  Offline zero-shot voice cloning. Provide a reference audio sample and target
  text — outputs a WAV file in the cloned voice. No GPU required.
version: 2
language: python
---

# Qwen3-TTS Voice Cloning (0.6B)

Zero-shot offline voice cloning powered by Alibaba's
[Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS) 0.6B model.

## When to Use

- User provides a reference voice sample (`.wav`, `.mp3`, `.flac`) + target text
- User asks to "clone my voice", "模仿这个声音说话", "声音克隆", "make X say Y"
- Offline / local-only operation is required — no cloud API calls
- Target languages: Chinese, English, Japanese, Korean, German, French,
  Russian, Portuguese, Spanish, Italian (+ `Auto` detection)

### Boundaries

- Does **not** handle video input — user must extract audio first
- Does **not** require the reference audio transcript (x_vector_only_mode)
- Reference audio: ideally ~10 seconds, clean, single speaker
- Quality is lower than the 1.7B model, but runs on consumer hardware

## Hardware

| Platform | Backend | Speed |
|----------|---------|-------|
| macOS (Apple Silicon) | MPS | Fast |
| Linux / Windows (NVIDIA) | CUDA (bfloat16) | Fastest |
| Any (CPU fallback) | CPU (float32) | Slow |

Auto-detected: CUDA → MPS → CPU.

## Procedure

### 1. Install dependencies

```bash
pip install qwen-tts soundfile transformers accelerate torch
```

FlashAttention 2 is optional (CUDA only):

```bash
pip install flash-attn --no-build-isolation
```

### 2. Run voice clone

```bash
python skill/clone_voice.py \
  --reference /path/to/speaker_sample.wav \
  --text "Hello, this is my cloned voice." \
  --output cloned.wav
```

| Flag | Default | Description |
|------|---------|-------------|
| `-r`, `--reference` | *(required)* | Path to reference audio |
| `-t`, `--text` | *(required)* | Text to synthesize |
| `-o`, `--output` | `output.wav` | Output file path |
| `-l`, `--language` | `Auto` | Target language (see list above) |

First run downloads ~1.2 GB model from HuggingFace Hub — one-time only.

> **China users**: Set `HF_ENDPOINT=https://hf-mirror.com` before first run.

## Agent Integration

This skill can be loaded by any AI coding agent (Pi, Cursor, Copilot, etc.).
When loaded, the agent should:

1. Check `python3 --version` ≥ 3.10
2. Ensure dependencies installed: `pip install qwen-tts soundfile transformers accelerate torch`
3. Locate the reference audio from user's message
4. Run: `python skill/clone_voice.py -r <audio> -t <text> -o <out.wav> [-l <lang>]`
5. Report the output file path and duration

## Pitfalls

- **First-run download**: ~1.2 GB from HuggingFace — 5–15 minutes. Warn the user.
- **CPU is slow**: ~5s of speech takes 30–60s. Set expectations.
- **FlashAttention macOS**: `flash-attn` is CUDA-only; skip on macOS.
- **Long text** (>200 chars): may OOM on 8GB. Split into sentences.
- **Poor reference audio**: noisy, multi-speaker, or <3s samples produce bad
  results. Use clean 10s+ single-speaker audio.
- **Python version**: requires 3.10+. Run `python3 --version` first.

## Verification

- [ ] Output `.wav` file exists and is >1 KB
- [ ] Audio has recognizable speaker characteristics from reference
- [ ] Sample rate is 24000 Hz
- [ ] No Python traceback or CUDA/MPS errors in stderr
