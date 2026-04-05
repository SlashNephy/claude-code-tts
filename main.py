import json
import os
import subprocess
import sys
import tempfile

import soundfile as sf
from mlx_audio.tts.utils import load_model

TTS_ENABLED = os.environ.get("CLAUDE_CODE_TTS_ENABLED", "0") == "1"
MODEL_ID = os.environ.get("CLAUDE_CODE_TTS_MODEL_ID", "mlx-community/Kokoro-82M-bf16")
VOICE = os.environ.get("CLAUDE_CODE_TTS_VOICE", "jf_alpha")
SPEED = float(os.environ.get("CLAUDE_CODE_TTS_SPEED", "1.0"))
LANG_CODE = os.environ.get("CLAUDE_CODE_TTS_LANG_CODE", "j")
LINE_LIMIT = int(os.environ.get("CLAUDE_CODE_TTS_LINE_LIMIT", "0"))

if __name__ == "__main__":
    if not TTS_ENABLED:
        sys.exit(0)

    data = json.load(sys.stdin)
    text = data.get("last_assistant_message")
    if not text:
        sys.exit(0)

    chunks = text.split("\n\n")
    if LINE_LIMIT > 0:
        chunks = chunks[:LINE_LIMIT]

    model = load_model(MODEL_ID)
    for chunk in chunks:
        for result in model.generate(
            text=chunk,
            voice=VOICE,
            speed=SPEED,
            lang_code=LANG_CODE,
        ):
            with tempfile.NamedTemporaryFile(suffix=".wav") as f:
                sf.write(f.name, result.audio, result.sample_rate)
                subprocess.run(["afplay", f.name], check=True)
