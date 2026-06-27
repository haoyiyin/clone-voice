# Qwen3-TTS Voice Clone — Agent Skill

> 🎙️ **Agent Skill** — Offline zero-shot voice cloning for AI coding agents.
> Drop a reference audio and some text. It speaks back in that voice.
> Powered by Alibaba's [Qwen3-TTS 0.6B](https://github.com/QwenLM/Qwen3-TTS).

[![License](https://img.shields.io/badge/license-Apache%202.0-blue)](./LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Agent Skill](https://img.shields.io/badge/type-Agent%20Skill-6c47ff)](https://github.com/haoyiyin/clone-voice)

---

## What is this?

An **agent skill** — a self-contained module that gives any AI coding agent the
ability to clone voices offline. Wraps Qwen3-TTS 0.6B into a single CLI command:

```
User:  "Clone this voice and say: Hello world"
Agent: [runs skill/clone_voice.py] → output.wav ✅
```

No cloud API keys. No GPUs required. Works on Mac, Linux, and Windows.

Compatible with any agent platform — **Pi**, **Cursor**, **Copilot**, **Claude Code**, etc.

## Features

- 🎤 **Zero-shot voice cloning** — one reference audio sample, no fine-tuning
- 🌍 **10 languages** — Chinese, English, Japanese, Korean, German, French,
  Russian, Portuguese, Spanish, Italian (+ `Auto` detection)
- 💻 **CPU-friendly** — runs on CPU, MPS (Apple Silicon), or CUDA
- 📦 **Auto-download** — model (~1.2 GB) fetched from HuggingFace on first run
- 🧩 **Agent-agnostic** — works with any agent that can run shell commands

## Quick Start

### 1. Install

```bash
# One-time setup
pip install qwen-tts soundfile transformers accelerate torch
```

### 2. Clone a voice

```bash
python skill/clone_voice.py \
  --reference speaker_sample.wav \
  --text "Hello, this is my cloned voice." \
  --output cloned.wav
```

### 3. First run downloads the model

The first invocation downloads ~1.2 GB of model weights from HuggingFace Hub.
One-time only.

> **In China?** Set `HF_ENDPOINT=https://hf-mirror.com` before the first run.

## Agent Usage

Load this skill into your agent. When a user asks for voice cloning, the agent
follows the specification in [`skill/SKILL.md`](./skill/SKILL.md):

| User says | Agent does |
|-----------|------------|
| "Clone this voice and say: 你好世界" | Finds the audio, runs `skill/clone_voice.py`, returns the output |
| "Make this person say: I love coding" | Same flow, `--language English` |
| "用这个声音读这段话" | Same, Chinese auto-detected |

## Hardware

| Platform | Backend | Speed |
|----------|---------|-------|
| macOS (Apple Silicon) | MPS | ⚡ Fast |
| Linux / Windows (NVIDIA) | CUDA (bfloat16) | ⚡⚡ Fastest |
| Any (CPU fallback) | CPU (float32) | 🐢 Slow (~30–60s per 5s audio) |

Auto-detected at runtime.

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
- **Format**: WAV, MP3, FLAC — anything `soundfile` can read

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
├── skill/
│   ├── SKILL.md           # Agent skill specification
│   ├── clone_voice.py     # CLI inference script
│   └── requirements.txt   # Python dependencies
└── .gitignore
```

## License

Apache 2.0 — matching the upstream [Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS) license.
