# ------------- RDX MASTER SYSTEM: ENCODER & DECODER BOT -------------
import asyncio
import logging
import os
import base64
import hashlib
import secrets
import re
import urllib.parse
from Crypto.Cipher import AES
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.utils import executor

# ================= CONFIG =================
API_TOKEN = "8606851269:AAE5FPOPUU0Zgg18kZ9orSgbbDRbzQQ1Q68"

# ---------- CHANNELS ----------
CHANNEL_1_USERNAME = "RDXOWNER77"
CHANNEL_2_USERNAME = "RDXOWNER7"
CHANNEL_1_LINK = "https://t.me/RDXOWNER77"
CHANNEL_2_LINK = "https://t.me/RDXOWNER7"

# ---------- SYSTEM VARS ----------
FIXED_KEY = "RDX_FIXED_KEY_2024"
SALT = b"rdx_salt_2024"
ITERATIONS = 100000
KEY_LEN = 32
DECODER_PASSWORD = "RDXOWNER7"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# ================= STATES (Simple dict based) =================
user_states = {}
user_encrypt_state = {}

# ================= FORCE JOIN =================
async def check_join(user_id):
    try:
        m1 = await bot.get_chat_member(f"@{CHANNEL_1_USERNAME}", user_id)
        m2 = await bot.get_chat_member(f"@{CHANNEL_2_USERNAME}", user_id)
        ok = ["member", "administrator", "creator"]
        return m1.status in ok and m2.status in ok
    except:
        return False

# ================= UI HELPERS =================
def premium_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔐 ENCRYPTION ENGINE", callback_data="menu_encrypt")],
        [InlineKeyboardButton(text="🔓 DECODER SYSTEM", callback_data="menu_decode_login")],
        [InlineKeyboardButton(text="✦ CONTACT DEVELOPER ✦", url="https://t.me/RDX_OWNER_7")]
    ])

def decoder_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚙ 01: V3 ENGINE", callback_data="dec_t1")],
        [InlineKeyboardButton(text="🌐 02: DOM ENGINE", callback_data="dec_t2")],
        [InlineKeyboardButton(text="⬡ 03: NEXUS ENGINE", callback_data="dec_t3")],
        [InlineKeyboardButton(text="◈ 04: VISUAL ENGINE", callback_data="dec_t4")],
        [InlineKeyboardButton(text="← BACK TO MAIN MENU", callback_data="back_main")]
    ])

async def process_ui(msg):
    steps = [
        "⚙ INITIALIZING RDX CORE...\n[■■□□□□□□□□] 20%",
        "🔐 ANALYZING PROTOCOL...\n[■■■■■□□□□□] 50%",
        "🛡 EXECUTING ENGINE LOGIC...\n[■■■■■■■■□□] 80%",
        "🚀 FINALIZING PAYLOAD...\n[■■■■■■■■■■] 100%"
    ]
    for s in steps:
        try:
            await msg.edit_text(s)
        except:
            pass
        await asyncio.sleep(0.6)

# ================= START =================
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_states[message.from_user.id] = None
    user_encrypt_state[message.from_user.id] = None
    
    if not await check_join(message.from_user.id):
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📢 Join Channel 1", url=CHANNEL_1_LINK)],
            [InlineKeyboardButton(text="📢 Join Channel 2", url=CHANNEL_2_LINK)],
            [InlineKeyboardButton(text="✅ I've Joined", callback_data="check")]
        ])
        await message.reply("🚫 AUTHENTICATION REQUIRED\n\nAccess Denied. Join both channels first.", reply_markup=kb)
        return

    await message.reply(
        "⚡ RDX MASTER SYSTEM ⚡\n"
        "DECODER & ENCODER · VER 4.0\n\n"
        "SELECT PROTOCOL:\n\n"
        "• 🔐 ENCODER: AES-256-CBC + PBKDF2 HTML Protection\n"
        "• 🔓 DECODER: 4 Advanced Bypass Engines\n\n"
        "💀 @RDX_OWNER_7",
        reply_markup=premium_keyboard()
    )

@dp.callback_query_handler(lambda c: c.data == "check")
async def check_join_callback(call: types.CallbackQuery):
    if await check_join(call.from_user.id):
        await call.message.delete()
        await start(call.message)
    else:
        await call.answer("❌ You haven't joined both channels yet!", show_alert=True)

