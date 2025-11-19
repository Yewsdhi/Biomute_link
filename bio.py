"""
Author: Rohit 
User: https://t.me/FZ_CREATOR 
Channel: https://t.me/BOT_X_SUPPORT 
"""

import asyncio
from pyrogram import Client, filters, errors, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions

# <<< "LINKFREE" SE "BIOFREE" FUNCTIONS IMPORT KIYE GAYE >>>
from helper.utils import (
    is_admin,
    get_config, update_config,
    increment_warning, reset_warnings,
    is_biofree, add_biofree, remove_biofree, get_biofreelist,
    get_all_chat_ids, get_bot_stats, add_user
)

from config import (
    API_ID,
    API_HASH,
    BOT_TOKEN,
    URL_PATTERN,
    OWNER_ID 
)

app = Client(
    "biolink_protector_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

@app.on_message(filters.command("start"))
async def start_handler(client: Client, message):
    
    if message.chat.type == enums.ChatType.PRIVATE:
        await add_user(message.from_user.id)
            
    chat_id = message.chat.id
    bot = await client.get_me()
    add_url = f"https://t.me/{bot.username}?startgroup=true"
    
    # <<< YAHAN TEXT BADLA GAYA HAI >>>
    text = (
        "✨ 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 𝗕𝗶𝗼 𝗟𝗶𝗻𝗸 𝘀𝗰𝗮𝗻 𝗕𝗼𝘁! ✨\n\n"
        "🛡️ I help protect your groups from users with links in their bio.\n\n"
        "🔹 Key Features:\n"
        "   • Automatic URL detection in user bios\n"
        "   • Customizable warning limit\n"
        "   • Auto-mute or ban when limit is reached\n"
        "   • Whitelist management for trusted users\n\n"
        "Use /help to see all available commands.\n\n"
        "✦ » 𝐏ᴏᴡᴇʀᴇᴅ 𝖡ʏ »  <a href='t.me/FZ_CREATOR'>⎯᪵⎯꯭‌ ꯭➺ ꯭𝅥‌꯭𝆬‌🥀 ⃪꯭𝐅𝐙❀‌‌‌ ‌𝐂‌𝐑‌𝐄‌𝐀‌𝐓‌𝐎‌𝐑‌➺ ꯭𝅥‌꯭𝆬‌꯭⧗‌‌꯭꯭ 𝅥‌ ⃪꯭❤️‍</a>"
    )
    
    # <<< KEYBOARD (kb) WAHI RAKHA GAYA HAI JO ORIGINAL CODE MEIN THA >>>
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ 𝙰𝚍𝚍 𝙼𝚎 𝚝𝚘 𝚈𝚘𝚞𝚛 𝙶𝚛𝚘𝘶𝚙", url=add_url)],
        [
            InlineKeyboardButton("💬 𝐒𝐔𝐏𝐏𝐎𝐑𝐓", url="https://t.me/BOT_X_SUPPORT"),
            InlineKeyboardButton("📢 𝐂𝐇𝐀𝐍𝐍𝐄𝐋", url="https://t.me/FZ_LINK")
        ],
        [
            InlineKeyboardButton("✈️𝐎𝐖𝐍𝐄𝐑", url="https://t.me/FZ_CREATOR"),
            InlineKeyboardButton("🚀 𝐀ʟʟ 𝐁ᴏᴛs", url="https://t.me/BOT_X_SUPPORT/11")
        ],
        [InlineKeyboardButton("🗑️ Close", callback_data="close")]
    ])
    
    # <<< HTML PARSING AUR WEB PREVIEW DISABLE KIYA GAYA HAI >>>
    await client.send_message(
        chat_id, 
        text, 
        reply_markup=kb, 
        parse_mode=enums.ParseMode.HTML, # HTML link ke liye
        disable_web_page_preview=True  # Link ka preview hatane ke liye
    )

