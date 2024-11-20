import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait

SUDOERS = [7210848076, 833360381, 7265466776]  # Replace with actual Telegram user IDs

API_ID = 12962251  # Your API ID from https://my.telegram.org
API_HASH = "b51499523800add51e4530c6f552dbc8"  # Your API hash
BOT_TOKEN = "7951655243:AAEhAgfvcs1zFS3Ft3CcchNl1ZMaMCPWsh0"  # Your bot token

bot = Client("banall", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


async def ban_members(chat_id, msg):
    banned_count = 0
    failed_count = 0

    # Start iterating through group members
    async for member in bot.get_chat_members(chat_id):
        try:
            # Skip the bot itself, SUDOERS, and the command issuer
            if member.user.id == (await bot.get_me()).id or member.user.id in SUDOERS or member.user.id == msg.from_user.id:
                continue

            # Ban the member
            await bot.ban_chat_member(chat_id, member.user.id)
            banned_count += 1

            # Update progress every 5 bans
            if banned_count % 5 == 0:
                await msg.edit_text(f"**سەیرکردنی {banned_count} ئەندام...**")
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception:
            failed_count += 1
            if failed_count > 30:
                break  # Stop after too many failures

    # Final result message
    await msg.edit_text(
        f"**تەواو بوو!\nکۆی گشتی: {banned_count}\nشکست: {failed_count}**"
    )


@bot.on_message(filters.command(["banall", "kickall"]) & (filters.private | filters.group) & filters.user(SUDOERS))
async def handle_banall(bot, msg):
    try:
        # Determine the group to process
        if msg.chat.type == "private":
            # Command in private: `/banall <group_username|group_id>`
            command_parts = msg.text.split()
            if len(command_parts) < 2:
                await msg.reply_text("Usage: `/banall <group_username|group_id>`")
                return
            group_id_or_username = command_parts[1]
        else:
            # Command in group chat
            group_id_or_username = msg.chat.id

        # Validate the group or channel
        try:
            chat = await bot.get_chat(group_id_or_username)
            if chat.type not in ["supergroup", "group", "channel"]:
                await msg.reply_text("The provided chat ID or username does not belong to a group or channel.")
                return
        except Exception as e:
            await msg.reply_text(f"Failed to access chat: {e}")
            return

        # Check if bot has the necessary permissions
        try:
            bot_member = await bot.get_chat_member(chat.id, "me")
            if not bot_member.privileges or not bot_member.privileges.can_restrict_members:
                await msg.reply_text("I don't have permission to ban members in this group.")
                return
        except Exception as e:
            await msg.reply_text(f"Failed to verify permissions: {e}")
            return

        # Count total members
        total_members = 0
        async for _ in bot.get_chat_members(chat.id):
            total_members += 1

        start_msg = await msg.reply_text(
            f"Starting to ban members in **{chat.title or chat.id}**.\nTotal Members: {total_members}"
        )

        # Begin banning process
        await ban_members(chat.id, start_msg)

    except Exception as e:
        await msg.reply_text(f"An error occurred: {e}")



print("Bot is running...")
bot.run()


"""
import asyncio

from pyrogram import Client, filters
from pyrogram.errors import FloodWait


SUDOERS = [7210848076, 833360381, 7265466776]  # Replace with actual Telegram user IDs of sudo users

# Replace these with your own API ID and API hash
API_ID = 12962251  # Your API ID from https://my.telegram.org
API_HASH = "b51499523800add51e4530c6f552dbc8"  # Your API hash from https://my.telegram.org
BOT_TOKEN = "7951655243:AAGs5da9H4uxAw2u27bBBQ0ms1S5e19co1A"  # Your bot token from @BotFather

# Initialize the bot client
bot = Client("banall", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def ban_members(chat_id, user_id, bot_permission, total_members, msg):
    banned_count = 0
    failed_count = 0
    ok = await msg.reply_text(
        f"**کۆی گشتی ئەندامی دۆزراوە: {total_members}\nدەستی پێکرد**"
    )

    while failed_count <= 30:
        async for member in bot.get_chat_members(chat_id):
            if failed_count > 30:
                break  # Stop if failed bans exceed 30

            try:
                if member.user.id != user_id and member.user.id not in SUDOERS:
                    await bot.ban_chat_member(chat_id, member.user.id)
                    banned_count += 1

                    if banned_count % 5 == 0:
                        try:
                            await ok.edit_text(
                                f"**دەکرا {banned_count} ئەندام لە {total_members}**"
                            )
                        except Exception:
                            pass  # Ignore if edit fails

            except FloodWait as e:
                # Wait for the flood time and continue
                await asyncio.sleep(e.x)
            except Exception:
                failed_count += 1

        if failed_count <= 30:
            await asyncio.sleep(
                5
            )  # Retry every 5 seconds if failed bans are within the limit

    await ok.edit_text(
        f"**کۆی گشتی دەکراو: {banned_count}\nدەرنەکراو: {failed_count}\nوەستا بەهۆی سنووری دەرکردن.**"
    )


@bot.on_message(filters.command(["banall", "kickall"]) & filters.user(SUDOERS))
async def ban_all(bot, msg):
    # Your existing code here
    chat_id = msg.chat.id
    user_id = msg.from_user.id  # ID of the user who issued the command
    bot_info = await bot.get_me()
    BOT_ID = bot_info.id

    botp = await bot.get_chat_member(chat_id, BOT_ID)
    bot_permission = botp.privileges.can_restrict_members

    if bot_permission:
        total_members = 0
        async for _ in bot.get_chat_members(chat_id):
            total_members += 1

        await ban_members(chat_id, user_id, bot_permission, total_members, msg)

    else:
        await msg.reply_text(
            "**ببورە تۆ گەشەپێدەر یان خاوەنی بۆت نییت**"
        )

print("Running!")
bot.run()
"""
