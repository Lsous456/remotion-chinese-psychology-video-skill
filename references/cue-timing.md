# Cue 时间轴与修改规则

## 单一数据源

把以下内容放在可审计配置中，不要让镜头组件自行决定全局起点：

```ts
type Cue = {
  id: string;
  section: "hook" | "setup" | "title" | "explanation";
  text: string;
  pause?: number;
  dur?: number;
};

type TimingConfig = {
  fps: number;
  baseHold: number;
  charsPerSecond: number;
  minDuration: number;
  tailFrames: number;
};
```

推荐单独生成并导出：

```ts
type TimedCue = Cue & {
  startFrame: number;
  durationInFrames: number;
  endFrame: number;
};
```

`sequence`, `durationInFrames`、字幕、镜头关键帧和音效都从 `TimedCue` 读取。

## 时长公式

```text
if cue.dur exists:
  seconds = cue.dur
else:
  seconds = max(
    minDuration,
    baseHold + visibleCharacterCount(cue.text) / charsPerSecond + (cue.pause ?? 0)
  )

durationInFrames = max(1, round(seconds * fps))
```

约定：

- `dur` 是固定秒数覆盖项；存在时忽略公式和 `pause`。
- `pause` 是可选的额外静置秒数，只在公式分支生效。
- 所有 cue 在 30 fps 下转为整数帧。
- `startFrame(0) = 0`。
- `startFrame(n) = sum(durationInFrames[0..n-1])`。
- `durationInFrames(composition) = sum(all cue frames) + tailFrames`。

把 `visibleCharacterCount` 写成项目内统一函数。默认可忽略空白和标点，只计算可见汉字、拉丁字母和数字；若连续拉丁单词或数字应按单词计“字”，在函数里明确说明并保持一致。若用户明确要求“字符串长度”，则按用户定义执行。

不要一帧一帧用浮点累计；先得到每个 cue 的整数帧，再累加，避免 30 fps 下的漂移。

## 场景与事件映射

每个 cue 建议保留：

```ts
{
  cueId: "c03",
  visualId: "editor-undo",
  sfx: [
    { type: "delete", at: 0.42, gain: 0.7 },
    { type: "undo", at: 0.78, gain: 0.8 }
  ]
}
```

`at` 是 cue 内秒数，不是全片秒数。生成音效时：

```text
absoluteSeconds = startFrame / fps + at
```

这样修改前序 cue 时长后，后续事件会自动顺延并保持局部对齐。

## 文案修改的 cue diff

不要靠数组下标判断 cue 是否变化。使用稳定 `id`；新文案若没有 id，先按原段结构复用旧 id，再为新增项分配新 id。

规范化文本比较可去除多余空白、统一全半角并保留正文语义，但原展示文本仍使用用户新文案。示例：

```ts
const normalize = (text: string) =>
  text.normalize("NFKC").replace(/\s+/g, "").trim();
```

处理规则：

- 未变 cue：保留 `visualId`、组件参数、配色、道具和局部关键帧。
- 改文 cue：只重做该 cue 的字幕排版、道具适配和所需动作。
- 新增 cue：创建新画面，可从全片视觉语言延伸，但不能复制旧开场。
- 删除 cue：删除其视觉和事件，并顺延后续 cue。
- 所有环节重算 `startFrame`、composition 总时长和音效事件绝对时间。

## 修改冲突的说明

“其余画面不变”和“时间轴重算”同时存在时，解释为：

- 视觉内容、设计和局部演出保持不变。
- 绝对起点、全局 Sequence 区间和后续音效时间可变化。

若用户要求绝对帧也完全不变，则只有新旧 cue 帧数完全相同时才能满足；否则必须指出冲突。
