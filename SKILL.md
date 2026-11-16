---
name: remotion-chinese-psychology-video
description: Build complete Chinese psychology and thought-explainer short-video projects in Remotion from cue-based copy, including bespoke first-act direction, deterministic cue timing, synchronized sound effects, strict legibility, copy revisions, verification, and zip delivery. Use for Chinese psychology or ideas videos that need a complete runnable Remotion project; do not use for unrelated video edits or one-off Remotion snippets.
---

# Remotion 中文心理短片

## 交付目标

把用户给出的中文文案做成可运行、可修改、可导出的 Remotion v4 工程，并交付 zip。

除非用户明确覆盖，工程必须满足：

- Node.js 18+、Remotion v4、TypeScript。
- 1920×1080、30 fps。
- 中文字体为思源宋体 `NotoSerifSC`。
- `npm install && npm run dev` 可以预览，`npm run build` 可以导出。
- 工程内提供 `tools/make_audio.py`，使用 Python + NumPy 按文案时间点合成关键音效，输出 `public/soundtrack.wav`。
- 工程带 README，说明项目结构、文案修改方式和音效重新生成方式。
- 不包含配音或配乐，只包含与关键画面事件精确同步的音效。
- zip 不包含 `node_modules`、预览缓存或无关临时文件。

将用户已经确认的文案、作者署名、视觉方向和其他明确选择视为锁定内容。只有用户明确要求时才改；未要求改动的 cue 保留原有视觉设计、道具、配色与局部动画。

## 先锁定需求

开始制作前先独立检查：

1. 文案是否包含钩子、提问、主题名和解释段。
2. 作者、固定时长、逐句 `dur` / `pause`、配色或特定画面是否给出。
3. 用户是否要求直接导出且不逐帧检验。若是，仍要完成必要的类型检查和工程完整性检查。
4. 文案修改是否会让未变 cue 的绝对起点变化。会变化时，保留其视觉和局部动画，但重算全局时间轴与音效。
5. 是否存在无法同时满足的约束。先指出冲突并采用最合理的可执行解释，不要悄悄违背已确认内容。

默认不增加配音、配乐、画面水印、品牌、作者（除非文案或用户给出）或未要求的剧情。

## 建立 cue 时间轴

先读 [references/cue-timing.md](references/cue-timing.md)，再建立唯一的时间轴数据源。

- 每个可独立成镜的句子对应一个稳定 `cueId`。
- 先确定场景边界，再计算时长；不要让 React 组件各自估算起点。
- 普通 cue 的秒数按用户参数计算：

  `seconds = max(minDuration, baseHold + visibleCharacterCount / charsPerSecond + pause)`

- `pause` 是可选的附加停留；`dur` 是固定秒数覆盖项，存在时忽略公式和 `pause`。
- 在 30 fps 下将时长转换为整数帧，并让后一 cue 起点等于前一 cue 结束帧。
- 总时长由所有 cue 帧数相加得到；片尾如需尾留，单独设 `tailFrames`。
- 把参数、cue、场景和音效事件放在少量可审计的配置文件中，README 必须告诉用户从哪里修改。

中文可见字数、标点是否计字、基础停留、每秒字数和最短时长应在工程中明确配置，不能散落在镜头组件里。若用户没给参数，可给一套合理默认值，并在交付说明中写明。

## 先导演，再编码

制作当前视频的视觉主轴和镜头表。先读 [references/creative-direction.md](references/creative-direction.md)，完成以下决策后再写组件：

- 全片统一的火柴人造型、线宽、比例、关节和识别色。
- 与主题相关的材质、光影、空间和色彩系统。
- 每个 cue 的独立道具、动作和视觉隐喻。
- 第一幕的连续镜头路径、点题动作和标题揭晓机制。
- 哪些字幕关键词需要高亮，哪些数字或界面元素需要独立避让。

每个视频的开场必须重新设计。不要复用以前的镜头路径、构图或标题动效。每个场景也必须有自己的道具和事件，不能退化为火柴人站在字幕旁边。

## 第一幕硬要求

第一幕由钩子、铺垫、主题标题揭晓组成，目标约 10–20 秒。

- 尽量一镜到底；采用连续 2D、2.5D 或 3D 镜头运动。
- 不用平铺直叙的横向卷轴式 ppt 幻灯片。
- 钩子先制造问题、损失、矛盾或视觉异样，再给主题命名。
- 标题出场必须单独设计，并“演出”主题含义，而不是只做普通推拉、逐字弹入或缩放。
- 作者存在时，在标题下方用一行清晰小字署名；小字仍不得低于画面可读下限。
- 若钩子本身是文案 cue，确保表演与第一句字幕同步，不能先演完再补字幕。

