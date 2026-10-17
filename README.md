# Discord 会話ログ出力Bot

Discordのチャンネルから会話履歴を取得し、テキストファイルとして出力するBotです。  
This bot retrieves message history from a Discord channel and exports it as a text file.

## 目次 / Contents

- [機能 / Features](#機能--features)
- [必要なもの / Requirements](#必要なもの--requirements)
- [初期設定 / Initial Setup](#初期設定--initial-setup)
- [起動方法 / How to Start](#起動方法--how-to-start)
- [使用方法 / Usage](#使用方法--usage)
- [出力ファイル / Output File](#出力ファイル--output-file)
- [トラブルシューティング / Troubleshooting](#トラブルシューティング--troubleshooting)

## 機能 / Features

### 日本語

- `/export` スラッシュコマンドでチャンネルの会話ログを出力
- 取得するメッセージ数を指定可能（デフォルト: 100件）
- UTF-8（BOM付き）またはShift_JIS（CP932）を選択可能
- ユーザーIDをログに含めるか選択可能
- ユーザー名の表示形式を選択可能
- 実行結果と設定を埋め込みメッセージで表示
- ログファイル名にチャンネル名とサーバー名を使用

### English

- Export channel conversation logs with the `/export` slash command
- Choose how many messages to retrieve (default: 100)
- Choose UTF-8 with BOM or Shift_JIS (CP932)
- Choose whether to include user IDs
- Choose the user name display format
- Show the result and settings in an embedded message
- Include the channel and server names in the output filename

## 必要なもの / Requirements

- Python 3.10以上 / Python 3.10 or later
- Discord Bot
- `discord.py`
- `python-dotenv`

## 初期設定 / Initial Setup

### 1. Discord Botを作成する / Create a Discord Bot

1. [Discord Developer Portal](https://discord.com/developers/applications)を開く。
2. 「New Application」を選択し、アプリケーションを作成する。
3. 「Bot」ページを開き、「Add Bot」を選択する。
4. Bot Tokenをコピーする。

> Tokenはパスワードと同じように扱ってください。GitHubなどに公開しないでください。  
> Treat the token like a password. Never publish it on GitHub or elsewhere.

### 2. 必要なIntentを設定する / Configure Intents

このBotではメッセージ本文を扱うため、Developer Portalの「Bot」ページで以下を有効にしてください。

- **Message Content Intent**

Since this bot reads message content, enable **Message Content Intent** on the Bot page in the Developer Portal.

### 3. Botをサーバーに招待する / Invite the Bot

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

Select the following options in the OAuth2 URL Generator and invite the bot:

- Scopes: `bot`, `applications.commands`
- Bot Permissions: View Channels, Read Message History, Send Messages, Attach Files, and Embed Links

Make sure these permissions are also allowed for the target channel. Channel-specific permission overwrites can deny access even when the role permissions look correct.

### 4. 仮想環境を作成する / Create a Virtual Environment

プロジェクトのフォルダーで以下を実行します。

Run the following commands in the project directory:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

PowerShellでスクリプト実行が制限されている場合は、必要に応じて実行ポリシーを確認してください。

If PowerShell blocks script execution, check your execution policy as needed.

### 5. パッケージをインストールする / Install Dependencies

```powershell
py -m pip install -U discord.py python-dotenv
```

### 6. `.env`を作成する / Create `.env`

プロジェクトのルートに `.env` ファイルを作成し、Bot Tokenを設定します。

Create a `.env` file in the project root and set the bot token:

```dotenv
TOKEN=ここにBotのTokenを入力
```

`.env` は `.gitignore` によりGit管理から除外されています。Tokenをソースコードに直接書かないでください。

The `.env` file is excluded from Git by `.gitignore`. Do not put the token directly in the source code.

## 起動方法 / How to Start

仮想環境を有効にした状態で、以下を実行します。

With the virtual environment activated, run:

```powershell
py bot.py
```

以下のようなログが表示されれば起動成功です。

The bot has started successfully when you see a log similar to:

```text
Logged in as ...
```

Botを停止するには、ターミナルで `Ctrl+C` を押します。

Press `Ctrl+C` in the terminal to stop the bot.

## 使用方法 / Usage

1. Botが起動していることを確認する。
2. ログを取得したいDiscordチャンネルで `/export` と入力する。
3. 必要に応じて引数を設定する。
4. コマンドを実行すると、ログファイルが添付された埋め込みメッセージが送信される。

1. Make sure the bot is running.
2. Type `/export` in the Discord channel whose logs you want to retrieve.
3. Configure the optional arguments as needed.
4. Run the command. The bot sends an embedded result message with the log file attached.

### `/export` の引数 / `/export` Arguments

| 引数 / Argument | 説明 / Description | デフォルト / Default |
| --- | --- | --- |
| `limit` | 取得するメッセージ数 / Number of messages to retrieve | `100` |
| `use_sjis` | `True`でShift_JIS（CP932）、`False`でUTF-8（BOM付き） / `True` for Shift_JIS (CP932), `False` for UTF-8 with BOM | `False` |
| `include_user_id` | ログにユーザーIDを含めるか / Whether to include user IDs | `True` |
| `user_name_type` | `username`、`both`、`display_name`から選択 / Choose `username`, `both`, or `display_name` | `username` |

ユーザー名タイプの意味:

- `username`: ユーザー名のみ
- `both`: ユーザー名と表示名
- `display_name`: 表示名のみ

User name display types:

- `username`: Username only
- `both`: Username and display name
- `display_name`: Display name only

## 出力ファイル / Output File

ファイル名は以下の形式です。

The filename uses the following format:

```text
log_[チャンネル名]in[サーバー名].txt
```

例 / Example:

```text
log_generalinMyServer.txt
```

UTF-8を選択した場合はBOM付きで出力されます。Shift_JISで表現できない文字は置換されます。

UTF-8 output includes a BOM. Characters unsupported by Shift_JIS are replaced when CP932 is selected.

## トラブルシューティング / Troubleshooting

### `403 Forbidden (error code: 50001): Missing Access`

Botに対象チャンネルへのアクセス権がありません。対象チャンネルの権限設定を確認し、Botに以下を許可してください。

- チャンネルを見る / View Channels
- メッセージ履歴を読む / Read Message History

The bot cannot access the target channel. Check the channel-specific permissions and allow View Channels and Read Message History.

### スラッシュコマンドが表示されない / The slash command does not appear

- Botが `applications.commands` スコープ付きで招待されているか確認する。
- Botを再起動する。
- Discord側でコマンドの反映に少し時間がかかる場合がある。

- Make sure the bot was invited with the `applications.commands` scope.
- Restart the bot.
- Discord may take some time to update slash commands.

### `TOKENが見つかりません` / `TOKEN not found`

`.env` がプロジェクトのルートにあり、次の形式でTokenが設定されているか確認してください。

Make sure `.env` is in the project root and contains the token in this format:

```dotenv
TOKEN=your_bot_token
```

## セキュリティ上の注意 / Security Notes

- Bot Tokenを他人に共有しない。
- `.env` をGitにコミットしない。
- Tokenを公開してしまった場合は、Developer PortalでTokenを再生成する。
- 取得したログには個人情報が含まれる可能性があるため、取り扱いに注意する。

- Never share the bot token.
- Do not commit `.env` to Git.
- If the token is exposed, regenerate it in the Developer Portal.
- Exported logs may contain personal information; handle them carefully.
