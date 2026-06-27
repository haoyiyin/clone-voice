# Qwen3-TTS Voice Clone — Pi Agent Skill

> 🎙️ **Agent Skill** — Offline zero-shot voice cloning for AI coding agents.
> Drop a reference audio and some text. The agent speaks it back in that voice.
> Powered by Alibaba's [Qwen3-TTS 0.6B](https://github.com/QwenLM/Qwen3-TTS).

[![License](https://img.shields.io/badge/license-Apache%202.0-blue)](./LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Pi Agent Skill](https://img.shields.io/badge/Pi-Agent%20Skill-6c47ff)](https://github.com/earendil-works/pi-coding-agent)

---

## What is this?

This is a **[Pi](https://github.com/earendil-works/pi-coding-agent) agent skill**
that gives your coding agent the ability to clone voices offline. It wraps
Qwen3-TTS 0.6B into a single CLI command your agent can call:

```
User:  "Clone this voice and say: Hello world"
Agent: [runs clone_voice.py] → output.wav ✅
```

No cloud API keys. No GPUs required. Works on Mac, Linux, and Windows.

## Features

- 🎤 **Zero-shot voice cloning** — one reference audio sample, no fine-tuning
- 🌍 **10 languages** — Chinese, English, Japanese, Korean, German, French,
  Russian, Portuguese, Spanish, Italian (plus `Auto` detection)
- 💻 **CPU-friendly** — runs on CPU, MPS (Apple Silicon), or CUDA
- 📦 **Auto-download** — model (~1.2 GB) fetched from HuggingFace on first run
- 🧩 **Agent-native** — designed as a Pi skill; also usable standalone

## Quick Start

### 1. Install

```bash
# One-time setup
pip install qwen-tts soundfile transformers accelerate torch
```

### 2. Clone a voice

```bash
python .pi/skills/qwen3-tts-voice-clone/clone_voice.py \
  --reference speaker_sample.wav \
  --text "Hello, this is my cloned voice." \
  --output cloned.wav
```

### 3. First run downloads the model

The first invocation downloads ~1.2 GB of model weights from HuggingFace Hub.
This is one-time only. Subsequent runs are instant.

> **In China?** Set `HF_ENDPOINT=https://hf-mirror.com` before the first run.

## Agent Usage

When this skill is loaded, a Pi agent handles voice-clone requests
automatically:

| User says | Agent does |
|-----------|------------|
| "Clone this voice audio and say 你好世界" | Finds the audio file, runs `clone_voice.py`, returns the output |
| "Make this person say: I love coding" | Same flow, `--language English` |
| "用这个声音读这段话" | Same flow, Chinese auto-detected |

The agent follows the procedure defined in
[SKILL.md](./.pi/skills/qwen3-tts-voice-clone/SKILL.md).

## Hardware

| Platform | Backend | Speed |
|----------|---------|-------|
| macOS (Apple Silicon) | MPS | ⚡ Fast |
| Linux / Windows (NVIDIA) | CUDA (bfloat16) | ⚡⚡ Fastest |
| Any (CPU fallback) | CPU (float32) | 🐢 Slow (~5s audio / 30–60s) |

The script auto-detects the best available device.

## CLI Reference

```
usage: clone_voice.py [-h] --reference REFERENCE --text TEXT
                      [--output OUTPUT] [--language LANGUAGE]

options:
  -r, --reference   Path to reference audio (WAV, MP3, FLAC, etc.)
  -t, --text        Text to synthesize with the cloned voice
  -o, --output      Output WAV path (default: output.wav)
  -l, --language    Target language (default: Auto)
                    Choices: Auto, Chinese, English, Japanese, Korean,
                             German, French, Russian, Portuguese,
                             Spanish, Italian
```

## Reference Audio Tips

- **Duration**: ~10 seconds recommended (3s minimum)
- **Quality**: Clean, single speaker, minimal background noise
- **Format**: WAV, MP3, FLAC, or any format `soundfile` can read

## Tech Stack

| Component | Details |
|-----------|---------|
| Model | [Qwen/Qwen3-TTS-12Hz-0.6B-Base](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-0.6B-Base) |
| Framework | [Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS) (Apache 2.0) |
| Runtime | Python 3.10+, PyTorch, Transformers |
| Output | 24 kHz mono WAV |

## File Structure

```
clone-voice/
├── README.md
├── .pi/skills/qwen3-tts-voice-clone/
│   ├── SKILL.md           # Agent skill specification
│   ├── clone_voice.py     # CLI inference script
│   └── requirements.txt   # Python dependencies
```

## License

This project is released under the Apache 2.0 license, matching the upstream
[Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS) license.
