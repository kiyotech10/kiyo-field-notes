#!/usr/bin/env python3
"""
汎用 音声生成・動画合成スクリプト (pyopenjtalk / mei女性音声版)
Usage:
  python3 add_voice_generic.py <article_name>
  例: python3 add_voice_generic.py burnout
      python3 add_voice_generic.py musenmai

<article_name> に対応する make_video_<article_name>.py と
<article_name>_texts.py が必要。

texts.py の形式:
  TEXTS = ["スライド1のナレーション", "スライド2のナレーション", ...]
  OUTPUT = "output_video_name.mp4"  # オプション（省略時は article_name.mp4）
"""
import sys, wave
from pathlib import Path
import numpy as np
import subprocess
import importlib.util

SCRIPT_DIR = Path(__file__).parent
TMP        = Path("/tmp/voice_segs")
TMP.mkdir(exist_ok=True)

# ── TTS settings ─────────────────────────────────────────────
SPEED     = 1.05
HALF_TONE = 0.0

# ── Video settings ───────────────────────────────────────────
W, H    = 1920, 1080
FPS     = 30
FADE    = 15
MIN_HOLD = 2.5

# ── Audio helpers ─────────────────────────────────────────────

def speak(text):
    import pyopenjtalk
    x, sr = pyopenjtalk.tts(text, speed=SPEED, half_tone=HALF_TONE)
    return np.array(x, dtype=np.float32), sr

def trim_leading_silence(arr, sr, threshold=600, pad_ms=80):
    for i in range(len(arr)):
        if abs(arr[i]) > threshold:
            keep = max(0, i - int(pad_ms / 1000 * sr))
            return arr[keep:]
    return arr

def normalize(arr, target=29000):
    peak = np.abs(arr).max()
    return arr * (target / peak) if peak > 0 else arr

def fade_edges(arr, sr, ms=40):
    n = int(ms / 1000 * sr)
    if len(arr) > n * 2:
        arr = arr.copy()
        arr[:n]  *= np.linspace(0, 1, n)
        arr[-n:] *= np.linspace(1, 0, n)
    return arr

def silence(secs, sr):
    return np.zeros(int(secs * sr), dtype=np.float32)

def arr_to_wav(arr, sr, path):
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(np.clip(arr, -32768, 32767).astype(np.int16).tobytes())

def load_module(path):
    spec = importlib.util.spec_from_file_location("mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

# ── Main ──────────────────────────────────────────────────────

def main(article_name):
    # ── テキスト読み込み ──────────────────────────────────────
    texts_path = SCRIPT_DIR / f"{article_name}_texts.py"
    if not texts_path.exists():
        print(f"ERROR: {texts_path} が見つかりません")
        print("各スライドのナレーションテキストを定義した _texts.py が必要です")
        sys.exit(1)

    texts_mod = load_module(texts_path)
    TEXTS = texts_mod.TEXTS
    output_name = getattr(texts_mod, "OUTPUT", f"{article_name}-with-voice.mp4")
    VIDEO_OUT = SCRIPT_DIR / output_name

    # ── make_video モジュール読み込み ────────────────────────
    mv_path = SCRIPT_DIR / f"make_video_{article_name}.py"
    if not mv_path.exists():
        print(f"ERROR: {mv_path} が見つかりません")
        sys.exit(1)
    mv = load_module(mv_path)
    SLIDES = mv.SLIDES

    if len(TEXTS) != len(SLIDES):
        print(f"WARNING: TEXTS({len(TEXTS)}) と SLIDES({len(SLIDES)}) の数が一致しません")

    # ── 1. 音声生成 ──────────────────────────────────────────
    print(f"Generating speech for '{article_name}' ({len(TEXTS)} slides)...")
    speech_data = []
    for i, text in enumerate(TEXTS):
        arr, sr = speak(text)
        arr = trim_leading_silence(arr, sr)
        arr = normalize(arr)
        arr = fade_edges(arr, sr)
        dur = len(arr) / sr
        speech_data.append((arr, sr, dur))
        sys.stdout.write(f"  [{i+1:2d}/{len(TEXTS)}] {dur:.1f}s\n")
        sys.stdout.flush()

    # ── 2. スライド尺を音声長に合わせて決定 ─────────────────
    holds = [max(d + 0.4, MIN_HOLD) for _, _, d in speech_data]
    holds[-1] += 1.0

    # ── 3. 映像生成 ──────────────────────────────────────────
    print("\nGenerating video slides...")
    from video_engine import RENDERERS, W as VW, H as VH, FPS as VFPS, FADE as VFADE
    images = []
    for i, slide in enumerate(SLIDES):
        from video_engine import RENDERERS
        typ = slide.get("type", "STATEMENT")
        renderer = RENDERERS.get(typ)
        if renderer is None:
            from video_engine import render_STATEMENT
            renderer = render_STATEMENT
        images.append(np.array(renderer(slide)))
        sys.stdout.write(f"  Slide {i+1}/{len(SLIDES)}\r"); sys.stdout.flush()
    print()

    silent_mp4 = TMP / f"{article_name}_silent.mp4"
    enc = subprocess.Popen([
        "ffmpeg", "-y", "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{W}x{H}", "-pix_fmt", "rgb24", "-r", str(FPS),
        "-i", "pipe:0",
        "-vcodec", "libx264", "-pix_fmt", "yuv420p",
        "-crf", "20", "-preset", "fast", str(silent_mp4)
    ], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    n_slides = min(len(images), len(holds))
    for i in range(n_slides):
        raw = images[i].tobytes()
        for _ in range(int(holds[i] * FPS)):
            enc.stdin.write(raw)
        if i < n_slides - 1:
            nxt = images[i + 1]
            for fi in range(FADE):
                a = fi / FADE
                bl = ((1 - a) * images[i] + a * nxt).astype(np.uint8)
                enc.stdin.write(bl.tobytes())
    enc.stdin.close(); enc.wait()

    # ── 4. 音声トラック構築 ──────────────────────────────────
    print("Building audio track...")
    all_segs = []
    for i, ((arr, sr, dur), hold) in enumerate(zip(speech_data, holds)):
        slot = hold + (FADE / FPS if i < len(holds) - 1 else 0)
        n = int(slot * sr)
        if len(arr) < n:
            arr = np.concatenate([arr, silence(slot - len(arr) / sr, sr)])
        else:
            arr = arr[:n]
        all_segs.append(arr)

    full = np.concatenate(all_segs)
    full = normalize(full, target=29000)
    sr_out = speech_data[0][1]
    audio_wav = TMP / f"{article_name}_audio.wav"
    arr_to_wav(full, sr_out, audio_wav)

    # ── 5. 映像＋音声を合成 ──────────────────────────────────
    print("Merging video + audio...")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(silent_mp4),
        "-i", str(audio_wav),
        "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
        "-shortest", str(VIDEO_OUT)
    ], check=True, stderr=subprocess.DEVNULL)

    total = sum(holds) + (len(holds) - 1) * FADE / FPS
    mb = VIDEO_OUT.stat().st_size / 1024 / 1024
    print(f"\nDone → {VIDEO_OUT}")
    print(f"Duration: {total:.0f}s ({total/60:.1f}min)  Size: {mb:.1f}MB")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 add_voice_generic.py <article_name>")
        print("例: python3 add_voice_generic.py burnout")
        sys.exit(1)
    main(sys.argv[1])
