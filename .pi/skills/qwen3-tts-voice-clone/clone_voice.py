#!/usr/bin/env python3
"""
Qwen3-TTS 0.6B Offline Voice Cloning CLI

Zero-shot voice cloning: extracts speaker timbre from a reference audio file
and synthesizes new speech matching that voice.

Usage:
    python clone_voice.py --reference speaker.wav --text "Hello world" --output out.wav
    python clone_voice.py -r voice.mp3 -t "你好世界" -l Chinese -o out.wav

First run auto-downloads ~1.2 GB model from HuggingFace Hub.

Hardware: CUDA (fastest) > MPS (Apple Silicon) > CPU (fallback).
"""

import argparse
import os
import sys

import soundfile as sf
import torch
from qwen_tts import Qwen3TTSModel

MODEL_ID = "Qwen/Qwen3-TTS-12Hz-0.6B-Base"

# All languages supported by the 0.6B Base model
SUPPORTED_LANGUAGES = [
    "Auto",
    "Chinese",
    "English",
    "Japanese",
    "Korean",
    "German",
    "French",
    "Russian",
    "Portuguese",
    "Spanish",
    "Italian",
]


def detect_device():
    """Return (device_map, dtype) for the best available hardware."""
    if torch.cuda.is_available():
        return "cuda:0", torch.bfloat16
    if torch.backends.mps.is_available():
        return "mps", torch.float32
    return "cpu", torch.float32


def main():
    parser = argparse.ArgumentParser(description="Qwen3-TTS 0.6B Offline Voice Cloning")
    parser.add_argument(
        "--reference",
        "-r",
        required=True,
        help="Path to reference audio file (WAV, MP3, FLAC, etc.)",
    )
    parser.add_argument(
        "--text",
        "-t",
        required=True,
        help="Text to synthesize with the cloned voice",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="output.wav",
        help="Output audio file path (default: output.wav)",
    )
    parser.add_argument(
        "--language",
        "-l",
        default="Auto",
        choices=SUPPORTED_LANGUAGES,
        help="Target language (default: Auto-detect)",
    )
    args = parser.parse_args()

    # Validate reference audio exists
    if not os.path.exists(args.reference):
        print(f"Error: reference audio not found: {args.reference}", file=sys.stderr)
        sys.exit(1)

    # Detect best device
    device, dtype = detect_device()
    print(f"Device: {device}  |  Dtype: {dtype}")

    # Load model (auto-downloads on first run)
    print(f"Loading model '{MODEL_ID}'...")
    print("(first run downloads ~1.2 GB — this is one-time only)")
    model = Qwen3TTSModel.from_pretrained(
        MODEL_ID,
        device_map=device,
        dtype=dtype,
    )

    # Generate cloned speech
    print(f"Reference : {args.reference}")
    print(f"Text      : {args.text}")
    print(f"Language  : {args.language}")
    print("Generating...")

    wavs, sr = model.generate_voice_clone(
        text=args.text,
        language=args.language,
        ref_audio=args.reference,
        x_vector_only_mode=True,  # no reference transcript needed
    )

    # Write output
    sf.write(args.output, wavs[0], sr)
    duration = len(wavs[0]) / sr
    print(f"Done! → {args.output}")
    print(f"  Sample rate : {sr} Hz")
    print(f"  Duration    : {duration:.2f}s")
    print(f"  Channels    : {1 if wavs[0].ndim == 1 else wavs[0].shape[1]}")


if __name__ == "__main__":
    main()
