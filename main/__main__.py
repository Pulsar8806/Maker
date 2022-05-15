from main import app
import pyrogram
from pyrogram import filters, idle
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from main.logo import generate_logo

START = """
**🔮 Merhaba, Harika Logolar Oluşturmak İçin Beni Kullanabilirsiniz...**

➤ Tıklayınız /help Veya Beni Nasıl Kullanacağınızı Bilmek İçin Aşağıdaki Düğmeye basın
"""

HELP = """
**🖼 Beni Kullanmak için?**

**Logo Yapmak İçin -** `/logo İsim yazınız`
**Kare Logo Yapmak İçin - ** `/logom İsim yazınız`
**♻️ Örnek:** 
`/logo Mahoaga`
`/logom Kral Geri Döndü`
"""

# Komut
@app.on_message(filters.command("start"))
async def start(bot, message):
  await message.reply_photo("https://i.ibb.co/khRz42f/Turkish-Voice.jpg",caption=START,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Help", callback_data="help_menu"), InlineKeyboardButton(text="Repo", url="https://github.com/TechShreyash/TechZ-Logo-Maker-Bot")]]))

@app.on_message(filters.command("help"))
async def help(bot, message):
  await message.reply_photo("https://i.ibb.co/khRz42f/Turkish-Voice.jpg",caption=HELP,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Geri", callback_data="start_menu")]]))

@app.on_message(filters.command("logo") & filters.incoming & filters.text & ~filters.forwarded & (
  filters.group | filters.private))
async def logo(bot, message):
  try:
    text = message.text.replace("logo","").replace("/","").replace("@SohbetDestek","").strip().upper()
    
    if text == "":
      return await message.reply_text(HELP)

    x = await message.reply_text("`🔍 Sizin İçin Logo Yapıyorum...`")  
    logo = await generate_logo(text)

    if "telegra.ph" not in logo:
      return await x.edit("`❌ Bir Şeyler Ters Gitti...`\n\nBu Hatayı Şurada Bildir: @Botdestekgrubu")
      
    if "error" in logo:
      return await x.edit(f"`❌ Bir Şeyler Ters Gitti...`\n\nBu Hatayı Şurada Bildir: @Botdestekgrubu\n\n`{logo}`")
      
    await x.edit("`🔄 Bitti Oluşturuldu... Şimdi Size Gönderiyoruz`")

    logo_id = logo.replace("https://telegra.ph//file/","").replace(".jpg","").strip()
    await message.reply_photo(logo,caption="**🖼 Logo Tasarım @SohbetDestek**",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Dosya Olarak Yükle 📁", callback_data=f"flogo {logo_id}")]]))
    await x.delete()
  except FloodWait:
    pass
  except Exception as e:
    try:
      await x.delete()
    except:
      pass
    return await message.reply_text("`❌ Bir Şeyler Ters Gitti...`\n\nBu Hatayı Şurada Bildir: @Botdestekgrubu")

# Square Logo
@app.on_message(filters.command("logom") & filters.incoming & filters.text & ~filters.forwarded & (
  filters.group | filters.private))
async def logo(bot, message):
  try:
    text = message.text.replace("logom","").replace("/","").replace("@SohbetDestek","").strip().upper()
      
    if text == "":
      return await message.reply_text(HELP)
  
    x = await message.reply_text("`🔍 Sizin İçin Logo Yapılıyor...`")  
    logo = await generate_logo(text,True)
  
    if "telegra.ph" not in logo:
      return await x.edit("`❌ Bir Şeyler Ters Gitti...`\n\nBu Hatayı Şurada Bildir: @Botdestekgrubu")
        
    if "error" in logo:
      return await x.edit(f"`❌ Bir Şeyler Ters Gitti...`\n\nBu Hatayı Şurada Bildir: @Botdestekgrubu\n\n`{logo}`")
      
    await x.edit("`🔄 Bitti Üretildi... Şimdi Size Gönderiyorum`")
    
    logo_id = logo.replace("https://telegra.ph//file/","").replace(".jpg","").strip()
    
    await message.reply_photo(logo,caption="**🖼 Logo Tasarım Kanalı @SohbetDestek**",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Dosya Olarak Yükle 📁", callback_data=f"flogo {logo_id}")]]))
    await x.delete()
  except FloodWait:
    pass
  except Exception as e:
    try:
      await x.delete()
    except:
      pass
    return await message.reply_text("`❌ Bir Şeyler Ters Gitti...`\n\nBu Hatayı Şurada Bildir: @Botdestekgrubu")

# Callbacks
@app.on_callback_query(filters.regex("start_menu"))
async def start_menu(_,query):
  await query.answer()
  await query.message.edit(START,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Help", callback_data="help_menu"),InlineKeyboardButton(text="💬 İletişim", url="https://t.me/Botdestekgrubu")]]))

@app.on_callback_query(filters.regex("help_menu"))
async def help_menu(_,query):
  await query.answer()
  await query.message.edit(HELP,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Back", callback_data="start_menu")]]))

@app.on_callback_query(filters.regex("flogo"))
async def logo_doc(_,query):
  await query.answer()
  try:
    x = await query.message.reply_text("`🔄 Logoyu Size Dosya Olarak Gönderiyorum`")
    await query.message.edit_reply_markup(reply_markup=None)
    link = "https://telegra.ph//file/" + query.data.replace("flogo","").strip() + ".jpg"
    await query.message.reply_document(link,caption="**🖼 Logo Tasarım @Botdestekgrubu**")
  except FloodWait:
    pass
  except Exception as e:
    try:
      return await x.edit(f"`❌ Bir Şeyler Ters Gitti...`\n\nBu Hatayı Şurada Bildir: @Botdestekgrubu \n\n`{str(e)}`")
    except:
      return
    
  return await x.delete()
  

if __name__ == "__main__":
  print("==================================")
  print("[INFO]: LOGO YAPIMCISI BOT, BOT'U BAŞARIYLA BAŞLATTI")
  print("==========JOIN @BOTDESTEKGRUBU=========")

  idle()
  print("[INFO]: LOGO YAPIMCI BOTU DURDURULDU")