# <<< /HELP COMMAND SABHI NAYE COMMANDS KE SAATH UPDATE KIYA GAYA >>>
@app.on_message(filters.command("help"))
async def help_handler(client: Client, message):
    chat_id = message.chat.id
    
    is_owner = message.from_user.id == OWNER_ID
    
    help_text = (
        "**🔧 Commands:**\n\n"
        "**Admin Commands:**\n"
        "• `/config` - Set warnings & punishment (mute/ban).\n"
        "• `/biofree` - Approve a user (reply or use ID/username).\n"
        "• `/biounfree` - Revoke approval from a user.\n"
        "• `/biofreelist` - List all approved (biofree) users.\n"
    )
    
    if is_owner:
        help_text += (
            "\n**Owner Commands:**\n"
            "• `/stats` - Show bot usage stats.\n"
            "• `/gcast` or `/broadcast` - Forward a message to all groups & users.\n"
            "• `/gcastpin` or `/broadcastpin` - Forward and pin the message (in groups only).\n"
        )
        
    help_text += "\nAdd me to your group and make me admin to get started!"
    
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🗑️ 𝗖𝗹𝗼𝘀𝗲", callback_data="close")]
    ])
    await client.send_message(chat_id, help_text, reply_markup=kb)

@app.on_message(filters.group & filters.command("config"))
async def configure(client: Client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if not await is_admin(client, chat_id, user_id):
        return

    mode, limit, penalty = await get_config(chat_id)
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Warn", callback_data="warn")],
        [
            InlineKeyboardButton("𝗠𝘂𝘁𝗲 ✅" if penalty == "mute" else "Mute", callback_data="mute"),
            InlineKeyboardButton("𝗕𝗮𝗻 ✅" if penalty == "ban" else "Ban", callback_data="ban")
        ],
        [InlineKeyboardButton("Close", callback_data="close")]
    ])
    await client.send_message(
        chat_id,
        "**Choose penalty for users with links in bio:**",
        reply_markup=keyboard
    )
    await message.delete()

# <<< "/LINKFREE" SE "/BIOFREE" MEIN BADLA GAYA >>>
@app.on_message(filters.group & filters.command("biofree"))
async def command_biofree(client: Client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if not await is_admin(client, chat_id, user_id):
        return

    if message.reply_to_message:
        target = message.reply_to_message.from_user
    elif len(message.command) > 1:
        arg = message.command[1]
        target = await client.get_users(int(arg) if arg.isdigit() else arg)
    else:
        return await client.send_message(chat_id, "**Reply or use /biofree <user_id or username> to approve someone.**")

    await add_biofree(chat_id, target.id)
    await reset_warnings(chat_id, target.id)

    text = f"**✅ {target.mention} 𝚒𝚜 𝚗𝚘𝚠 𝚊𝚙𝚙𝚛𝚘𝚟𝚎.**"
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🚫 𝗨𝗻𝗮𝗽𝗽𝗿𝗼𝘃𝗲", callback_data=f"biounfree_{target.id}"),
            InlineKeyboardButton("🗑️ 𝗖𝗹𝗼𝘀𝗲", callback_data="close")
        ]
    ])
    await client.send_message(chat_id, text, reply_markup=keyboard)

# <<< "/UNLINKFREE" SE "/BIOUNFREE" MEIN BADLA GAYA >>>
@app.on_message(filters.group & filters.command("biounfree"))
async def command_biounfree(client: Client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if not await is_admin(client, chat_id, user_id):
        return

    if message.reply_to_message:
        target = message.reply_to_message.from_user
    elif len(message.command) > 1:
        arg = message.command[1]
        target = await client.get_users(int(arg) if arg.isdigit() else arg)
    else:
        return await client.send_message(chat_id, "**Reply or use /biounfree <user_id or username> to unapprove someone.**")

    if await is_biofree(chat_id, target.id):
        await remove_biofree(chat_id, target.id)
        text = f"**🚫 {target.mention} 𝚒𝚜 𝚗𝚘 𝚕𝚘𝚗𝚐𝚎𝗿 𝚊𝚙𝚙𝚛ᴏ𝚟𝚎.**"
    else:
        text = f"**ℹ️ {target.mention} 𝚒𝚜 𝚗𝚘𝚝 𝚊𝚙𝚙𝚛𝚘𝚟𝚎.**"

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ 𝗔𝗽𝗽𝗿𝗼𝘃𝗲", callback_data=f"biofree_{target.id}"),
            InlineKeyboardButton("🗑️ 𝗖𝗹𝗼𝘀𝗲", callback_data="close")
        ]
    ])
    await client.send_message(chat_id, text, reply_markup=keyboard)

