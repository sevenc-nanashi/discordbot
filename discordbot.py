from functions import run_command
from functions import get_user_myself
from discord.message import Message
from discord.user import User
from discord.reaction import Reaction
from discord import Client
import os
import traceback
import discord

client = Client()
debug_mode = False

@client.event
async def on_ready() -> None:
    """起動時に実行する"""
    print('Logged in')
    await client.edit_profile(username="Echidna")


@client.event
async def on_message(message: Message) -> None:
    """メッセージ受信時に実行する"""
    try:
        if message.author == client.user:
            return
        else:
            await run_command(client, message)
    except Exception as e:
        await client.send_message(message.channel, str(e))
        if debug_mode:
            traceback_msg = '```\n{}\n```'.format(traceback.format_exc())
            await client.send_message(message.channel, traceback_msg)
    else:
        pass
    finally:
        pass


@client.event
async def on_reaction_add(reaction: Reaction, user: User) -> None:
    """リアクションが付いた時に実行する"""
    myself = get_user_myself(reaction.message)
    if reaction.message.author == myself:
        msg = f'{user} が {reaction.message.content} に {reaction.emoji} を付けました'
        await client.send_message(myself, msg)


@client.event
async def on_reaction_remove(reaction: Reaction, user: User) -> None:
    """リアクション削除時に実行する"""
    myself = get_user_myself(reaction.message)
    if reaction.message.author == myself:
        msg = f'{user} が {reaction.message.content} の {reaction.emoji} を削除しました'
        await client.send_message(myself, msg)


def main() -> None:
    client.run(os.environ['DISCORD_BOT_TOKEN'])


if __name__ == '__main__':
    main()
