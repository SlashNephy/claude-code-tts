import fcntl
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import alkana
import soundfile as sf
import unidic
from mlx_audio.tts.utils import load_model
from unidic.download import download_version

TTS_ENABLED = os.environ.get("CLAUDE_CODE_TTS_ENABLED", "0") == "1"
MODEL_ID = os.environ.get("CLAUDE_CODE_TTS_MODEL_ID", "mlx-community/Kokoro-82M-bf16")
VOICE = os.environ.get("CLAUDE_CODE_TTS_VOICE", "jf_alpha")
SPEED = float(os.environ.get("CLAUDE_CODE_TTS_SPEED", "1.0"))
LANG_CODE = os.environ.get("CLAUDE_CODE_TTS_LANG_CODE", "j")
LINE_LIMIT = int(os.environ.get("CLAUDE_CODE_TTS_LINE_LIMIT", "0"))
# モデル固有の引数 (Irodori-TTS の instruct など) を model.generate() にそのまま渡す
GENERATE_KWARGS = json.loads(os.environ.get("CLAUDE_CODE_TTS_GENERATE_KWARGS", "{}"))


def load_json_file(file_name: str) -> dict:
    base_dir = Path(__file__).parent
    file_path = base_dir / file_name
    if not file_path.exists():
        return {}

    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def ensure_unidic_dictionary() -> None:
    # unidic パッケージは辞書本体を含まず、venv を作り直すと消えるため、無ければ取得する
    # mecabrc はダウンロード処理の最後に書かれるので、展開途中の辞書を完成品と誤認しない
    mecabrc = Path(unidic.DICDIR) / "mecabrc"
    if mecabrc.exists():
        return

    # Stop hook は非同期で並行に走りうるため、ダウンロードを排他する
    lock_path = Path(unidic.DICDIR).parent / "download.lock"
    with lock_path.open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if not mecabrc.exists():
            download_version()


def english_to_kana(text: str) -> str:
    dictionary = load_json_file("dictionary.json")
    custom_dictionary = load_json_file("dictionary.custom.json")
    dictionary.update(custom_dictionary)
    for k, v in dictionary.items():
        text = re.sub(k, v, text, flags=re.IGNORECASE)

    def replace_word(m):
        word = m.group(0)
        kana = alkana.get_kana(word.lower())
        return kana if kana else word

    return re.sub(r"[a-zA-Z0-9]{2,}", replace_word, text)


if __name__ == "__main__":
    if not TTS_ENABLED:
        sys.exit(0)

    data = json.load(sys.stdin)
    text = data.get("last_assistant_message")
    if not text:
        sys.exit(0)

    text = english_to_kana(text)
    chunks = text.split("\n\n")
    if LINE_LIMIT > 0:
        chunks = chunks[:LINE_LIMIT]

    ensure_unidic_dictionary()
    model = load_model(MODEL_ID)
    for chunk in chunks:
        for result in model.generate(
            text=chunk,
            **{
                "voice": VOICE,
                "speed": SPEED,
                "lang_code": LANG_CODE,
                **GENERATE_KWARGS,
            },
        ):
            with tempfile.NamedTemporaryFile(suffix=".wav") as f:
                sf.write(f.name, result.audio, result.sample_rate)
                subprocess.run(["afplay", f.name], check=True)
