<h1 align="center">邓紫棋拟人 Codex 桌宠</h1>

<p align="center">G.E.M. Codex Pet · 以邓紫棋（G.E.M.）为灵感的 Q 版动画桌宠，由粉丝制作。</p>

<p align="center">
  <a href="https://github.com/ArthurLloyd/gem-codex-pet/actions/workflows/validate.yml"><img src="https://github.com/ArthurLloyd/gem-codex-pet/actions/workflows/validate.yml/badge.svg" alt="Validate release"></a>
</p>

<p align="center">
  <a href="https://github.com/ArthurLloyd/gem-codex-pet/releases/latest">下载</a> ·
  <a href="#安装">安装</a> ·
  <a href="docs/compatibility.md">兼容性</a> ·
  <a href="CHANGELOG.md">更新记录</a> ·
  <a href="https://github.com/ArthurLloyd/gem-codex-pet/issues">问题反馈</a>
</p>

<p align="center">
  <img src="assets/idle.gif" width="192" height="208" alt="邓紫棋拟人桌宠的待机动画：呼吸与眨眼">
  <img src="assets/waving.gif" width="192" height="208" alt="邓紫棋拟人桌宠的挥手动画">
</p>

## 特性

- **邓紫棋主题**：以邓紫棋（G.E.M.）为灵感制作的粉色系 Q 版角色与动画。
- **九种动画**：待机、左右跑动、挥手、跳跃、失败、等待、工作和检查。
- **离线安装**：Windows 完整解压后双击安装，无需管理员权限、Python 或额外运行时。
- **用户级安装**：支持默认 Codex home、`CODEX_HOME` 和自定义绝对路径。
- **完整性校验**：安装前验证 SHA-256，保留与发行资源不同的已有内容。
- **便携分发**：同时提供 Windows 安装包、通用资源包和独立透明精灵图。

## 环境要求

- 已安装并登录支持本地自定义宠物的 **Codex 桌面版**。
- 自动安装脚本需要 Windows 和 Windows PowerShell 5.1 或更高版本。
- macOS 提供手动安装方式，尚未完成运行验收。详细测试范围见 [兼容性记录](docs/compatibility.md)。

## 安装

当前 v1.1.0 发行包在 Codex 中仍显示为 **Pink Heart Companion**，文件名和安装目录也沿用 `pink-heart-companion`，以兼容已有安装。仓库名与 README 展示名称已更新为邓紫棋主题。

### Windows

