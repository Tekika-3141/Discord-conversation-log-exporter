
import io
import os

import discord
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True


class MyBot(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()


bot = MyBot()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.tree.command(
    name="export",
    description="このチャンネルの会話ログを抽出します"
)
@app_commands.describe(
    limit="取得するメッセージ数（デフォルト: 100）",
    use_sjis="Shift_JIS(CP932)で出力する場合はTrue",
    include_user_id="ユーザーIDを出力に含める場合はTrue",
    user_name_type="投稿者名の表示形式",
)
@app_commands.choices(
    user_name_type=[
        app_commands.Choice(
            name="ユーザー名のみ",
            value="username",
        ),
        app_commands.Choice(
            name="ユーザー名＋表示名",
            value="both",
        ),
        app_commands.Choice(
            name="表示名のみ",
            value="display_name",
        ),
    ]
)
async def export_logs(
    interaction: discord.Interaction,
    limit: int = 100,
    use_sjis: bool = False,
    include_user_id: bool = False,
    user_name_type: str = "display_name",
):
    await interaction.response.defer(ephemeral=False)

    messages = []

    try:
        async for message in interaction.channel.history(limit=limit):
            time_str = message.created_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            # 投稿者のユーザー名と表示名を取得
            username = message.author.name
            display_name = message.author.display_name

            # 投稿者名の表示形式を選択
            if user_name_type == "username":
                author_name = username

            elif user_name_type == "both":
                author_name = f"{username} ({display_name})"

            elif user_name_type == "display_name":
                author_name = display_name

            else:
                author_name = username

            # ユーザーIDを含めるか選択
            if include_user_id:
                author_info = f"{author_name} (#{message.author.id})"
            else:
                author_info = author_name

            messages.append(
                f"[{time_str}] {author_info}: "
                f"{message.content}\n"
            )
    except discord.Forbidden:
        embed = discord.Embed(
            title="ログを出力できませんでした",
            description=(
                "このチャンネルのメッセージ履歴を取得する権限がありません。\n"
                "Botに「チャンネルを見る」と「メッセージ履歴を読む」の"
                "権限を付与してください。"
            ),
            color=discord.Color.red(),
        )
        await interaction.followup.send(embed=embed, ephemeral=True)
        return

    messages.reverse()
    log_text = "".join(messages)

    if use_sjis:
        encoding_name = "cp932(Shift_JIS)"
        file_bytes = io.BytesIO(
            log_text.encode("cp932", errors="replace")
        )
    else:
        # UTF-8(BOM付き)で保存
        encoding_name = "utf-8-sig"
        file_bytes = io.BytesIO(
            log_text.encode(encoding_name)
        )

    server_name = interaction.guild.name if interaction.guild else "DM"

    file = discord.File(
        file_bytes,
        filename=f"log_{interaction.channel.name} in {server_name}.txt"
    )

    embed = discord.Embed(
        title="会話ログを出力しました",
        description=(
            "設定：\n"
            f"・件数 `{limit}`件\n"
            f"・使用文字コード `{encoding_name}`\n"
            f"・ユーザーIDの表示 `{include_user_id}`\n"
            f"・ユーザー名タイプ `{user_name_type}`"
        ),
        color=discord.Color.green(),
    )

    await interaction.followup.send(
        embed=embed,
        file=file,
        ephemeral=False,
    )


# .envからトークンを取得
TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    raise ValueError(
        "TOKENが見つかりません。.envファイルを確認してください。"
    )

# Botを起動
bot.run(TOKEN)
