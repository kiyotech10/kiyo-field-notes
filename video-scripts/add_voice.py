#!/usr/bin/env python3
"""
音声生成・動画合成スクリプト (pyopenjtalk / mei女性音声版)
Usage: python3 add_voice.py
Output: borderline-intelligence-with-voice.mp4
"""
import wave, sys
from pathlib import Path
import numpy as np
import pyopenjtalk
import subprocess

SCRIPT_DIR = Path(__file__).parent
VIDEO_OUT  = SCRIPT_DIR / "borderline-intelligence-with-voice.mp4"
TMP        = Path("/tmp/voice_segs")
TMP.mkdir(exist_ok=True)

# ── TTS settings ─────────────────────────────────────────────
SPEED     = 1.05   # 1.0=普通, 1.1=少し速め
HALF_TONE = 0.0    # ピッチ調整（半音単位, 0=デフォルト）

# ── Video settings (make_video.py と一致させること) ───────────
W, H   = 1920, 1080
FPS    = 30
FADE   = 15        # slides間のフェードフレーム数
MIN_HOLD = 2.5     # スライド最低表示秒数

# ── Narration ────────────────────────────────────────────────
TEXTS = [
    # 1 HOOK
    "境界知能は、7人に1人いる。"
    "最近、SNSやニュースでよく見かける数字だ。",
    # 2 HOOK2
    "この数字の正体、知ってますか？"
    "どこから来た数字なのか、少し立ち止まって考えてほしい。",
    # 3 DEFINITION
    "境界知能というのは、IQがおよそ70から85の範囲にある状態のことだ。"
    "知的障害はIQ70未満。平均的な知能はIQ85以上。"
    "その間に位置する、グレーゾーンと呼ばれる領域だ。",
    # 4 MATH
    "IQは、平均を100、標準偏差を15として設計されている。"
    "正規分布に従うため、IQ70から85の範囲には"
    "数学的に全体の約13.6パーセントが収まる。",
    # 5 7IN1
    "7人に1人は、この13.6パーセントから来ている。",
    # 6 PIVOT
    "ここで、一つ問いたい。"
    "この数字は、どうやって生まれたのか。",
    # 7 VS
    "7人に1人という数字は。"
    "現実の中に存在していたものを、発見した数字なのか。"
    "それとも、カテゴリーを定義した結果として生まれた数字なのか。",
    # 8 ANSWER
    "答えは、後者だ。"
    "調べて出てきた数字ではなく、定義によって導かれた数字だ。",
    # 9 MECHANISM
    "IQを正規分布で設計した時点で、"
    "平均から1から2標準偏差下に収まる人の割合は、数学的にもう決まっていた。"
    "境界知能という名前を、その範囲につけた瞬間、"
    "7人に1人という数字は、自動的に確定した。",
    # 10 STRUCTURE
    "つまり、定義から数値、であって、発見から数値、ではない。",
    # 11 STEPS
    "統計的なカテゴリーには、こういう順番がある。"
    "まず、どこかに線を引く、定義する。"
    "次に、線の内側に入る人を数える。"
    "そして、何人に1人がXだ、と言う。"
    "この順番が重要だ。",
    # 12 EXAMPLES
    "これは境界知能だけの話じゃない。"
    "高血圧の基準値、貧困線、BMIによる肥満の定義。"
    "全部、先に線を引いて、後から数えている。"
    "線の位置が変われば、有病率も変わる。",
    # 13 TRAP
    "数字の作られ方を知らないまま受け取ると、"
    "数字が現実を映す鏡だと思い込んでしまう。"
    "でも実際には、定義が鏡の形を決めている。",
    # 14 WHY85
    "境界知能のIQ85という上限は、なぜ85なのか。"
    "なぜ80ではなく、なぜ90でもなくて、85なのか。"
    "その根拠を問えるかどうかが、統計リテラシーの核心にある。",
    # 15 QUESTION
    "統計を読むとき、一つ持っておくといい問いがある。"
    "この数字は、何をどう定義した結果か？",
    # 16 CONCLUSION
    "7人に1人という数字の重さを、否定したいわけじゃない。"
    "ただ、その数字がカテゴリーの設計図から生まれた数字だと知っていれば、"
    "議論の地に足がつく。"
    "数値は先にこない。定義が先にある。",
    # 17 OUTRO
    "統計の見方が変わると、社会の議論の見え方も変わる。"
    "この動画が参考になったら、チャンネル登録と高評価お願いします。"
    "ブログ記事もプロフィールのリンクから読めるので、あわせてどうぞ。",
]