## 实现 Remotion 工程

使用集中配置驱动 Composition：

- 在 `calculateMetadata` 或等价位置从 cue 数据计算 composition 的 `durationInFrames`。
- 使用统一 `Sequence` 或绝对帧映射，避免多个独立计时器漂移。
- 在 `delayRender` / `continueRender` 或可靠字体加载流程中等待 `NotoSerifSC`；不要让首帧闪回退字体。
- 给每个 cue 建立明确组件映射。组件只接收自身 cue 与局部参数。
- 局部动画使用 cue 内相对帧；全局音效事件用 cue ID + cue 内秒数记录，再映射到绝对帧。
- 对相机运动使用稳定锚点和可逆变换；需要界面清晰时，相机运动应停住在可读姿态。
- 保持可维护的组件命名和配置边界，禁止把所有镜头堆进一个超大文件。

## 清晰度硬门槛

- 画面正文不得小于 44 px；重点词通常 60–200 px。
- 字幕约 66–68 px，并使用深色渐变底托或奶油色纸片等实底提升对比。
- 亮字加深色描边；暗字放在足够亮的底上。
- 不使用半透明“鬼影字”作为可读信息。
- 画面四边保留安全边距，底部约 200 px 留给字幕；关键道具、数字、按钮和标题不能被字幕、遮罩、眼皮、粒子或镜头裁切遮挡。
- 镜头放大手机整屏、编辑器、关键界面或关键数字时，必须保证信息完整可见。
- 若缩放后主界面文字仍偏小，把关键数字或结论用独立大字放在两侧，但不要伪装成主界面的一部分。
- 在代表性帧上检查文字边界、描边、对比度、遮挡和最小字号；不能只凭代码判断“应该清楚”。

## 声音

先读 [references/audio-synthesis.md](references/audio-synthesis.md)，再写 `tools/make_audio.py`。

- 建立事件表，把点击、划屏、心跳、碎裂、气泡、剪刀、脚步等绑定到 cue ID 和 cue 内时间。
- 音效必须和画面事件共用同一事件源或同一时间映射；不要维护两套近似时间。
- 点题处可使用极短节奏型音效，但不得形成持续配乐。
- 使用 NumPy 和 Python 标准库生成确定性 PCM WAV。默认 48 kHz、16-bit，可单声道或立体声。
- 重新运行脚本必须覆盖 `public/soundtrack.wav`，且结果与事件表一致。
- README 写明依赖、命令、事件表和输出路径。

## 修改文案

用户提供新文案时，按以下规则合并：

1. 旧文案整体被新文案替换。
2. 用稳定 cue ID 和规范化文本判断哪些 cue 文本未变。
3. 未变 cue 保留原场景组件、视觉设计、道具、配色和局部动画。
4. 新增或改文 cue 重新设计对应画面与字幕；若结构变化破坏了主题主轴，允许重新导演受影响的连续段。
5. 重算每个 cue 时长、全局起点和 composition 总帧数。
6. 由于前序时长改变，未变 cue 的绝对起点可以变化；这不等于改动其视觉内容。必须同步平移所有后续 `Sequence`、音效事件和相机关键帧。
7. 重新生成 WAV，并检查所有音效仍与局部事件点对齐。
8. 不因一次文案修改顺手更换作者、字体、分辨率、视觉系统或未受影响的场景。

若用户要求“完全不改动其他画面”且文案时长变化，说明无法同时保持绝对时间位置不变；优先保持视觉内容不变并重算时间轴。

## 验证与打包

完成工程后运行 [scripts/audit_project.py](scripts/audit_project.py) 做静态交付检查，再执行工程自身的类型检查。用户要求正常检验时，还应渲染代表性帧并人工查看：

- 第一幕点题帧、标题帧和作者行。
- 每个 cue 的中段和结束前状态。
- 字幕最长句、最大相机缩放、最复杂界面。
- 手机整屏、关键数字、划线与重点词的完整可见性。
- 至少检查声音事件表与对应 cue 的帧映射；如环境可播放，抽听关键事件，若不能则明确说明。

用户说“直接导出压缩包，不需要检验”时，不做逐帧预览，但必须完成类型检查和可打包性检查。

使用 [references/delivery-checklist.md](references/delivery-checklist.md) 做最终检查。zip 根目录应直接包含可运行工程文件，避免多套一层无意义目录；README 放在工程根目录。

交付回复简短说明：

- 做了什么。
- 第一幕和标题的独立设计。
- 后续各场景。
- 音效事件与生成方式。
- 哪些部分已验证、哪些未验证。