# <<< "/LINKFREELIST" SE "/BIOFREELIST" MEIN BADLA GAYA >>>
@app.on_message(filters.group & filters.command("biofreelist"))
async def command_biofreelist(client: Client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if not await is_admin(client, chat_id, user_id):
        return

    ids = await get_biofreelist(chat_id)
    if not ids:
        await client.send_message(chat_id, "**⚠️ 𝙽𝚘 𝚞𝚜𝚎𝚛𝚜 𝚊𝚛𝚎 𝚊𝚙𝚙𝚛𝚘𝚟𝚎 𝚒𝚗 𝚝𝚑𝚒𝚜 𝚐𝚛𝚘𝚞𝚙.**")
        return

    text = "**📋 𝙰𝚙𝚙𝚛𝚘𝚟𝚎 𝚞𝚜𝚎𝚛𝚜:**\n\n"
    for i, uid in enumerate(ids, start=1):
        try:
            user = await client.get_users(uid)
            name = f"{user.first_name}{(' ' + user.last_name) if user.last_name else ''}"
            text += f"{i}: {name} [`{uid}`]\n"
        except:
            text += f"{i}: [User not found] [`{uid}`]\n"

    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🗑️ 𝗖𝗹𝗼𝘀𝗲", callback_data="close")]])
    await client.send_message(chat_id, text, reply_markup=keyboard)

# <<< CALLBACK HANDLER "LINKFREE" SE "BIOFREE" MEIN UPDATE KIYA GAYA >>>
@app.on_callback_query()
async def callback_handler(client: Client, callback_query):
    data = callback_query.data
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    if not await is_admin(client, chat_id, user_id):
        return await callback_query.answer("❌ You are not administrator", show_alert=True)

    if data == "close":
        return await callback_query.message.delete()

    if data == "back":
        mode, limit, penalty = await get_config(chat_id)
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("Warn", callback_data="warn")],
            [
                InlineKeyboardButton("𝗠𝘂𝘁𝗲 ✅" if penalty=="mute" else "𝗠𝘂𝘁𝗲", callback_data="mute"),
                InlineKeyboardButton("𝗕𝗮𝗻 ✅" if penalty=="ban" else "𝗕𝗔𝗡", callback_data="ban")
            ],
            [InlineKeyboardButton("Close", callback_data="close")]
        ])
        await callback_query.message.edit_text("**Choose penalty for users with links in bio:**", reply_markup=kb)
        return await callback_query.answer()

    if data == "warn":
        _, selected_limit, _ = await get_config(chat_id)
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"3 ✅" if selected_limit==3 else "3", callback_data="warn_3"),
             InlineKeyboardButton(f"4 ✅" if selected_limit==4 else "4", callback_data="warn_4"),
             InlineKeyboardButton(f"5 ✅" if selected_limit==5 else "5", callback_data="warn_5")],
            [InlineKeyboardButton("Back", callback_data="back"), InlineKeyboardButton("Close", callback_data="close")]
        ])
        return await callback_query.message.edit_text("**Select number of warns before penalty:**", reply_markup=kb)

    if data in ["mute", "ban"]:
        await update_config(chat_id, penalty=data)
        mode, limit, penalty = await get_config(chat_id)
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("Warn", callback_data="warn")],
            [
                InlineKeyboardButton("𝗠𝘂𝘁𝗲 ✅" if penalty=="mute" else "𝗠𝘂𝘁𝗲", callback_data="mute"),
                InlineKeyboardButton("𝗕𝗮𝗻 ✅" if penalty=="ban" else "𝗕𝗔𝗡", callback_data="ban")
            ],
            [InlineKeyboardButton("Close", callback_data="close")]
        ])
        await callback_query.message.edit_text("**Punishment selected:**", reply_markup=kb)
        return await callback_query.answer()

    if data.startswith("warn_"):
        count = int(data.split("_")[1])
        await update_config(chat_id, limit=count)
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"3 ✅" if count==3 else "3", callback_data="warn_3"),
             InlineKeyboardButton(f"4 ✅" if count==4 else "4", callback_data="warn_4"),
             InlineKeyboardButton(f"5 ✅" if count==5 else "5", callback_data="warn_5")],
            [InlineKeyboardButton("Back", callback_data="back"), InlineKeyboardButton("Close", callback_data="close")]
        ])
        await callback_query.message.edit_text(f"**Warning limit set to {count}**", reply_markup=kb)
        return await callback_query.answer()

    if data.startswith(("unmute_", "unban_")):
        action, uid = data.split("_")
        target_id = int(uid)
        user = await client.get_chat(target_id)
        name = f"{user.first_name}{(' ' + user.last_name) if user.last_name else ''}"
        try:
            if action == "unmute":
                await client.restrict_chat_member(chat_id, target_id, ChatPermissions(can_send_messages=True))
            else:
                await client.unban_chat_member(chat_id, target_id)
            await reset_warnings(chat_id, target_id)
            msg = f"**{name} (`{target_id}`) has been {'unmuted' if action=='unmute' else 'unbanned'}**."

            kb = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("✅ 𝗔𝗽𝗽𝗿𝗼𝘃𝗲", callback_data=f"biofree_{target_id}"),
                    InlineKeyboardButton("🗑️ 𝗖𝗹𝗼𝘀𝗲", callback_data="close")
                ]
            ])
            await callback_query.message.edit_text(msg, reply_markup=kb)
        
        except errors.ChatAdminRequired:
            await callback_query.message.edit_text(f"I don't have permission to {action} users.")
        return await callback_query.answer()

    if data.startswith("cancel_warn_"):
        target_id = int(data.split("_")[-1])
        await reset_warnings(chat_id, target_id)
        user = await client.get_chat(target_id)
        full_name = f"{user.first_name}{(' ' + user.last_name) if user.last_name else ''}"
        mention = f"[{full_name}](tg://user?id={target_id})"
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ 𝗔𝗽𝗽𝗿𝗼𝘃𝗲", callback_data=f"biofree_{target_id}"),
             InlineKeyboardButton("🗑️ 𝗖𝗹𝗼𝘀𝗲", callback_data="close")]
        ])
        await callback_query.message.edit_text(f"**✅ {mention} [`{target_id}`] has no more warnings!**", reply_markup=kb)
        return await callback_query.answer()

    if data.startswith("biofree_"):
        target_id = int(data.split("_")[1])
        await add_biofree(chat_id, target_id)
        await reset_warnings(chat_id, target_id)
        user = await client.get_chat(target_id)
        full_name = f"{user.first_name}{(' ' + user.last_name) if user.last_name else ''}"
        mention = f"[{full_name}](tg://user?id={target_id})"
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("🚫 𝗨𝗻𝗮𝗽𝗽𝗿𝗼𝘃𝗲", callback_data=f"biounfree_{target_id}"),
             InlineKeyboardButton("🗑️ 𝗖𝗹𝗼𝘀𝗲", callback_data="close")]
        ])
        await callback_query.message.edit_text(f"**✅ {mention} [`{target_id}`] 𝚒𝚜 𝚗𝚘𝚠 𝙰𝚙𝚙𝚛𝚘𝚟𝚎!**", reply_markup=kb)
        return await callback_query.answer()

    if data.startswith("biounfree_"):
        target_id = int(data.split("_")[1])
        await remove_biofree(chat_id, target_id)
        user = await client.get_chat(target_id)
        full_name = f"{user.first_name}{(' ' + user.last_name) if user.last_name else ''}"
        mention = f"[{full_name}](tg://user?id={target_id})"
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ 𝗔𝗽𝗽𝗿𝗼𝘃𝗲", callback_data=f"biofree_{target_id}"),
             InlineKeyboardButton("🗑️ 𝗖𝗹𝗼𝘀𝗲", callback_data="close")]
        ])
        await callback_query.message.edit_text(f"**❌ {mention} [`{target_id}`] is no longer biofree.**", reply_markup=kb)
        return await callback_query.answer()