# ── Audio helpers ─────────────────────────────────────────────

def speak(text):
    """pyopenjtalk (mei女性音声) で合成 → float32配列とSRを返す"""
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

# ── Main ──────────────────────────────────────────────────────

def main():
    # ── 1. 全スライドの音声を生成 ──────────────────────────────
    print("Generating speech (mei / female)...")
    speech_data = []   # list of (arr, sr, dur)

    for i, text in enumerate(TEXTS):
        arr, sr = speak(text)
        arr = trim_leading_silence(arr, sr)
        arr = normalize(arr)
        arr = fade_edges(arr, sr)
        dur = len(arr) / sr
        speech_data.append((arr, sr, dur))
        sys.stdout.write(f"  [{i+1:2d}/17] {dur:.1f}s\n")
        sys.stdout.flush()

    # ── 2. スライド尺を音声長に合わせて決定 ────────────────────
    holds = [max(d + 0.4, MIN_HOLD) for _, _, d in speech_data]
    holds[-1] += 1.0   # 最後のスライドは余韻を長めに

    # ── 3. 映像を再生成 ────────────────────────────────────────
    print("\nRegenerating video slides...")
    import importlib.util
    spec = importlib.util.spec_from_file_location("make_video", SCRIPT_DIR / "make_video.py")
    mv = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mv)

    images = []
    for i, (fn, _) in enumerate(mv.SLIDES):
        sys.stdout.write(f"  Slide {i+1}/17\r"); sys.stdout.flush()
        images.append(np.array(fn()))
    print()

    silent_mp4 = TMP / "silent.mp4"
    enc = subprocess.Popen([
        "ffmpeg", "-y", "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", f"{mv.W}x{mv.H}", "-pix_fmt", "rgb24", "-r", str(mv.FPS),
        "-i", "pipe:0",
        "-vcodec", "libx264", "-pix_fmt", "yuv420p",
        "-crf", "20", "-preset", "fast", str(silent_mp4)
    ], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

    for i, (img, hold) in enumerate(zip(images, holds)):
        raw = img.tobytes()
        for _ in range(int(hold * mv.FPS)):
            enc.stdin.write(raw)
        if i < len(images) - 1:
            nxt = images[i + 1]
            for fi in range(FADE):
                a = fi / FADE
                bl = ((1 - a) * img + a * nxt).astype(np.uint8)
                enc.stdin.write(bl.tobytes())
    enc.stdin.close(); enc.wait()

    # ── 4. 音声トラック構築 ────────────────────────────────────
    print("Building audio track...")
    all_segs = []
    for i, ((arr, sr, dur), hold) in enumerate(zip(speech_data, holds)):
        slot = hold + (FADE / mv.FPS if i < len(holds) - 1 else 0)
        n = int(slot * sr)
        if len(arr) < n:
            arr = np.concatenate([arr, silence(slot - len(arr) / sr, sr)])
        else:
            arr = arr[:n]
        all_segs.append(arr)

    full = np.concatenate(all_segs)
    full = normalize(full, target=29000)

    sr_out = speech_data[0][1]   # 全セグメント同SR
    audio_wav = TMP / "full_audio.wav"
    arr_to_wav(full, sr_out, audio_wav)

    # ── 5. 映像＋音声を合成 ────────────────────────────────────
    print("Merging video + audio...")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(silent_mp4),
        "-i", str(audio_wav),
        "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
        "-shortest", str(VIDEO_OUT)
    ], check=True, stderr=subprocess.DEVNULL)

    total = sum(holds) + (len(holds) - 1) * FADE / mv.FPS
    mb = VIDEO_OUT.stat().st_size / 1024 / 1024
    print(f"\nDone → {VIDEO_OUT}")
    print(f"Duration: {total:.0f}s ({total/60:.1f}min)  Size: {mb:.1f}MB")

if __name__ == "__main__":
    main()
