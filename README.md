# Discord 会話ログ出力Bot

Discordのチャンネルから会話履歴を取得し、テキストファイルとして出力するBotです。
For the English version, please see the section below.

## 目次

- [機能](#機能)
- [必要なもの](#必要なもの)
- [初期設定](#初期設定)
- [起動方法](#起動方法)
- [使用方法](#使用方法)
- [出力ファイル](#出力ファイル)
- [トラブルシューティング](#トラブルシューティング)
- [セキュリティ上の注意](#セキュリティ上の注意)

## 機能

- `/export` スラッシュコマンドでチャンネルの会話ログを出力
- 取得するメッセージ数を指定可能（デフォルト: 100件）
- UTF-8（BOM付き）またはShift_JIS（CP932）を選択可能
- ユーザーIDをログに含めるか選択可能
- ユーザー名の表示形式を選択可能
- 実行結果と設定を埋め込みメッセージで表示
- ログファイル名にチャンネル名とサーバー名を使用

## 必要なもの

- Python 3.10以上
- Discord Bot
- `discord.py`
- `python-dotenv`

## 初期設定

### 1. Discord Botを作成する

1. [Discord Developer Portal](https://discord.com/developers/applications)を開く。
2. 「New Application」を選択し、アプリケーションを作成する。
3. 「Bot」ページを開き、「Add Bot」を選択する。
4. Bot Tokenをコピーする。

> Tokenはパスワードと同じように扱ってください。GitHubなどに公開しないでください。

### 2. 必要なIntentを設定する

このBotではメッセージ本文を扱うため、Developer Portalの「Bot」ページで以下を有効にしてください。

- **Message Content Intent**

### 3. Botをサーバーに招待する

OAuth2 URL Generatorで以下を選択し、生成されたURLからBotをサーバーに招待します。

- Scopes:
  - `bot`
  - `applications.commands`
- Bot Permissions:
  - View Channels
  - Read Message History
  - Send Messages
  - Attach Files
  - Embed Links

ログを取得する対象チャンネルで、BotのロールまたはBot自身に以下の権限があることを確認してください。

- チャンネルを見る
- メッセージ履歴を読む
- メッセージを送信
- ファイルを添付
- 埋め込みリンク

### 4. 仮想環境を作成する

プロジェクトのフォルダーで以下を実行します。

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 5. パッケージをインストールする

```powershell
py -m pip install -U discord.py python-dotenv
```

### 6. `.env`を作成する

プロジェクトのルートに `.env` ファイルを作成し、Bot Tokenを設定します。

```dotenv
TOKEN=ここにBotのTokenを入力
```

`.env` は `.gitignore` によりGit管理から除外されています。Tokenをソースコードに直接書かないでください。

## 起動方法

仮想環境を有効にした状態で、以下を実行します。

```powershell
py bot.py
```

以下のようなログが表示されれば起動成功です。

```text
Logged in as ...
```

Botを停止するには、ターミナルで `Ctrl+C` を押します。

## 使用方法

1. Botが起動していることを確認する。
2. ログを取得したいDiscordチャンネルで `/export` と入力する。
3. 必要に応じて引数を設定する。
4. コマンドを実行すると、ログファイルが添付された埋め込みメッセージが送信される。

### `/export` の引数

| 引数 | 説明 | デフォルト |
| --- | --- | --- |
| `limit` | 取得するメッセージ数 | `100` |
| `use_sjis` | `True`でShift_JIS（CP932）、`False`でUTF-8（BOM付き） | `False` |
| `include_user_id` | ログにユーザーIDを含めるか | `True` |
| `user_name_type` | `username`、`both`、`display_name`から選択 | `username` |

ユーザー名タイプの意味:

- `username`: ユーザー名のみ
- `both`: ユーザー名と表示名
- `display_name`: 表示名のみ

## 出力ファイル

ファイル名は以下の形式です。

```text
log_[チャンネル名]in[サーバー名].txt
```

例:

```text
log_generalinMyServer.txt
```

UTF-8を選択した場合はBOM付きで出力されます。Shift_JISで表現できない文字は置換されます。

## トラブルシューティング

### `403 Forbidden (error code: 50001): Missing Access`

Botに対象チャンネルへのアクセス権がありません。対象チャンネルの権限設定を確認し、Botに以下を許可してください。

- チャンネルを見る
- メッセージ履歴を読む

### スラッシュコマンドが表示されない

- Botが `applications.commands` スコープ付きで招待されているか確認する。
- Botを再起動する。
- Discord側でコマンドの反映に少し時間がかかる場合がある。

### `TOKENが見つかりません`

`.env` がプロジェクトのルートにあり、次の形式でTokenが設定されているか確認してください。

```dotenv
TOKEN=your_bot_token
```

## セキュリティ上の注意

- Bot Tokenを他人に共有しない。
- `.env` をGitにコミットしない。
- Tokenを公開してしまった場合は、Developer PortalでTokenを再生成する。
- 取得したログには個人情報が含まれる可能性があるため、取り扱いに注意する。

---

# Discord Conversation Log Export Bot

This bot retrieves message history from a Discord channel and exports it as a text file.

## Contents

- [Features](#features)
- [Requirements](#requirements)
- [Initial Setup](#initial-setup)
- [How to Start](#how-to-start)
- [Usage](#usage)
- [Output File](#output-file)
- [Troubleshooting](#troubleshooting)
- [Security Notes](#security-notes)

## Features

- Export channel conversation logs with the `/export` slash command
- Choose how many messages to retrieve (default: 100)
- Choose UTF-8 with BOM or Shift_JIS (CP932)
- Choose whether to include user IDs
- Choose the user name display format
- Show the result and settings in an embedded message
- Include the channel and server names in the output filename

## Requirements

- Python 3.10 or later
- A Discord Bot
- `discord.py`
- `python-dotenv`

## Initial Setup

### 1. Create a Discord Bot

1. Open the [Discord Developer Portal](https://discord.com/developers/applications).
2. Select "New Application" and create an application.
3. Open the "Bot" page and select "Add Bot".
4. Copy the bot token.

> Treat the token like a password. Never publish it on GitHub or elsewhere.

### 2. Configure Intents

Since this bot reads message content, enable the following on the Bot page in the Developer Portal:

- **Message Content Intent**

### 3. Invite the Bot to a Server

In the OAuth2 URL Generator, select the following options and invite the bot using the generated URL:

- Scopes:
  - `bot`
  - `applications.commands`
- Bot Permissions:
  - View Channels
  - Read Message History
  - Send Messages
  - Attach Files
  - Embed Links

Make sure these permissions are also allowed for the target channel. Channel-specific permission overwrites can deny access even when the role permissions look correct.

## How to Start

### 4. Create a Virtual Environment

Run the following commands in the project directory:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```powershell
py -m pip install -U discord.py python-dotenv
```

### 6. Create `.env`

Create a `.env` file in the project root and set the bot token:

```dotenv
TOKEN=your_bot_token
```

The `.env` file is excluded from Git by `.gitignore`. Do not put the token directly in the source code.

Run the bot with the virtual environment activated:

```powershell
py bot.py
```

The bot has started successfully when you see a log similar to:

```text
Logged in as ...
```

Press `Ctrl+C` in the terminal to stop the bot.

## Usage

1. Make sure the bot is running.
2. Type `/export` in the Discord channel whose logs you want to retrieve.
3. Configure the optional arguments as needed.
4. Run the command. The bot sends an embedded result message with the log file attached.

### `/export` Arguments

| Argument | Description | Default |
| --- | --- | --- |
| `limit` | Number of messages to retrieve | `100` |
| `use_sjis` | `True` for Shift_JIS (CP932), `False` for UTF-8 with BOM | `False` |
| `include_user_id` | Whether to include user IDs in the log | `True` |
| `user_name_type` | Choose `username`, `both`, or `display_name` | `username` |

User name display types:

- `username`: Username only
- `both`: Username and display name
- `display_name`: Display name only

## Output File

The filename uses the following format:

```text
log_[channel name]in[server name].txt
```

Example:

```text
log_generalinMyServer.txt
```

UTF-8 output includes a BOM. Characters unsupported by Shift_JIS are replaced when CP932 is selected.

## Troubleshooting

### `403 Forbidden (error code: 50001): Missing Access`

The bot cannot access the target channel. Check the channel-specific permissions and allow:

- View Channels
- Read Message History

### The slash command does not appear

- Make sure the bot was invited with the `applications.commands` scope.
- Restart the bot.
- Discord may take some time to update slash commands.

### `TOKEN not found`

Make sure `.env` is in the project root and contains the token in this format:

```dotenv
TOKEN=your_bot_token
```

## Security Notes

- Never share the bot token.
- Do not commit `.env` to Git.
- If the token is exposed, regenerate it in the Developer Portal.
- Exported logs may contain personal information; handle them carefully.