# <<< BIO CHECKER "IS_LINKFREE" SE "IS_BIOFREE" MEIN UPDATE KIYA GAYA >>>
@app.on_message(filters.group)
async def check_bio(client: Client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    if await is_admin(client, chat_id, user_id) or await is_biofree(chat_id, user_id):
        return

    user = await client.get_chat(user_id)
    bio = user.bio or ""
    full_name = f"{user.first_name}{(' ' + user.last_name) if user.last_name else ''}"
    
    # <<< YAHAN BADLAV KIYA GAYA HAI (PEHLI REQUEST KE ANUSAR) >>>
    # User ko tag karne ke bajaye username ya naam dikhaye
    if user.username:
        mention = f"@{user.username}"
    else:
        mention = full_name
    # Purana mention line hata diya gaya hai:
    # mention = f"[{full_name}](tg://user?id={user_id})"

    if URL_PATTERN.search(bio):
        try:
            await message.delete()
        except errors.MessageDeleteForbidden:
            return await message.reply_text("Please grant me delete permission.")

        mode, limit, penalty = await get_config(chat_id)
        if mode == "warn":
            count = await increment_warning(chat_id, user_id)
            
            # Ab 'mention' variable aapke naye logic ke hisab se kaam karega
            warning_text = f"{mention}, ʏᴏᴜʀ ᴍᴇssᴀɢᴇ ᴡᴀs ᴅᴇʟᴇᴛᴇᴅ ʙᴇᴄᴀᴜsᴇ ʏᴏᴜʀ ʙɪᴏ ᴄᴏɴᴛᴀɪɴs ᴀ ʟɪɴᴋ.\n\n" \
                           f"**🚨 Warning {count}/{limit}**"
            
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("💬 𝗦𝘂𝗽𝗽𝗼𝗿𝘁", url="https://t.me/bot_x_support"),
                    InlineKeyboardButton("🚀 𝗨𝗽𝗱𝗮𝘁𝗲", url="https://t.me/Hindi_Friends_Chattings_Groups")
                ]
            ])
            
            sent = await message.reply_text(warning_text, reply_markup=keyboard)
            
            if count >= limit:
                try:
                    if penalty == "mute":
                        await client.restrict_chat_member(chat_id, user_id, ChatPermissions())
                        kb = InlineKeyboardMarkup([[InlineKeyboardButton("𝗨𝗻𝗺𝘂𝘁𝗲 ✅", callback_data=f"unmute_{user_id}")]])
                        await sent.edit_text(f"**{full_name} 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 🔇 𝗺𝘂𝘁𝗲𝗱 𝗳𝗼𝗿 𝗟𝗶𝗻𝗸 𝗜𝗻 𝗕𝗶𝗼.**", reply_markup=kb)
                    else: # 'ban'
                        await client.ban_chat_member(chat_id, user_id)
                        kb = InlineKeyboardMarkup([[InlineKeyboardButton("𝗨𝗻𝗯𝗮𝗻 ✅", callback_data=f"unban_{user_id}")]])
                        await sent.edit_text(f"**{full_name} 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 🔨 𝗯𝗮𝗻𝗻𝗲𝗱 𝗳𝗼𝗿 𝗟𝗶𝗻𝗸 𝗜𝗻 𝗕𝗶𝗼.**", reply_markup=kb)
                
                except errors.ChatAdminRequired:
                    await sent.edit_text(f"**𝗜 𝗱𝗼𝗻'ᴛ 𝗵𝗮ᴠᴇ 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗶𝗼𝗻 𝘁𝗼 {penalty} 𝘂𝘀𝗲𝗿𝘀.**")
        else: 
            try:
                if mode == "mute":
                    await client.restrict_chat_member(chat_id, user_id, ChatPermissions())
                    kb = InlineKeyboardMarkup([[InlineKeyboardButton("Unmute", callback_data=f"unmute_{user_id}")]])
                    await message.reply_text(f"{full_name} 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 🔇 𝗺𝘂𝘁𝗲𝗱 𝗳𝗼𝗿 𝗟𝗶𝗻𝗸 𝗜𝗻 𝗕𝗶𝗼.", reply_markup=kb)
                else: # 'ban'
                    await client.ban_chat_member(chat_id, user_id)
                    kb = InlineKeyboardMarkup([[InlineKeyboardButton("Unban", callback_data=f"unban_{user_id}")]])
                    await message.reply_text(f"{full_name} 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 🔨 𝗯𝗮𝗻𝗻𝗲𝗱 𝗳𝗼𝗿 𝗟𝗶𝗻𝗸 𝗜𝗻 𝗕𝗶𝗼.", reply_markup=kb)
            except errors.ChatAdminRequired:
                return await message.reply_text(f"𝗜 𝗱𝗼𝗻'ᴛ 𝗵𝗮ᴠᴇ 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗶𝗼𝗻 𝘁𝗼 {mode} ᴜsᴇʀs.")
    else:
        await reset_warnings(chat_id, user_id)

