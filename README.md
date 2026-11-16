# Remotion 中文心理短片 Skill

这是一个用于 Codex/Agent Skills 的可复用技能，目标是让 agent 根据中文心理学或思想类文案，生成完整的 Remotion v4 TypeScript 工程，并交付可运行的 zip。

## 能力范围

- 解析钩子、提问、主题名和解释段，建立稳定的 cue 时间轴。
- 每句时长按基础停留、字数和语速自动计算，支持 `pause` 和固定 `dur`。
- 为每个视频重新设计第一幕连续镜头和主题标题演出，不复用旧开场。
- 保持统一火柴人、分场景独立道具、主题化色彩与空间。
- 强制检查 1920×1080、30 fps、思源宋体、字幕字号和关键内容安全区。
- 提供 NumPy 音效合成规范，输出 `public/soundtrack.wav`。
- 修改文案时只重做变更 cue，同时重算全局时间轴和音效。
- 包含交付检查脚本，覆盖运行入口、Remotion 版本、音效文件和 README 信息。

## 安装为 Codex Skill

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone <THIS_REPOSITORY_URL> \
  "${CODEX_HOME:-$HOME/.codex}/skills/remotion-chinese-psychology-video"
```

重新打开 Codex 或刷新 skills 后，可通过 `$remotion-chinese-psychology-video` 显式调用，也可能在匹配的中文 Remotion 短视频任务中自动触发。

本仓库只提供 skill 指令和辅助检查脚本，不包含某个具体视频工程的源码、字体文件或第三方音频素材。

## 使用示例

```text
使用 $remotion-chinese-psychology-video，把下面文案做成完整 Remotion 工程，
最后直接交付 zip。作者：XXX。
```

然后粘贴按句拆分的文案。建议同时提供：

- 希望的视觉方向或必须避开的风格。
- `baseHold`、`charsPerSecond`、`minDuration` 等时长参数。
- 特定句子的 `pause` 或 `dur`。
- 是否要求渲染后逐帧检查。

## 仓库结构

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── audio-synthesis.md
│   ├── creative-direction.md
│   ├── cue-timing.md
│   └── delivery-checklist.md
└── scripts/
    └── audit_project.py
```

`SKILL.md` 是入口。只有在当前任务需要时，agent 才读取对应的 `references/` 文档。

## 校验项目

生成视频工程后，可运行：

```bash
python scripts/audit_project.py /path/to/generated-project
```

该脚本只做静态交付检查，不能代替 TypeScript 检查、Remotion 实际渲染和逐帧视觉验收。