1. 安装并登录支持自定义宠物的 **Codex 桌面版**。
2. 从 [Release](https://github.com/ArthurLloyd/gem-codex-pet/releases/latest) 下载 `pink-heart-companion-v1.1.0-windows.zip`，**完整解压**到普通文件夹。
3. 双击 `install.cmd`，按提示完成安装。无需管理员权限、Python 或额外软件；安装过程完全离线。
4. 打开 Codex **设置 → Pets（或 Mini & Pets）**，点击 **Refresh / 刷新**，选择 **Pink Heart Companion**。
5. 未显示时使用 **Show pet** 或输入 `/pet`；没有刷新按钮时重启 Codex。

安装只写入当前用户的宠物目录。选择和显示宠物由 Codex 设置完成。[官方宠物使用说明](https://learn.chatgpt.com/docs/pets)

### 发行文件

| Release 附件 | 用途 |
| --- | --- |
| `pink-heart-companion-v1.1.0-windows.zip` | Windows 双击安装、卸载，推荐大多数用户使用 |
| `pink-heart-companion-v1.1.0-portable.zip` | 仅包含宠物目录与两个资源文件，适合手动安装 |
| `pink-heart-companion-v1.1.0.webp` | 原始透明精灵图，供支持导入精灵图的界面使用 |
| `SHA256SUMS.txt` | 三个附件的 SHA-256 校验值 |

GitHub 自动生成的 **Source code** 是开发源码，普通用户请选择上面的 Windows ZIP。

### 自定义安装位置

默认目录：

```text
%USERPROFILE%\.codex\pets\pink-heart-companion\
├── pet.json
└── spritesheet.webp
```

如果运行 Codex 时设置了 `CODEX_HOME`，安装器会使用 `%CODEX_HOME%\pets\pink-heart-companion`。也可以在 PowerShell 中指定绝对路径：

```powershell
.\install.cmd -CodexHome "D:\My Codex Home"
.\uninstall.cmd -CodexHome "D:\My Codex Home"
```

路径选择顺序为 `-CodexHome` → `CODEX_HOME` → `%USERPROFILE%\.codex`。请以运行 Codex 的普通用户安装；传入的路径是 **Codex home**，无需追加 `pets`。

重复安装相同资源会直接校验并退出。安装器不会覆盖不同内容的同名目录；卸载器遇到被修改的资源、额外文件、符号链接或目录联接会停止，保留现有内容供你检查。脚本只为本次 PowerShell 进程设置执行策略，不修改系统执行策略；受管电脑的策略可能阻止脚本，此时可手动安装。

### 手动安装

解压 `portable.zip`，把 **`pink-heart-companion` 整个文件夹**复制到活动 Codex home 的 `pets` 目录，然后刷新并选择宠物。

- Windows 默认：`%USERPROFILE%\.codex\pets\`
- macOS 默认：`~/.codex/pets/`；此平台仅提供手动安装方式，尚未做运行验收。
- 自定义环境：`$CODEX_HOME/pets/`，应与桌面应用实际使用的位置一致。

最终 `pet.json` 必须直接位于 `pets/pink-heart-companion/`，不要多套一层解压目录。本项目面向支持本地自定义宠物的桌面版；IDE 扩展没有桌面悬浮宠物选择界面。CLI 与其他界面不在本版本验收范围。[官方界面差异说明](https://learn.chatgpt.com/docs/pets)

## 卸载

双击解压目录中的 `uninstall.cmd`，然后在 Codex 里选择其他宠物并刷新。若安装时传入了 `-CodexHome`，卸载时也应传入相同路径：

```powershell
.\uninstall.cmd -CodexHome "D:\My Codex Home"
```

使用手动安装时，可在确认文件内容后移除活动 Codex home 下的 `pets/pink-heart-companion` 目录。安装器不生成额外备份；保留下载的 ZIP 即可重新安装或运行卸载脚本。

## 常见问题

**安装后列表中没有出现？** 检查安装器输出的路径与 Codex 的活动 home 是否一致，确认完整解压、刷新列表，并检查 `pet.json` 的上一级是否就是 `pink-heart-companion`。仍未出现时重启 Codex，确认应用已提供自定义宠物功能。

**提示文件校验失败或目录内容不同？** 重新下载完整 ZIP。若目标目录有你自己修改的内容，先检查并移到其他位置，再安装；脚本不会替你覆盖它。

**脚本被电脑策略阻止？** 使用 portable ZIP 手动复制文件，或由电脑管理员按组织策略处理。无需把系统执行策略永久改成不受限。

**宠物不动或某个状态未触发？** 检查操作系统的减少动态效果设置，并用实际任务触发相应状态。动画事件和悬浮窗行为由 Codex 控制。[官方动态效果说明](https://learn.chatgpt.com/docs/pets)

## 开发与打包

安装用户不需要 Python。开发、校验和构建使用 Python 3.11+：

```powershell
python -m pip install -r requirements-dev.txt
python tools/validate_pet.py release/pink-heart-companion
python -m unittest discover -s tests -v
python tools/build_release.py
python tools/audit_publication.py --dist dist
```

输出在 `dist/`，包括两个 ZIP、独立 WebP 和校验清单。打包使用明确的文件白名单与固定 ZIP 时间戳，相同输入生成相同字节。Windows 测试会从生成的 ZIP 解压，在隔离目录里验证安装、重复安装、路径选择、卸载、文件冲突和完整性保护，不接触开发者真实的 Codex home。非 Windows 环境只运行资源与打包测试。

```text
release/pink-heart-companion/  Codex 读取的两文件资源
scripts/                      离线安装与卸载脚本
tools/                        资源校验与可复现打包
tests/                        分发包与安装行为测试
assets/                       README 动画预览
source/                       角色参考图、基础图和美术约定
docs/                         安装说明、兼容记录与动画参数
.github/workflows/            Windows 自动校验与构建
```

V1.1.0 改进的是分发、安装、文档与项目结构，宠物资源与已验收 V1.0 完全相同。`spriteVersionNumber: 1` 表示精灵图格式，不是 Release 版本号；本资源为 1536 × 1872、8 列 × 9 行的无损透明 WebP。旧制作工具对格式版本的命名曾与 Codex 不同，不能把 manifest 改成 `2`。详见 [兼容性记录](docs/compatibility.md)。

## 隐私

安装器完全离线运行，仅处理当前宠物目录中的两个资源文件；不读取 Codex 会话、账号配置或凭据，不包含遥测和后台服务。发行包使用文件白名单构建，角色参考图和开发过程文件不进入安装资源。

`tools/audit_publication.py` 检查已跟踪文件、Git 历史、图片元数据和可选的发行包，报告匹配到的个人路径、凭据或标识。该工具用于辅助发布前审核，不能替代人工检查。

## 反馈与贡献

欢迎通过 [Issues](https://github.com/ArthurLloyd/gem-codex-pet/issues) 反馈问题。请提供操作系统、Codex 版本、安装方式、复现步骤和错误信息，并在提交日志或截图前移除个人路径、账号信息和凭据。

修改脚本或资源后，请运行上述校验和测试；变更资源格式时同步更新兼容性文档。

## 许可

本项目为粉丝创作的桌宠，不代表邓紫棋本人或其团队。

本仓库暂未指定开源许可证。