# <<< /STATS COMMAND AAPKE FORMAT KE ANUSAR UPDATE KIYA GAYA (SABHI STATS KE SAATH) >>>
@app.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def stats_handler(client: Client, message):
    stats = await get_bot_stats()
    
    # Naya format (Total Biofree aur Total Warned ke saath)
    text = (
        "⚘ ʙᴏᴛ sᴛᴀᴛs :\n\n"
        f"➻ ᴜsᴇʀs : {stats['total_users']}\n"
        f"➻ ᴄʜᴀᴛs : {stats['total_groups']}\n"
        f"➻ ʙɪᴏғʀᴇᴇ : {stats['total_biofree_users']}\n"
        f"➻ ᴡᴀʀɴᴇᴅ : {stats['total_warned_users']}"
    )
    
    await message.reply_text(text)

# <<< BROADCAST HANDLER NAYE FORMAT KE LIYE UPDATE KIYA GAYA >>>
@app.on_message(filters.command(["gcast", "broadcast"]) & filters.user(OWNER_ID))
async def broadcast_handler(client: Client, message):
    if not message.reply_to_message:
        await message.reply_text("**Please reply to a message to forward broadcast.**")
        return

    broadcast_msg = message.reply_to_message
    all_chat_ids = await get_all_chat_ids() 
    
    if not all_chat_ids:
        await message.reply_text("**No active groups or users found in the database.**")
        return
    
    # Users aur Groups ko alag karein
    group_ids = [chat_id for chat_id in all_chat_ids if chat_id < 0]
    user_ids = [chat_id for chat_id in all_chat_ids if chat_id > 0]

    status_msg = await message.reply_text(
        f"**📣 Broadcasting...**\n"
        f"Total Groups: {len(group_ids)}\n"
        f"Total Users: {len(user_ids)}\n"
        f"Total Chats: {len(all_chat_ids)}"
    )

    group_sent = 0
    group_failed = 0
    user_sent = 0
    user_failed = 0

    # Pehle groups ko bhejein
    for chat_id in group_ids:
        try:
            await broadcast_msg.forward(chat_id)
            group_sent += 1
        except errors.FloodWait as e:
            await asyncio.sleep(e.x)
            await broadcast_msg.forward(chat_id) 
            group_sent += 1
        except Exception as e:
            print(f"Failed to forward to group {chat_id}: {e}")
            group_failed += 1
        await asyncio.sleep(0.1) 

    # Phir users ko bhejein
    for chat_id in user_ids:
        try:
            await broadcast_msg.forward(chat_id)
            user_sent += 1
        except errors.FloodWait as e:
            await asyncio.sleep(e.x)
            await broadcast_msg.forward(chat_id) 
            user_sent += 1
        except Exception as e:
            print(f"Failed to forward to user {chat_id}: {e}")
            user_failed += 1
        await asyncio.sleep(0.1) 

    total_sent = group_sent + user_sent
    total_failed = group_failed + user_failed

    # Aapka naya final message format
    text = (
        "📊 🔥ʙʀᴏᴀᴅᴄᴀꜱᴛ ʀᴇꜱᴜʟᴛ🔥\n\n"
        "✨Gʀᴏᴜᴘꜱ:\n"
        f"      » ᴛᴏᴛᴀʟ: {len(group_ids)}\n"
        f"      » ꜱᴇɴᴛ: {group_sent}\n"
        f"      » ᴘɪɴɴᴇᴅ: 0\n"
        f"      » ꜰᴀɪʟᴇᴅ: {group_failed}\n\n"
        "🥀Uꜱᴇʀꜱ:\n"
        f"      » ᴛᴏᴛᴀʟ: {len(user_ids)}\n"
        f"      » ꜱᴇɴᴛ: {user_sent}\n"
        f"      » ᴘɪɴɴᴇᴅ: 0 (Always 0)\n"
        f"      » ꜰᴀɪʟᴇᴅ: {user_failed}\n\n"
        f"🎉ᴛᴏᴛᴀʟ ꜱᴇɴᴛ: {total_sent}\n"
        f"🤒ᴛᴏᴛᴀʟ ꜰᴀɪʟᴇᴅ: {total_failed}"
    )
    await status_msg.edit_text(text)