@dp.callback_query_handler(lambda c: c.data == "back_main")
async def back_to_main(call: types.CallbackQuery):
    user_states[call.from_user.id] = None
    user_encrypt_state[call.from_user.id] = None
    await call.message.delete()
    await start(call.message)

# ================= MENU HANDLERS =================
@dp.callback_query_handler(lambda c: c.data == "menu_encrypt")
async def ask_encrypt(call: types.CallbackQuery):
    await call.answer()
    user_encrypt_state[call.from_user.id] = "waiting"
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="← BACK", callback_data="back_main")]])
    await call.message.edit_text(
        "🔐 PROTOCOL 05: ENCRYPTION ENGINE\n\n"
        "AES-256-CBC + PBKDF2 · HTML Protection\n\n"
        "📁 Send your .html file to encrypt.\n\n"
        "👑 @RDX_OWNER_7",
        reply_markup=kb
    )

@dp.callback_query_handler(lambda c: c.data == "menu_decode_login")
async def ask_password(call: types.CallbackQuery):
    await call.answer()
    user_states[call.from_user.id] = "waiting_password"
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="← CANCEL", callback_data="back_main")]])
    await call.message.edit_text(
        "🔒 AUTHENTICATION REQUIRED\n\n"
        "ENTER SYSTEM PASSWORD TO UNLOCK DECODER ENGINES...\n\n"
        "Password: RDXOWNER7",
        reply_markup=kb
    )

@dp.callback_query_handler(lambda c: c.data.startswith("dec_"))
async def setup_decoder(call: types.CallbackQuery):
    await call.answer()
    proto = call.data
    
    if proto == "dec_t1":
        user_states[call.from_user.id] = "waiting_t1"
        title = "01: V3 ENGINE"
    elif proto == "dec_t2":
        user_states[call.from_user.id] = "waiting_t2"
        title = "02: DOM ENGINE"
    elif proto == "dec_t3":
        user_states[call.from_user.id] = "waiting_t3"
        title = "03: NEXUS ENGINE"
    elif proto == "dec_t4":
        user_states[call.from_user.id] = "waiting_t4"
        title = "04: VISUAL ENGINE"
    else:
        return
        
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="← CANCEL", callback_data="back_main")]])
    await call.message.edit_text(
        f"⚙ PROTOCOL {title}\n\n"
        "📁 Send the encrypted .html file you want to decode.",
        reply_markup=kb
    )

# ================= ENCRYPTION ENGINE =================
def encrypt_html(plaintext: str, password: str, username: str, user_id: int) -> str:
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), SALT, ITERATIONS, dklen=KEY_LEN)
    iv = secrets.token_bytes(16)
    plain_bytes = plaintext.encode('utf-8')
    pad_len = 16 - (len(plain_bytes) % 16)
    padded = plain_bytes + bytes([pad_len] * pad_len)
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(padded)
    
    iv_b64 = base64.b64encode(iv).decode('ascii')
    ct_b64 = base64.b64encode(ciphertext).decode('ascii')
    safe_key = password.replace('\\', '\\\\').replace("'", "\\'").replace('"', '\\"')

    raw_js = f"""
    (function() {{
        var content = document.documentElement.outerHTML;
        if (content.indexOf("Obfuscated By: @RDX_OWNER_7") === -1 || content.indexOf("Signature: RDX_PROTECTED") === -1) {{
            document.body.innerHTML = '<div style="display:flex;justify-content:center;align-items:center;height:100vh;background-color:#000;color:red;font-family:monospace;flex-direction:column;margin:0;"><h1 style="font-size:4rem;text-shadow:0 0 20px red;margin-bottom:10px;">⚠️ ERROR</h1><h2 style="font-size:1.5rem;">DO NOT REMOVE HEADER CREDITS!</h2><p style="color:#fff;">Tampering Detected. @RDX_OWNER_7</p></div>';
            return;
        }}
        try {{
            var k = CryptoJS.PBKDF2("{safe_key}", CryptoJS.enc.Utf8.parse("rdx_salt_2024"), {{ keySize: 256/32, iterations: 100000, hasher: CryptoJS.algo.SHA256 }});
            var d = CryptoJS.AES.decrypt(CryptoJS.lib.CipherParams.create({{ ciphertext: CryptoJS.enc.Base64.parse("{ct_b64}") }}), k, {{ iv: CryptoJS.enc.Base64.parse("{iv_b64}"), mode: CryptoJS.mode.CBC, padding: CryptoJS.pad.Pkcs7 }});
            var o = d.toString(CryptoJS.enc.Utf8);
            if(!o) throw new Error();
            document.open();
            document.write(o);
            document.close();
        }} catch(e) {{
            document.body.innerHTML = '<h2 style="color:red;text-align:center;margin-top:20vh;font-family:monospace;background:#000;padding:20px;">DECRYPTION FAILED. FILE CORRUPTED.</h2>';
        }}
    }})();
    """
    
    encoded_js = base64.b64encode(raw_js.encode('utf-8')).decode('ascii')
    stealth_loader = f"(function(w,d){{w['\\x65\\x76\\x61\\x6c'](w['\\x61\\x74\\x6f\\x62'](d));}})(window,'{encoded_js}');"

    return f"""<!DOCTYPE html>
<html lang="en">
<!--
██████╗ ██████╗ ██╗  ██╗
██╔══██╗██╔══██╗╚██╗██╔╝
██████╔╝██║  ██║ ╚███╔╝ 
██╔══██╗██║  ██║ ██╔██╗ 
██║  ██║██████╔╝██╔╝ ██╗
╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💀 FUCK BY RDX OWNER 💀
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Obfuscated By: @RDX_OWNER_7
Developer: RDX ULTRA
Signature: RDX_PROTECTED
User: @{username}
ID: {user_id}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ WARNING: DO NOT REMOVE THIS HEADER!
IF YOU REMOVE THIS, FILE WILL BE DESTROYED.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
-->
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🔒 RDX Encrypted File</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js"></script>
</head>
<body>
<script>{stealth_loader}</script>
</body>
</html>"""

