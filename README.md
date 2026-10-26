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
            "command": "uv --directory ~/ghq/github.com/SlashNephy/claude-code-tts run main.py",
            "async": true
          }
        ]
      }
    ]
  }
}
```

### モデル固有の引数

`CLAUDE_CODE_TTS_GENERATE_KWARGS` に JSON オブジェクトを指定すると、`model.generate()` にそのまま渡します。
`voice` / `speed` / `lang_code` と重複するキーは、こちらの値が優先されます。

例: [Irodori-TTS](https://github.com/Blaizzy/mlx-audio/tree/main/mlx_audio/tts/models/irodori_tts) の VoiceDesign モデルで、声質をテキストで指定する

```json
{
  "env": {
    "CLAUDE_CODE_TTS_MODEL_ID": "mlx-community/Irodori-TTS-600M-v3-VoiceDesign-8bit",
    "CLAUDE_CODE_TTS_GENERATE_KWARGS": "{\"instruct\": \"落ち着いた女性の声で、近い距離感でやわらかく自然に読み上げてください。\", \"num_steps\": 6, \"t_schedule_mode\": \"sway\"}"
  }
}
```
