#!/usr/bin/env python3
"""
音声生成・動画合成スクリプト
Usage: python3 add_voice.py
Output: borderline-intelligence-with-voice.mp4
"""
import subprocess, wave
from pathlib import Path
import numpy as np

SCRIPT_DIR = Path(__file__).parent
VIDEO_IN   = SCRIPT_DIR / "borderline-intelligence.mp4"
VIDEO_OUT  = SCRIPT_DIR / "borderline-intelligence-with-voice.mp4"
TMP        = Path("/tmp/voice_segs")
TMP.mkdir(exist_ok=True)

SR    = 22050   # sample rate
HOLDS = [5,6,8,7,5,5,8,6,10,7,9,8,8,9,9,8,10]  # must match make_video.py
FADE  = 0.5                                       # cross-fade between slides

TEXTS = [
    # 1
    "境界知能は、7人に1人いる。最近、SNSやニュースでよく見かける数字だ。",
    # 2
    "この数字の正体、知ってますか？どこから来た数字なのか、少し立ち止まって考えてほしい。",
    # 3
    "境界知能というのは、IQがおよそ70から85の範囲にある状態のことだ。"
    "知的障害はIQ70未満。平均的な知能はIQ85以上。"
    "その間に位置する、グレーゾーンと呼ばれる領域だ。",
    # 4
    "IQは、平均を100、標準偏差を15として設計されている。"
    "正規分布に従う。IQ70から85の範囲には、数学的に全体の約13.6パーセントが収まる。",
    # 5
    "7人に1人は、この13.6パーセントから来ている。",
    # 6
    "ここで、一つ問いたい。この数字は、どうやって生まれたのか。",
    # 7
    "7人に1人という数字は。"
    "現実の中に存在していたものを、発見した数字なのか。"
    "それとも、カテゴリーを定義した結果として生まれた数字なのか。",
    # 8
    "答えは後者だ。調べて出てきた数字ではなく、定義によって導かれた数字だ。",
    # 9
    "IQを正規分布で設計した時点で、"
    "平均から1から2標準偏差下に収まる人の割合は、数学的にもう決まっていた。"
    "境界知能という名前を、その範囲につけた瞬間、"
    "7人に1人という数字は、自動的に確定した。",
    # 10
    "つまり、定義から数値、であって、発見から数値、ではない。",
    # 11
    "統計的なカテゴリーには、こういう順番がある。"
    "まず、どこかに線を引く、定義する。"
    "次に、線の内側に入る人を数える。"
    "そして、何人に1人がXだ、と言う。この順番が重要だ。",
    # 12
    "これは境界知能だけの話じゃない。"
    "高血圧の基準値、貧困線、BMIによる肥満の定義。"
    "全部、先に線を引いて、後から数えている。"
    "線の位置が変われば、有病率も変わる。",
    # 13
    "数字の作られ方を知らないまま受け取ると、"
    "数字が現実を映す鏡だと思い込んでしまう。"
    "でも実際には、定義が鏡の形を決めている。",
    # 14
    "境界知能のIQ85という上限は、なぜ85なのか。"
    "なぜ80ではなく、なぜ90でもなくて85なのか。"
    "その根拠を問えるかどうかが、統計リテラシーの核心にある。",
    # 15
    "統計を読むとき、一つ持っておくといい問いがある。"
    "この数字は、何をどう定義した結果か？",
    # 16
    "7人に1人という数字の重さを否定したいわけじゃない。"
    "ただ、その数字がカテゴリーの設計図から生まれた数字だと知っていれば、"
    "議論の地に足がつく。数値は先にこない。定義が先にある。",
    # 17
    "統計の見方が変わると、社会の議論の見え方も変わる。"
    "この動画が参考になったら、チャンネル登録と高評価お願いします。"
    "ブログ記事もプロフィールのリンクから読めるので、あわせてどうぞ。",
]

# ── helpers ──────────────────────────────────────────────────

def wav_to_arr(path):
    with wave.open(str(path), 'rb') as w:
        sr = w.getframerate(); ch = w.getnchannels()
        raw = w.readframes(w.getnframes())
    arr = np.frombuffer(raw, dtype=np.int16).astype(np.float32)
    if ch == 2:                          # stereo → mono
        arr = arr.reshape(-1, 2).mean(axis=1)
    if sr != SR:                         # resample
        n = int(len(arr) * SR / sr)
        arr = np.interp(np.linspace(0, len(arr), n), np.arange(len(arr)), arr)
    return arr

def arr_to_wav(arr, path):
    arr16 = np.clip(arr, -32768, 32767).astype(np.int16)
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(arr16.tobytes())

def silence(secs):
    return np.zeros(int(secs * SR), dtype=np.float32)

def fade_edges(arr, ms=80):
    n = int(ms / 1000 * SR)
    if len(arr) > n * 2:
        arr = arr.copy()
        arr[:n]  *= np.linspace(0, 1, n)
        arr[-n:] *= np.linspace(1, 0, n)
    return arr

# ── main ─────────────────────────────────────────────────────

def main():
    print("Generating speech...")
    segments = []

    for i, (text, hold) in enumerate(zip(TEXTS, HOLDS)):
        wav = TMP / f"seg{i:02d}.wav"
        subprocess.run(
            ["espeak-ng", "-v", "ja", "-s", "145", "-p", "52",
             "-a", "90", "-w", str(wav), text],
            check=True, capture_output=True
        )
        arr = wav_to_arr(wav)
        arr = fade_edges(arr)

        # Slot duration for this segment (hold + cross-fade to next, except last)
        slot = hold + (FADE if i < len(HOLDS) - 1 else 0)
        slot_n = int(slot * SR)

        if len(arr) < slot_n:
            arr = np.concatenate([arr, silence(slot - len(arr) / SR)])
        else:
            arr = arr[:slot_n]

        dur = len(arr) / SR
        print(f"  [{i+1:2d}/17] slot={slot:.1f}s  speech={dur:.1f}s")
        segments.append(arr)

    print("\nConcatenating audio...")
    full = np.concatenate(segments)
    audio_wav = TMP / "full.wav"
    arr_to_wav(full, audio_wav)

    print("Merging video + audio...")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(VIDEO_IN),
        "-i", str(audio_wav),
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "128k",
        "-shortest",
        str(VIDEO_OUT)
    ], check=True, stderr=subprocess.DEVNULL)

    mb = VIDEO_OUT.stat().st_size / 1024 / 1024
    print(f"\nDone → {VIDEO_OUT}  ({mb:.1f} MB)")

if __name__ == "__main__":
    main()