# ================= DECODER ENGINES =================
def aes_decrypt_core(ct_bytes, iv_bytes, key_bytes):
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
    dec = cipher.decrypt(ct_bytes)
    pad_len = dec[-1]
    return dec[:-pad_len].decode('utf-8', errors='ignore')

def run_dom_engine(html_content):
    enc_m = re.search(r'const\s+encData\s*=\s*["\']([^"\']+)["\']', html_content)
    key_m = re.search(r'const\s+key\s*=\s*["\']([^"\']+)["\']', html_content)
    if enc_m and key_m:
        try:
            enc_data = base64.b64decode(enc_m.group(1))
            pwd = key_m.group(1).replace("\\n", "\n").encode('utf-8')
            iv = enc_data[:16]
            ct = enc_data[16:]
            key = hashlib.pbkdf2_hmac('sha256', pwd, b"rdx_salt_2024", 100000, 32)
            return aes_decrypt_core(ct, iv, key)
        except Exception:
            pass

    stealth = re.search(r"\)\(window,\s*['\"]([^'\"]+)['\"]\)", html_content)
    if stealth:
        try:
            js = base64.b64decode(stealth.group(1)).decode('utf-8')
            k_m = re.search(r'CryptoJS\.PBKDF2\(["\']([^"\']+)["\']', js)
            ct_m = re.search(r'ciphertext:\s*CryptoJS\.enc\.Base64\.parse\(["\']([^"\']+)["\']\)', js)
            iv_m = re.search(r'iv:\s*CryptoJS\.enc\.Base64\.parse\(["\']([^"\']+)["\']\)', js)
            if k_m and ct_m and iv_m:
                pwd = k_m.group(1).encode('utf-8')
                ct = base64.b64decode(ct_m.group(1))
                iv = base64.b64decode(iv_m.group(1))
                key = hashlib.pbkdf2_hmac('sha256', pwd, b"rdx_salt_2024", 100000, 32)
                return aes_decrypt_core(ct, iv, key)
        except Exception:
            pass
    return None

def run_v3_engine(html_content):
    hex_match = re.findall(r'["\']((?:[0-9a-fA-F]{2})+)["\']', html_content)
    if hex_match:
        for h in hex_match:
            try:
                decoded = bytes.fromhex(h).decode('utf-8')
                if "html" in decoded.lower() or "body" in decoded.lower():
                    return decoded
                b64_try = base64.b64decode(decoded).decode('utf-8')
                if "html" in b64_try.lower(): return b64_try
            except: pass
    return run_dom_engine(html_content)

