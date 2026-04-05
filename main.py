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


if __name__ == "__main__":
    data = json.load(sys.stdin)
    text = data.get("last_assistant_message", "")
    if text is None:
        sys.exit(0)

    if not TTS_ENABLED:
        sys.exit(0)

    model = load_model(MODEL_ID)
    for result in model.generate(
        text=text,
        voice=VOICE,
        speed=SPEED,
        lang_code=LANG_CODE,
    ):
        with tempfile.NamedTemporaryFile(suffix=".wav") as f:
            sf.write(f.name, result.audio, result.sample_rate)
            subprocess.run(["afplay", f.name], check=True)
