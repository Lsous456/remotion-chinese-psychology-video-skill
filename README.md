# Remotion 中文心理短片 Claude Skill

这是一个主要面向 Claude Code 的 Agent Skill，也兼容 Codex 等支持 `SKILL.md` 的 Agent Skills 宿主。它根据中文心理学或思想类文案，生成完整的 Remotion v4 TypeScript 工程，并交付可运行的 zip。

## 能力范围

- 解析钩子、提问、主题名和解释段，建立稳定的 cue 时间轴。
- 每句时长按基础停留、字数和语速自动计算，支持 `pause` 和固定 `dur`。
- 为每个视频重新设计第一幕连续镜头和主题标题演出，不复用旧开场。
- 保持统一火柴人、分场景独立道具、主题化色彩与空间。
- 强制检查 1920×1080、30 fps、思源宋体、字幕字号和关键内容安全区。
- 提供 NumPy 音效合成规范，输出 `public/soundtrack.wav`。
- 修改文案时只重做变更 cue，同时重算全局时间轴和音效。
- 包含交付检查脚本，覆盖运行入口、Remotion 版本、音效文件和 README 信息。

## 安装到 Claude Code

个人 skill，所有本地项目可用：

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/Lsous456/remotion-chinese-psychology-video-skill.git \
  ~/.claude/skills/remotion-chinese-psychology-video
```

项目 skill，随仓库共享给团队：

```bash
mkdir -p .claude/skills
git clone https://github.com/Lsous456/remotion-chinese-psychology-video-skill.git \
  .claude/skills/remotion-chinese-psychology-video
```

Claude Code 会自动发现本地 skill。也可以直接调用：

```text
/remotion-chinese-psychology-video
```

如果 skill 是在 Claude Code 会话中新增的顶层目录，使用 `/reload-skills` 或重新打开会话。个人 skill 只在本机可用；如需 Cowork、云端会话或定时任务使用，需要按 claude.ai 的 Skill 上传流程单独启用。

## 兼容 Codex Skill

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/Lsous456/remotion-chinese-psychology-video-skill.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/remotion-chinese-psychology-video"
```

重新打开 Codex 或刷新 skills 后，可通过 `$remotion-chinese-psychology-video` 显式调用，也可能在匹配的中文 Remotion 短视频任务中自动触发。

本仓库只提供 skill 指令和辅助检查脚本，不包含某个具体视频工程的源码、字体文件或第三方音频素材。

## 使用示例

```text
/remotion-chinese-psychology-video

把下面文案做成完整 Remotion 工程，最后直接交付 zip。作者：XXX。
```

然后粘贴按句拆分的文案。Claude 也会在匹配的中文心理短文案需求中自动判断是否加载。建议同时提供：

- 希望的视觉方向或必须避开的风格。
- `baseHold`、`charsPerSecond`、`minDuration` 等时长参数。
- 特定句子的 `pause` 或 `dur`。
- 是否要求渲染后逐帧检查。

## 仓库结构

```text
.
├── CLAUDE.md
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