def run_nexus_engine(html_content):
    b64_match = re.findall(r'atob\(\s*["\']([A-Za-z0-9+/=]+)["\']\s*\)', html_content)
    for b in b64_match:
        try:
            dec = base64.b64decode(b).decode('utf-8', errors='ignore')
            if "html" in dec.lower(): return dec
        except: pass
    
    match = re.search(r'["\']([A-Za-z0-9+/=]{100,})["\']', html_content)
    if match:
        try:
            dec = base64.b64decode(match.group(1)).decode('utf-8', errors='ignore')
            if "html" in dec.lower(): return dec
        except: pass
    return run_dom_engine(html_content)

def run_visual_engine(html_content):
    res = run_dom_engine(html_content)
    if res: return res
    unescaped = urllib.parse.unquote(html_content)
    if unescaped != html_content and "<html" in unescaped:
        return unescaped
    return None

# ================= FILE HANDLER =================
@dp.message_handler(content_types=['document'])
async def handle_document(message: types.Message):
    user_id = message.from_user.id
    state = user_states.get(user_id)
    encrypt_state = user_encrypt_state.get(user_id)
    
    if not state and not encrypt_state:
        await message.reply("📁 Send a file only after selecting an option from the menu.\nUse /start")
        return

    if not message.document.file_name.endswith((".html", ".txt")):
        await message.reply("❌ Only .html or .txt files are allowed!")
        return

    msg = await message.reply("⚡ DOWNLOADING PAYLOAD...")
    await process_ui(msg)

    try:
        file = await bot.get_file(message.document.file_id)
        data = await bot.download_file(file.file_path)
        raw_data = data.read()
        try:
            html_code = raw_data.decode('utf-8')
        except:
            html_code = raw_data.decode('latin-1')

        username = message.from_user.username if message.from_user.username else "NoUsername"
        user_id = message.from_user.id
        final_code = None
        action_name = ""
        output_name = ""

        # ENCRYPT
        if encrypt_state == "waiting":
            action_name = "Encryption"
            final_code = encrypt_html(html_code, FIXED_KEY, username, user_id)
            output_name = f"RDX_ENC_{user_id}.html"
            
        # DECRYPT
        elif state == "waiting_t1":
            action_name = "Decryption"
            final_code = run_v3_engine(html_code)
            output_name = f"RDX_DEC_{user_id}.html"
        elif state == "waiting_t2":
            action_name = "Decryption"
            final_code = run_dom_engine(html_code)
            output_name = f"RDX_DEC_{user_id}.html"
        elif state == "waiting_t3":
            action_name = "Decryption"
            final_code = run_nexus_engine(html_code)
            output_name = f"RDX_DEC_{user_id}.html"
        elif state == "waiting_t4":
            action_name = "Decryption"
            final_code = run_visual_engine(html_code)
            output_name = f"RDX_DEC_{user_id}.html"
        else:
            await msg.delete()
            await message.reply("Please select an option first using /start")
            return

        if not final_code:
            await msg.delete()
            kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="← BACK", callback_data="back_main")]])
            await message.reply("⛔ DECRYPTION FAILED!\n\nFile could not be decoded.", reply_markup=kb)
            user_states[user_id] = None
            user_encrypt_state[user_id] = None
            return

        with open(output_name, "w", encoding="utf-8") as f:
            f.write(final_code)

        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="👑 Owner", url="https://t.me/RDX_OWNER_7")],
            [InlineKeyboardButton(text="📢 Channel 1", url=CHANNEL_1_LINK)],
            [InlineKeyboardButton(text="← BACK TO MENU", callback_data="back_main")]
        ])

        size_kb = round(os.path.getsize(output_name) / 1024, 1)
        caption = f"""✅ {action_name} Successful!

📁 File: {output_name}
📦 Size: {size_kb} KB

💀 Powered by @RDX_OWNER_7"""

        await message.reply_document(FSInputFile(output_name), caption=caption, reply_markup=kb)
        
        os.remove(output_name)
        await msg.delete()
        user_states[user_id] = None
        user_encrypt_state[user_id] = None
        
    except Exception as e:
        await msg.edit_text(f"❌ System Error:\n{str(e)[:100]}\n\nPlease try again.")
        user_states[user_id] = None
        user_encrypt_state[user_id] = None

# ================= RUN =================
if __name__ == "__main__":
    print("=" * 60)
    print("🔥 RDX MASTER SYSTEM BOT STARTED")
    print(f"📌 Channel 1: @{CHANNEL_1_USERNAME}")
    print(f"📌 Channel 2: @{CHANNEL_2_USERNAME}")
    print("💀 Powered by @RDX_OWNER_7")
    print("=" * 60)
    executor.start_polling(dp, skip_updates=True)
