# Remotion 中文心理短片

本仓库主要是一个面向 Claude Code 的 Agent Skill，同时保持与 Codex 等 Agent Skills 宿主兼容。

## 使用

- 个人安装：放到 `~/.claude/skills/remotion-chinese-psychology-video/`。
- 项目安装：放到项目的 `.claude/skills/remotion-chinese-psychology-video/`。
- 直接调用：`/remotion-chinese-psychology-video`。
- 当任务明显匹配中文心理学或思想类 Remotion 短视频时，Claude Code 可以自动加载。

执行视频任务时，先读取 `SKILL.md`，再只按需读取相关 `references/` 文档。

## 维护

- `SKILL.md` 是唯一行为入口；不要复制整段 reference 到这里。
- frontmatter 保持 Agent Skills 兼容：`name`、`description`、`license`、`compatibility`、`metadata`、`allowed-tools`；跨 Codex 和 Claude 共用的环境说明放入 `metadata`。
- 不要为了 Claude Code 便利加入仅宿主支持且会破坏 Agent Skills 标准上传的字段。
- 修改后运行 `quick_validate.py`、`python -m py_compile scripts/audit_project.py`，并比较远程和本地内容。
- 除非用户明确要求，不要把仓库安装到本机的 `~/.claude/skills/`。
