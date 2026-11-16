# 音效事件与 NumPy 合成

## 声音原则

只做关键音效，不做配音、背景音乐或持续铺底。音效应服务动作和语义，不要每个 cut 都塞 whoosh。

常用事件包括：

- 点击、按键、消息出现。
- 划屏、翻页、拖动。
- 心跳、呼吸、耳鸣。
- 碎裂、断裂、剪刀。
- 气泡出现/破裂、液体、纸张。
- 脚步、关门、抽屉。
- 点题时极短的节奏型强调。

把事件定义在一个清单中，并让画面和音频都引用它。事件至少包含：

```ts
{
  cueId: "c05",
  at: 1.2,
  type: "click",
  gain: 0.75
}
```

## 时间对齐

全局秒数必须由 cue 起点推导：

```text
absolute = startFrame(cueId) / fps + atSeconds
```

不要手填全片绝对秒数，否则改文案后会失配。生成脚本可接受从工程导出的 JSON，或读取共享 `audio-events.json`；避免 TS 与 Python 各维护一套事件。

## `tools/make_audio.py`

至少满足：

- Python 3，依赖 NumPy；文件读写使用标准库 `wave`。
- 输出 `public/soundtrack.wav`。
- 默认 48,000 Hz、16-bit PCM。
- 计算目标总时长，创建足够长的静音缓冲。
- 每个事件在对应 sample offset 写入短包络音效，不能只截断正弦波。
- 使用确定性随机种子，重新运行得到一致结果。
- 控制峰值，避免削波；事件重叠时做软限幅或归一化。
- 不生成连续音乐。

建议每种音效用 20–200 ms 的 attack/decay 包络，并对参数做轻微确定性变化，避免机械重复。

## 合成示例结构

```python
def add_event(mix, sample_rate, start_sec, sound):
    start = max(0, int(round(start_sec * sample_rate)))
    end = min(len(mix), start + len(sound))
    if start < end:
        mix[start:end] += sound[: end - start]
```

具体波形可按事件实现：

- click：极短高频瞬态 + 低频敲击。
- swipe：带通噪声的短促扫频。
- heartbeat：两次低频衰减脉冲。
- crack：短噪声爆点 + 多个细小碎片脉冲。
- bubble：上升正弦滑音或短共振。
- scissors：两段错位的高频短噪声。
- footstep：低频软瞬态 + 少量噪声。
- rhythm accent：1–3 个极短打击，不超过点题瞬间。

## 验证

- 检查 WAV 时长与 composition 完全匹配或在可接受尾留内。
- 检查无 NaN、无削波、左右声道一致。
- 对照画面事件峰值抽查帧时间。
- 若无法播放音频，交付时明确写“未试听”，不要声称已主观听验。