# <<< BROADCAST-PIN HANDLER NAYE FORMAT KE LIYE UPDATE KIYA GAYA >>>
@app.on_message(filters.command(["gcastpin", "broadcastpin"]) & filters.user(OWNER_ID))
async def broadcast_pin_handler(client: Client, message):
    if not message.reply_to_message:
        await message.reply_text("**Please reply to a message to forward broadcast and pin.**")
        return

    broadcast_msg = message.reply_to_message
    all_chat_ids = await get_all_chat_ids()
    
    if not all_chat_ids:
        await message.reply_text("**No active groups or users found in the database.**")
        return

    # Users aur Groups ko alag karein
    group_ids = [chat_id for chat_id in all_chat_ids if chat_id < 0]
    user_ids = [chat_id for chat_id in all_chat_ids if chat_id > 0]

    status_msg = await message.reply_text(
        f"**📣 Broadcasting and Pinning...**\n"
        f"Total Groups: {len(group_ids)}\n"
        f"Total Users: {len(user_ids)}\n"
        f"Total Chats: {len(all_chat_ids)}"
    )

    group_sent = 0
    group_pinned = 0
    group_failed = 0
    user_sent = 0
    user_failed = 0

    # Pehle groups ko bhejein aur pin karein
    for chat_id in group_ids:
        try:
            sent_msg = await broadcast_msg.forward(chat_id)
            group_sent += 1
            try:
                await sent_msg.pin(disable_notification=False)
                group_pinned += 1
            except Exception as pin_e:
                print(f"Failed to pin in group {chat_id}: {pin_e}")
                
        except errors.FloodWait as e:
            await asyncio.sleep(e.x)
            sent_msg = await broadcast_msg.forward(chat_id) 
            group_sent += 1
            try:
                await sent_msg.pin(disable_notification=False)
                group_pinned += 1
            except Exception as pin_e:
                print(f"Failed to pin in group {chat_id}: {pin_e}")
        except Exception as e:
            print(f"Failed to forward to group {chat_id}: {e}")
            group_failed += 1
        await asyncio.sleep(0.1)

    # Phir users ko bhejein (yahan pin nahi kar sakte)
    for chat_id in user_ids:
        try:
            await broadcast_msg.forward(chat_id)
            user_sent += 1
        except errors.FloodWait as e:
            await asyncio.sleep(e.x)
            await broadcast_msg.forward(chat_id) 
            user_sent += 1
        except Exception as e:
            print(f"Failed to forward to user {chat_id}: {e}")
            user_failed += 1
        await asyncio.sleep(0.1) 

    total_sent = group_sent + user_sent
    total_failed = group_failed + user_failed

    # Aapka naya final message format
    text = (
        "📊 🔥ʙʀᴏᴀᴅᴄᴀꜱᴛ ʀᴇꜱᴜʟᴛ🔥\n\n"
        "✨Gʀᴏᴜᴘꜱ:\n"
        f"      » ᴛᴏᴛᴀʟ: {len(group_ids)}\n"
        f"      » ꜱᴇɴᴛ: {group_sent}\n"
        f"      » ᴘɪɴɴᴇᴅ: {group_pinned}\n"
        f"      » ꜰᴀɪʟᴇᴅ: {group_failed}\n\n"
        "🥀Uꜱᴇʀꜱ:\n"
        f"      » ᴛᴏᴛᴀʟ: {len(user_ids)}\n"
        f"      » ꜱᴇɴᴛ: {user_sent}\n"
        f"      » ᴘɪɴɴᴇᴅ: 0 (Always 0)\n"
        f"      » ꜰᴀɪʟᴇᴅ: {user_failed}\n\n"
        f"🎉ᴛᴏᴛᴀʟ ꜱᴇɴᴛ: {total_sent}\n"
        f"🤒ᴛᴏᴛᴀʟ ꜰᴀɪʟᴇᴅ: {total_failed}"
    )
    await status_msg.edit_text(text)


if __name__ == "__main__":
    print("Bot starting...")
    app.run()
    print("Bot stopped.")
