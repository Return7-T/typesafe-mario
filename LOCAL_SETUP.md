# Mac 本地运行

首次安装：

```sh
python3.13 -m venv .venv
.venv/bin/python -m pip install -e ".[mario,dev]"
cp .env.example .env
```

编辑 `.env` 填入自己的密钥。

双击 `launch.command` 打开游戏和数据窗口。按 R 或点击 Restart 重开，Esc / Q 退出。

启动器在配置了 `OPENROUTER_API_KEY` 或 `TYPESAFE_API_KEY` 时使用 Jev，否则运行不调用 API 的规则策略演示。两者都有时优先使用 OpenRouter。

要启用 Jev，在项目目录创建 `.env`（已被 Git 忽略）：

```sh
OPENROUTER_API_KEY='你的密钥'
OPENROUTER_MODEL='typesafe/jev-1.13'
```

也可以从终端运行：

```sh
./launch.command
```

每轮的决策记录保存在 `artifacts/`。
