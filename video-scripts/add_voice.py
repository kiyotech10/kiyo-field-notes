#!/usr/bin/env python3
"""
音声生成・動画合成スクリプト (open-jtalk版)
Usage: python3 add_voice.py
Output: borderline-intelligence-with-voice.mp4
"""
import subprocess, wave, sys
from pathlib import Path
import numpy as np

SCRIPT_DIR = Path(__file__).parent
VIDEO_OUT  = SCRIPT_DIR / "borderline-intelligence-with-voice.mp4"
TMP        = Path("/tmp/voice_segs")
TMP.mkdir(exist_ok=True)

# open-jtalk settings
DIC   = "/var/lib/mecab/dic/open-jtalk/naist-jdic"
VOICE = "/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice"
RATE  = "0.95"   # speaking rate (1.0=normal, 0.9=slow)
PITCH = "120"    # base frequency Hz

W, H  = 1920, 1080
FPS   = 30
FADE  = 15        # fade frames between slides
SR    = 48000     # open-jtalk actual output SR (auto-detected below)
MIN_HOLD = 3      # minimum slide hold (seconds)

# ── Narration texts ───────────────────────────────────────────
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

def speak(text, out_wav):
    proc = subprocess.run(
        ["open_jtalk",
         "-x", DIC, "-m", VOICE,
         "-r", RATE, "-fm", PITCH,
         "-u", "0.3",
         "-ow", str(out_wav)],
        input=text.encode("utf-8"),
        capture_output=True
    )
    if proc.returncode != 0:
        raise RuntimeError(f"open_jtalk failed: {proc.stderr.decode()}")

def wav_to_arr(path):
    with wave.open(str(path), "rb") as w:
        sr = w.getframerate(); ch = w.getnchannels()
        raw = w.readframes(w.getnframes())
    arr = np.frombuffer(raw, dtype=np.int16).astype(np.float32)
    if ch == 2:
        arr = arr.reshape(-1, 2).mean(axis=1)
    return arr, sr

def arr_to_wav(arr, sr, path):
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(np.clip(arr, -32768, 32767).astype(np.int16).tobytes())

def trim_leading_silence(arr, sr, threshold=600, pad_ms=80):
    """先頭の無音を除去し pad_ms だけ残す"""
    for i in range(len(arr)):
        if abs(arr[i]) > threshold:
            keep = max(0, i - int(pad_ms / 1000 * sr))
            return arr[keep:]
    return arr

def normalize(arr, target=29000):
    """ピークを target (≈90% of 32768) に正規化"""
    peak = np.abs(arr).max()
    if peak > 0:
        arr = arr * (target / peak)
    return arr

def fade_in_out(arr, ms=40):
    n = int(ms / 1000 * SR)
    if len(arr) > n * 2:
        arr = arr.copy()
        arr[:n]  *= np.linspace(0, 1, n)
        arr[-n:] *= np.linspace(1, 0, n)
    return arr

def silence(secs, sr):
    return np.zeros(int(secs * sr), dtype=np.float32)

# ── Video helpers (same logic as make_video.py) ───────────────
# Import slide generators from make_video.py
import importlib.util, os
_spec = importlib.util.spec_from_file_location("make_video", SCRIPT_DIR / "make_video.py")
_mv   = importlib.util.load_from_spec(_spec) if False else None  # lazy

def get_slide_images():
    spec = importlib.util.spec_from_file_location("make_video", SCRIPT_DIR / "make_video.py")
    mv = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mv)
    return [(fn, hold) for fn, hold in mv.SLIDES], mv

# ── Main ──────────────────────────────────────────────────────

def main():
    # 1. Generate speech for all slides
    print("Generating speech with open-jtalk...")
    speech_arrs = []
    speech_secs = []
    for i, text in enumerate(TEXTS):
        wav = TMP / f"seg{i:02d}.wav"
        speak(text, wav)
        arr, sr = wav_to_arr(wav)
        arr = trim_leading_silence(arr, sr)
        arr = normalize(arr)
        arr = fade_in_out(arr)
        speech_arrs.append((arr, sr))
        dur = len(arr) / sr
        speech_secs.append(dur)
        sys.stdout.write(f"  [{i+1:2d}/17] {dur:.1f}s  \"{text[:22]}...\"\n")
        sys.stdout.flush()

    # 2. Determine hold time per slide = max(speech_dur + 0.3s buffer, MIN_HOLD)
    holds = [max(s + 0.3, MIN_HOLD) for s in speech_secs]
    holds[-1] = max(holds[-1], speech_secs[-1] + 1.0)  # extra pause at end

    # 3. Regenerate video with new hold times
    print("\nRegenerating video with speech-adjusted timing...")
    spec = importlib.util.spec_from_file_location("make_video", SCRIPT_DIR / "make_video.py")
    mv = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mv)

    slide_fns = [fn for fn, _ in mv.SLIDES]
    images = []
    for i, fn in enumerate(slide_fns):
        sys.stdout.write(f"  Slide {i+1}/17\r")
        sys.stdout.flush()
        images.append(np.array(fn()))
    print()

    silent_mp4 = TMP / "silent.mp4"
    cmd = ["ffmpeg", "-y",
           "-f", "rawvideo", "-vcodec", "rawvideo",
           "-s", f"{mv.W}x{mv.H}", "-pix_fmt", "rgb24",
           "-r", str(mv.FPS), "-i", "pipe:0",
           "-vcodec", "libx264", "-pix_fmt", "yuv420p",
           "-crf", "20", "-preset", "fast", str(silent_mp4)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    for i, (arr, hold) in enumerate(zip(images, holds)):
        raw = arr.tobytes()
        for _ in range(int(hold * mv.FPS)):
            proc.stdin.write(raw)
        if i < len(images) - 1:
            nxt = images[i + 1]
            for fi in range(mv.FADE):
                a = fi / mv.FADE
                bl = ((1 - a) * arr + a * nxt).astype(np.uint8)
                proc.stdin.write(bl.tobytes())
    proc.stdin.close()
    proc.wait()

    # 4. Build full audio track aligned to video
    print("Building audio track...")
    # 全セグメント結合後に再正規化（セグメント間の音量ばらつき解消）
    all_audio = []
    for i, ((arr, sr), hold) in enumerate(zip(speech_arrs, holds)):
        # Pad speech with silence to fill the full slot
        slot = hold + (FADE / mv.FPS if i < len(holds) - 1 else 0)
        slot_n = int(slot * sr)
        if len(arr) < slot_n:
            arr = np.concatenate([arr, silence(slot - len(arr)/sr, sr)])
        else:
            arr = arr[:slot_n]
        all_audio.append(arr)

    full_audio = np.concatenate(all_audio)
    full_audio = normalize(full_audio, target=29000)  # 全体を再正規化
    audio_wav  = TMP / "full_audio.wav"
    arr_to_wav(full_audio, SR, audio_wav)

    # 5. Merge video + audio
    print("Merging video + audio...")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(silent_mp4),
        "-i", str(audio_wav),
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "128k",
        "-shortest",
        str(VIDEO_OUT)
    ], check=True, stderr=subprocess.DEVNULL)

    mb = VIDEO_OUT.stat().st_size / 1024 / 1024
    total = sum(holds) + (len(holds)-1) * FADE/mv.FPS
    print(f"\nDone → {VIDEO_OUT}")
    print(f"Total duration: {total:.0f}s  Size: {mb:.1f} MB")

if __name__ == "__main__":
    main()
