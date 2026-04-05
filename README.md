# claude-code-tts

## Usage

`~/.claude/settings.json`
```json
{
  "env": {
    "CLAUDE_CODE_TTS_ENABLED": "1",
    "CLAUDE_CODE_TTS_MODEL_ID": "mlx-community/Kokoro-82M-bf16",
    "CLAUDE_CODE_TTS_VOICE": "jf_alpha",
    "CLAUDE_CODE_TTS_SPEED": "1.0",
    "CLAUDE_CODE_TTS_LANG_CODE": "j"
  },
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "[ \"$CLAUDE_CODE_TTS_ENABLED\" = \"1\" ] && uv --directory ~/ghq/github.com/SlashNephy/claude-code-tts run main.py || true",
            "async": true
          }
        ]
      }
    ]
  }
}
```
