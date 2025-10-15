import telebot
from functools import partial
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from manage import UserManager, UserActivityManager
import threading
from random import randint
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
from datetime import datetime
import logging

RULES_TEXT = """Made By Niproot
"""


ACTIVATION_TEXT = """Made By Niproot"""



#Settin_Up_Bot_______________________________________________________________________________________

photo_path = "images.png"  
caption_text = """Made By Niproot"""
ADMIN_IDS = [] 
TOKEN = ''
with open("products.json", "r", encoding="utf-8") as f:
    products_data = json.load(f)
bot = telebot.TeleBot(TOKEN)
USERS_FILE = "users.json"
categories = list(products_data.keys())
user_cart = {} 
user_last_msg = {}  

user_manager = UserManager("users.json")
users_lock = threading.Lock()
channels_lock = threading.Lock()
CHANNELS = []
activity_manager = UserActivityManager()
with open("products.json", "r", encoding="utf-8") as f:
    products_data = json.load(f)

categories = list(products_data.keys())
user_cart = {}  
user_last_msg = {}

with open("users.json", "r", encoding="utf-8") as f:
    USERS = json.load(f) 

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def send_email(receiver_email: str, code: str) -> bool:
   
    smtp_server = ''
    port = ''
    sender_email = ''
    password = ''

 
    subject = "Login Verification Code"
    text_body = f"""
    سلام 🌸

    خوش آمدید به !
    کد ورود شما: {code}

    لطفاً این کد را در کمتر از ۵ دقیقه استفاده کنید.
    """

    html_body = f"""
    <html>
    <body style="font-family:Tahoma, sans-serif; background-color:#f5f5f5; padding:20px;">
        <div style="max-width:600px; margin:auto; background:#ffffff; border-radius:12px; box-shadow:0 4px 12px rgba(0,0,0,0.1); padding:30px;">
            <h2 style="color:#3b5998; text-align:center;"> Login</h2>
            <p style="font-size:15px; color:#333;">سلام! 🌸<br><br>
            به  خوش اومدی.<br><br>
            <strong style="font-size:18px; color:#222;">کد ورود شما:</strong><br>
            <div style="background:#3b5998; color:#fff; display:inline-block; padding:10px 20px; border-radius:8px; margin-top:10px; font-size:22px; letter-spacing:2px;">
                {code}
            </div><br><br>
            <small style="color:#888;">اعتبار کد: ۵ دقیقه</small>
            </p>
        </div>
    </body>
    </html>
    """

 
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f" <{sender_email}>"
    msg["To"] = receiver_email
    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

 
    try:
        with smtplib.SMTP_SSL(smtp_server, port) as server:
            server.login(sender_email, password)
            server.send_message(msg)
        logging.info(f"✅ ایمیل با موفقیت به {receiver_email} ارسال شد.")
        return True

    except smtplib.SMTPAuthenticationError:
        logging.error("❌ خطای احراز هویت SMTP: نام کاربری یا رمز اشتباه است.")
    except smtplib.SMTPConnectError:
        logging.error("❌ خطای اتصال به سرور SMTP.")
    except Exception as e:
        logging.error(f"❌ خطای غیرمنتظره در ارسال ایمیل: {e}")

    return False
#Users_Panels_____________________________________________________________________________________________

def check_is_loggined(uid):
    try:
        pass
    except:
        pass

def is_member(user_id):
    try:
        for ch in CHANNELS:
            try:
                member = bot.get_chat_member(ch["id"], user_id)
                if member.status not in ["member", "creator", "administrator"]:
                    return False
            except Exception as ex:
                print(f"error {ch['id']}: {ex}")
                
                continue
        return True
    except Exception as ex:
        print(f"❌ error in is_member: {ex}")
        return False

def create_keyboard(buttons_list, row_width=2):
    try:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        for i in range(0, len(buttons_list), row_width):
            row_buttons = buttons_list[i:i+row_width]
            markup.add(*[KeyboardButton(btn) for btn in row_buttons])
        return markup
    except Exception as ex:
        print(f"❌ error{ex}")
        return None

def main_markup():
    return create_keyboard(["help", "محصولات","پشتیبانی", "ارسال تیکت","قوانین"], row_width=2)






#Admins_Panels__________________________________________________

DISCOUNT_FILE = "discount_codes.json"


def load_discount_codes():
    try:
        with open(DISCOUNT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_discount_codes(codes):
    with open(DISCOUNT_FILE, "w", encoding="utf-8") as f:
        json.dump(codes, f, ensure_ascii=False, indent=2)

discount_codes = load_discount_codes()


def admin_discount_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("💳 ساخت کد جدید"))
    markup.add(KeyboardButton("📄 لیست کدهای موجود"))
    markup.add(KeyboardButton("❌ حذف کد"))
    markup.add(KeyboardButton("🔙 بازگشت"))
    return markup


def start_create_discount(message):
    bot.send_message(message.chat.id, "لطفاً متن کد تخفیف را وارد کنید:")
    bot.register_next_step_handler(message, choose_discount_percent)

def choose_discount_percent(message):
    code = message.text.strip().upper()
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    
    
    percents = list(range(10, 101, 10))
    buttons = [KeyboardButton(f"{p}%") for p in percents]
    markup.add(*buttons)
    
    msg = bot.send_message(message.chat.id, f"✅ کد '{code}' دریافت شد. حالا درصد تخفیف را انتخاب کنید:", reply_markup=markup)
    bot.register_next_step_handler(msg, save_discount, code)

def save_discount(message, code):
    try:
        percent_text = message.text.strip().replace("%", "")
        percent = int(percent_text)
        discount_codes[code] = percent / 100
        save_discount_codes(discount_codes)
        bot.send_message(
            message.chat.id,
            f"✅ کد {code} با {percent}% تخفیف ساخته و ذخیره شد.\n /start را بزنید",
            reply_markup=ReplyKeyboardRemove()
        )
    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"❌ خطا در ذخیره کد: {e}",
            reply_markup=ReplyKeyboardRemove()
        )


def send_discount_to_user(message):
        uid = int(message.text.strip()) 
        if not discount_codes:
            bot.send_message(message.chat.id, "❌ هیچ کد تخفیفی وجود ندارد.", reply_markup=ReplyKeyboardRemove())
            return
        

        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        buttons = [KeyboardButton(code) for code in discount_codes.keys()]
        markup.add(*buttons)
        
        msg = bot.send_message(message.chat.id, "✅ آیدی دریافت شد.\n\nیکی از کدهای تخفیف را برای ارسال انتخاب کنید:", reply_markup=markup)
        bot.register_next_step_handler(msg, confirm_send_discount, uid)
def confirm_send_discount(message, uid):
    code = message.text.strip().upper()
    
    if code not in discount_codes:
        bot.send_message(message.chat.id, "❌ چنین کدی وجود ندارد.", reply_markup=ReplyKeyboardRemove())
        return

    try:
        percent = int(discount_codes[code] * 100)
        bot.send_message(
            uid,
            f"🎁 شما یک کد تخفیف جدید دریافت کردید!\n\nکد: `{code}`\nدرصد تخفیف: {percent}%",
            parse_mode="Markdown"
        )
        bot.send_message(
            message.chat.id,
            f"✅ کد {code} با موفقیت برای کاربر {uid} ارسال شد. \n /start را بزنید",
            reply_markup=ReplyKeyboardRemove()
        )
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ خطا در ارسال پیام: {e}", reply_markup=ReplyKeyboardRemove())

    except ValueError:
        bot.send_message(message.chat.id, "❌ آیدی وارد شده معتبر نیست (باید عددی باشد).", reply_markup=ReplyKeyboardRemove())
 
def show_discount_list(message):
    if not discount_codes:
        bot.send_message(message.chat.id, "هیچ کد تخفیفی ساخته نشده است.")
        return
    text = "📄 لیست کدهای موجود:\n\n"
    for code, percent in discount_codes.items():
        text += f"{code} → {int(percent*100)}%\n"
    bot.send_message(message.chat.id, text)


def delete_discount_start(message):
    if not discount_codes:
        bot.send_message(message.chat.id, "هیچ کدی برای حذف وجود ندارد.")
        return
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = [KeyboardButton(code) for code in discount_codes.keys()]
    markup.add(*buttons)
    msg = bot.send_message(message.chat.id, "کدام کد را می‌خواهید حذف کنید؟", reply_markup=markup)
    bot.register_next_step_handler(msg, delete_discount_confirm)

def delete_discount_confirm(message):
    code = message.text.strip().upper()
    if code in discount_codes:
        del discount_codes[code]
        save_discount_codes(discount_codes)
        bot.send_message(
            message.chat.id,
            f"✅ کد {code} حذف شد.\n /start رابزنید",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        bot.send_message(
            message.chat.id,
            "❌ کد پیدا نشد.",
            reply_markup=ReplyKeyboardRemove()
        )


def admin_panel_handler(message):
    text = message.text
    if text == "💳 ساخت کد جدید":
        start_create_discount(message)
    elif text == "📄 لیست کدهای موجود":
        show_discount_list(message)
    elif text == "❌ حذف کد":
        delete_discount_start(message)
    elif text == "🔙 بازگشت":
        bot.send_message(message.chat.id, "به منوی اصلی برگشتید.", reply_markup=main_markup())

def admin_panel_keyboard():
    try:
        buttons = [
            "آمار کاربران", 
            "ارسال پیام همگانی",
            "مدیریت کاربران",
            "ساخت کدتخفیف",
            "مدیریت محصولات",
            "ارسال تیکت"
        ]
        return create_keyboard(buttons, row_width=2)
    except Exception as ex:
        print(f"❌ خطا در admin_panel_keyboard: {ex}")
        return ReplyKeyboardMarkup()

def user_management_keyboard():
    try:
        buttons = ["دادن کد تخفیف","لیست فعالیت", "بازگشت"]
        return create_keyboard(buttons, row_width=2)
    except Exception as ex:
        print(f"❌ خطا در user_management_keyboard: {ex}")
        return ReplyKeyboardMarkup()
def send_ticket(user_id, ticket_text):
    try:
        

        for admin in ADMIN_IDS:
            try:
                bot.send_message(
                    admin,
                    f"🆕 تیکت جدید\nتاریخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nUID: {user_id}\nمتن تیکت: {ticket_text}",
                    )
            except:
                pass

        bot.send_message(user_id, "✅ تیکت شما با موفقیت ارسال شد.")
    except Exception as ex:
        print(f"❌ خطا در send_ticket: {ex}")
        bot.send_message(user_id, "❌ ارسال تیکت با مشکل مواجه شد.")


        
def broadcast_message(message):
    try:
        if message.text == "انصراف":
            bot.send_message(message.chat.id, "ارسال همگانی لغو شد.", reply_markup=admin_panel_keyboard())
            return

        text = message.text
        success_count = 0
        fail_count = 0
        
        with users_lock:
            for user_id, info in USERS.items():
                try:
                    bot.send_message(int(user_id), f"📢 پیام همگانی:\n\n{text}")
                    success_count += 1
                except Exception as e:
                    print(f"❌ خطا در ارسال به کاربر {user_id}: {e}")
                    fail_count += 1

        
        bot.send_message(
            message.chat.id, 
            f"✅ پیام همگانی ارسال شد.\n\n✅ موفق: {success_count}\n❌ ناموفق: {fail_count} \n /start",
            reply_markup=admin_panel_keyboard()
        )
    except Exception as ex:
        print(f"❌ خطا در broadcast_message: {ex}")
        bot.send_message(message.chat.id, "❌ خطا در ارسال پیام همگانی. \n /start")
def edit_products():
    try:
        buttons = ["حذف یک لیست از محصولات","افزودن محصول", "افزودن لیست جدید محصولات", "بازگشت"]
        return create_keyboard(buttons, row_width=2)
    except Exception as ex:
        pass
PRODUCTS_FILE = "products.json"


def edit_products():
    try:
        buttons = ["حذف یک دسته‌بندی","افزودن محصول", "افزودن دسته‌بندی جدید", "بازگشت"]
        return create_keyboard(buttons, row_width=2)
    except Exception as ex:
        print("Error in edit_products:", ex)
        return []

def remove_category(category_name):
    try:
        data = load_products()
        if category_name in data:
            del data[category_name]
            save_products(data)
            return f"دسته‌بندی '{category_name}' حذف شد. \n /start"
        else:
            return "این دسته‌بندی وجود ندارد. \n /start"
    except Exception as ex:
        return f"خطا در حذف دسته‌بندی: {ex} \n /start"

def add_products(category_name, name, price, url):
    try:
        data = load_products()
        if category_name not in data:
            return "این دسته‌بندی وجود ندارد. ابتدا دسته‌بندی ایجاد کنید. \n /start رابزنید"
        
        products = data[category_name]
        product_id = f"product{len(products)+1}"
        products[product_id] = {
            "name": name,
            "Price": price,
            "Image Addres": "",
            "Url": url,
            "Time": str(datetime.now())
        }
        save_products(data)
        return f"محصول '{name}' به دسته‌بندی '{category_name}' اضافه شد.\n /start رابزنید"
    except Exception as ex:
        return f"خطا در اضافه کردن محصول: {ex} \n /start"

def add_category(category_name):
    try:
        data = load_products()
        if category_name in data:
            return "این دسته‌بندی از قبل وجود دارد.\n /start"
        data[category_name] = {}
        save_products(data)
        return f"دسته‌بندی '{category_name}' ایجاد شد. \n /start"
    except Exception as ex:
        return f"خطا در اضافه کردن دسته‌بندی: {ex} \n /start"

def load_products():
    try:
        with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_products(data):
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    
def add_category_step(message):
    category_name = message.text.strip()
    result = add_category(category_name)
    bot.send_message(message.chat.id, result, reply_markup=edit_products())

def remove_category_step(message):
    category_name = message.text.strip()
    result = remove_category(category_name)
    bot.send_message(message.chat.id, result, reply_markup=edit_products())


def add_product_category_step(message):
    category_name = message.text.strip()
    data = load_products()
    if category_name not in data:
        bot.send_message(message.chat.id, "این دسته‌بندی وجود ندارد. ابتدا آن را بسازید. \n /start رابزنید", reply_markup=edit_products())
        return
    msg = bot.send_message(message.chat.id, "نام محصول را وارد کنید:")
    bot.register_next_step_handler(msg, add_product_name_step, category_name)

def add_product_name_step(message, category_name):
    name = message.text.strip()
    msg = bot.send_message(message.chat.id, "قیمت محصول را وارد کنید:")
    bot.register_next_step_handler(msg, add_product_price_step, category_name, name)

def add_product_price_step(message, category_name, name):
    price = message.text.strip()
    msg = bot.send_message(message.chat.id, "لینک محصول را وارد کنید:")
    bot.register_next_step_handler(msg, add_product_url_step, category_name, name, price)


def add_product_url_step(message, category_name, name, price):
    url = message.text.strip()
    
    result = add_products(category_name, name, price, url)
    bot.send_message(message.chat.id, result, reply_markup=edit_products())


#------------------------ ADMIN HANDLERS ------------------------

@bot.message_handler(func=lambda message: message.chat.id in ADMIN_IDS)
def admin_handler(message):
    try:
        text = message.text

        
        if text == "آمار کاربران":
            with users_lock:
                user_count = len(USERS)
            with channels_lock:
                channel_count = len(CHANNELS)
            bot.send_message(
                message.chat.id,
                f"📊 آمار ربات:\n\n👥 کاربران: {user_count}",
                reply_markup=admin_panel_keyboard()
            )
            
        elif text == "ارسال تیکت":
           msg = bot.send_message(message.chat.id, "📝 لطفاً UID عددی کاربر مورد نظر را وارد کنید:")
           bot.register_next_step_handler(msg, handle_ticket_from_admin)
       
        elif text == "ارسال پیام همگانی":
            msg = bot.send_message(message.chat.id, "لطفاً متن پیام همگانی را ارسال کنید (یا 'انصراف' برای لغو):")
            bot.register_next_step_handler(msg, broadcast_message)

        
        elif text == "مدیریت کاربران":
            bot.send_message(message.chat.id, "گزینه مورد نظر را انتخاب کنید:", reply_markup=user_management_keyboard())

        
        elif text == "مدیریت محصولات":
            bot.send_message(message.chat.id, "انتخاب کنید:", reply_markup=edit_products())
            
        elif text == "افزودن دسته‌بندی جدید":
            msg = bot.send_message(message.chat.id, "نام دسته‌بندی جدید را وارد کنید:")
            bot.register_next_step_handler(msg, add_category_step)
            
        elif text == "لیست فعالیت":
            ActivityList(message)
    
        elif text == "افزودن محصول":
            msg = bot.send_message(message.chat.id, "نام دسته‌بندی را وارد کنید که محصول به آن اضافه شود:")
            bot.register_next_step_handler(msg, add_product_category_step)

    
        elif text == "حذف یک دسته‌بندی":
            msg = bot.send_message(message.chat.id, "نام دسته‌بندی که می‌خواهید حذف کنید را وارد کنید:")
            bot.register_next_step_handler(msg, remove_category_step)
        
        elif text == "دادن کد تخفیف":
            msg = bot.send_message(message.chat.id, "لطفاً آیدی عددی کاربر را وارد کنید:")
            bot.register_next_step_handler(msg, send_discount_to_user)
        elif text == "ساخت کدتخفیف":
            bot.send_message(message.chat.id, "انتخاب کنید:", reply_markup=admin_discount_menu())

        elif text == "💳 ساخت کد جدید":
            start_create_discount(message)

        elif text == "📄 لیست کدهای موجود":
            show_discount_list(message)
            
    
        elif text == "❌ حذف کد":
            delete_discount_start(message)
            
        elif text == "بازگشت":
            bot.send_message(message.chat.id, "بازگشت به پنل اصلی:", reply_markup=admin_panel_keyboard())

        elif text == "🔙 بازگشت":
            bot.send_message(message.chat.id, "بازگشت به پنل اصلی:", reply_markup=admin_panel_keyboard())

       
        else:
            bot.send_message(message.chat.id, "لطفاً از گزینه‌های منو استفاده کنید.", reply_markup=admin_panel_keyboard())

    except Exception as ex:
        print(f"❌ خطا در admin_handler: {ex}")
        bot.send_message(message.chat.id, "❌ خطا در پردازش درخواست.")




def ActivityList(message):
    try:
        activity_list = []  

        with open("users.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        for user_id, info in data.items():
            last_activity = info.get("Last_activity", "ثبت نشده")
            join_time = info.get("join Time", "ثبت نشده")
            phone = info.get("phone", "نامشخص")

            user_info = (
                f"👤 UID: {user_id}\n"
                f"📱 Phone: {phone}\n"
                f"⏰ Last Activity: {last_activity}\n"
                f"🗓️ Join Time: {join_time}\n"
                "-------------------------"
            )

            activity_list.append(user_info)

        
        full_text = "\n\n".join(activity_list)

        
        bot.send_message(message.chat.id, full_text)

        return activity_list

    except Exception as ex:
        print(f"❌ خطا در ActivityList: {ex}")
        bot.send_message(message.chat.id, f"❌ خطا در نمایش لیست کاربران: {ex}")
        return []


#------------------------ USER HANDLERS ------------------------
def generate_code():
    return f"{randint(0, 999999):06}"  
def is_valid_email(email: str) -> bool:
   
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None


@bot.message_handler(commands=["login"])
def login(message):
    try:
        user_id = message.from_user.id
        username = message.from_user.username or "بدون نام"

       
    
       
        
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn_phone = KeyboardButton("📞 ارسال شماره", request_contact=True)
        markup.add(btn_phone)
        bot.send_message(message.chat.id, "سلام! برای ادامه روی دکمه زیر بزن:", reply_markup=markup)
    except Exception as e:
        bot.send_message(message.chat.id, f"خطا: {e}")
@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    try:
        uid = message.chat.id
        phone = message.contact.phone_number  
        user_id = message.from_user.id
        username = message.from_user.username or "بدون نام"
       
        if not phone.startswith("+"):
            phone = "+" + phone
            
        activity_manager.set_phone_number(uid, phone)
        msg = bot.send_message(user_id, "لطفاً ایمیل خود را وارد کنید:")
        bot.register_next_step_handler(msg, handle_email, username)

    except Exception as ex:
        print(f"❌ خطا در handle_contact: {ex}")
        bot.send_message(message.chat.id, "⚠️ مشکلی در پردازش شماره پیش اومد، دوباره تلاش کنید.")
def handle_email(message, username):
    user_id = message.from_user.id
    email = message.text.strip()

    if not is_valid_email(email):
        msg = bot.send_message(user_id, "ایمیل نامعتبر است. لطفاً یک ایمیل معتبر وارد کنید:")
        bot.register_next_step_handler(msg, handle_email, username)
        return

    code = generate_code()
    user_manager.save_code(user_id, code)  
   
    send_email(email, code)

  
    activity_manager.add_user(user_id)
    activity_manager.set_email(user_id, email)

    msg = bot.send_message(user_id, "کد ۶ رقمی به ایمیل شما ارسال شد. لطفاً کد را وارد کنید:")
    bot.register_next_step_handler(msg, verify_code, username)

def verify_code(message, username):
    user_id = message.from_user.id
    entered = message.text.strip()

    
    data = user_manager.get_user_data(user_id)
    if not data or not data.get("code"):
        bot.send_message(user_id, "کدی برای شما تولید نشده یا منقضی شده. لطفاً دوباره /login را بزنید.")
        return

    saved_code = str(data["code"])
    if entered != saved_code:
     
        msg = bot.send_message(user_id, "کد اشتباه است. دوباره وارد کنید یا /login را از ابتدا بزنید.")
        bot.register_next_step_handler(msg, verify_code, username)
        return

    user_manager.save_code(user_id, "")  
    bot.send_message(user_id, RULES_TEXT)
    msg = bot.send_message(user_id, "ورود موفق آمیز بود!", reply_markup=main_markup())
    activity_manager.set_is_loggin(user_id, True)


category_translations = {
    "": "",
    "": "",
    "": "",
    "": "",
    "": "",
    "": "",
    "": "",
    "": "",
    "": "",
    "": ""
}


def shopping_cart(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for cat_eng in categories:
        cat_fa = category_translations.get(cat_eng, cat_eng) 
        markup.add(telebot.types.KeyboardButton(f"🛍 {cat_fa}"))
    markup.add(telebot.types.KeyboardButton("🧾 تسویه حساب"))
    markup.add(telebot.types.KeyboardButton("🔙 بازگشت به منو اصلی"))
    bot.send_message(
        message.chat.id,
        "🌟 *به فروشگاه ما خوش آمدید!*\n\n"
        "📦 لطفاً دسته‌بندی مورد نظر خود را انتخاب کنید 👇",
        parse_mode="Markdown",
        reply_markup=markup,
    )


@bot.message_handler(func=lambda message: message.text.startswith("🛍 "))
def select_category(message):
    cat_fa = message.text.replace("🛍 ", "")
    
    cat_eng = next((k for k, v in category_translations.items() if v == cat_fa), None)
    if not cat_eng:
        bot.send_message(message.chat.id, "❌ دسته‌بندی نامعتبر.")
        return
    show_products_list(message.chat.id, message.from_user.id, cat_eng, cat_fa)

def show_products_list(chat_id, user_id, category_eng, category_fa):
    products = products_data.get(category_eng, {})
    if not products:
        bot.send_message(chat_id, "❌ هیچ محصولی در این دسته یافت نشد.")
        return

    text = f"📂 *دسته: {category_fa}*\n\n"
    text += "📦 لیست محصولات:\n\n"
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)

    for key, prod in products.items():
        button_text = f"{prod['name']} - {prod['Price']} تومان"
        markup.add(telebot.types.InlineKeyboardButton(button_text, callback_data=f"detail|{category_eng}|{key}"))

    markup.add(
        telebot.types.InlineKeyboardButton("🧾 تسویه حساب", callback_data=f"checkout|{category_eng}"),
        telebot.types.InlineKeyboardButton("🔙 بازگشت به دسته‌ها", callback_data="back_to_categories")
    )


    last_msg_id = user_last_msg.get(user_id)
    if last_msg_id:
        try:
            bot.delete_message(chat_id, last_msg_id)
        except:
            pass

    msg = bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=markup)
    user_last_msg[user_id] = msg.message_id

def show_product_detail(chat_id, user_id, category_eng, key):
    prod = products_data.get(category_eng, {}).get(key)
    if not prod:
        bot.send_message(chat_id, "❌ محصول یافت نشد.")
        return

    in_cart = any(item["name"] == prod["name"] for item in user_cart.get(user_id, []))

    text = (
        f"📦 *{prod['name']}*\n\n"
        f"💰 قیمت: `{prod['Price']}` تومان\n"
        f"🔗 [مشاهده جزئیات بیشتر]({prod['Url']})\n\n"
        f"🛍 وضعیت: {'در سبد خرید' if in_cart else 'قابل افزودن'}\n\n"
        f"تصویر: {prod.get('Image Addres', 'بدون تصویر')}"
    )

    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    if in_cart:
        markup.add(telebot.types.InlineKeyboardButton("❌ حذف از سبد خرید", callback_data=f"remove|{category_eng}|{key}"))
    else:
        markup.add(telebot.types.InlineKeyboardButton("🛒 افزودن به سبد خرید", callback_data=f"add|{category_eng}|{key}"))

    markup.add(
        telebot.types.InlineKeyboardButton("🔙 بازگشت به لیست محصولات", callback_data=f"back_to_list|{category_eng}"),
        telebot.types.InlineKeyboardButton("🧾 تسویه حساب", callback_data=f"checkout|{category_eng}")
    )
    markup.add(telebot.types.InlineKeyboardButton("🔙 بازگشت به منو اصلی", callback_data="back_to_categories"))


    last_msg_id = user_last_msg.get(user_id)
    if last_msg_id:
        try:
            bot.delete_message(chat_id, last_msg_id)
        except:
            pass

    msg = bot.send_message(chat_id, text, parse_mode="Markdown", disable_web_page_preview=False, reply_markup=markup)
    user_last_msg[user_id] = msg.message_id

@bot.callback_query_handler(func=lambda call: not call.data.startswith(("approve","reject")))
def handle_callbacks(call):
    user_id = call.from_user.id
    data = call.data
    chat_id = call.message.chat.id

    try:
        parts = data.split("|")
        action = parts[0]

        if action == "back_to_categories":
            bot.send_message(chat_id, "🏠 بازگشت به منوی فروشگاه.", reply_markup=ReplyKeyboardRemove())
            shopping_cart(call.message)
            return

        if action == "back_to_list":
            category_eng = parts[1]
            cat_fa = category_translations.get(category_eng, category_eng)
            show_products_list(chat_id, user_id, category_eng, cat_fa)
            bot.answer_callback_query(call.id)
            return

        if action == "detail":
            category_eng, key = parts[1], parts[2]
            show_product_detail(chat_id, user_id, category_eng, key)
            bot.answer_callback_query(call.id)
            return

        if action == "add":
            category_eng, key = parts[1], parts[2]
            prod = products_data.get(category_eng, {}).get(key)
            if prod:
                user_cart.setdefault(user_id, [])
                if not any(item["name"] == prod["name"] for item in user_cart[user_id]):
                    user_cart[user_id].append({
                        "name": prod["name"],
                        "Price": prod["Price"],
                        "Url": prod["Url"]
                    })
                bot.answer_callback_query(call.id, "✅ محصول به سبد خرید اضافه شد")
                
                show_product_detail(chat_id, user_id, category_eng, key)

        elif action == "remove":
            category_eng, key = parts[1], parts[2]
            prod = products_data.get(category_eng, {}).get(key)
            if prod and user_id in user_cart:
                user_cart[user_id] = [item for item in user_cart[user_id] if item["name"] != prod["name"]]
                bot.answer_callback_query(call.id, "❌ محصول از سبد خرید حذف شد")
                
                show_product_detail(chat_id, user_id, category_eng, key)

        elif action == "checkout":
            account_settlement(user_id, chat_id)
            bot.answer_callback_query(call.id)

    except Exception as e:
        bot.answer_callback_query(call.id, f"⚠️ خطا: {e}")


@bot.message_handler(func=lambda message: message.text == "🧾 تصفیه حساب")
def go_to_checkout(message):
    user_id = message.from_user.id
    account_settlement(user_id, message.chat.id)


def account_settlement(user_id, chat_id):
    cart = user_cart.get(user_id, [])
    if not cart:
        bot.send_message(chat_id, "سبد خرید شما خالی است.")
        return

    def clean_price(price_str):
        try:
            clean = price_str.replace(",", "").replace(" ", "").replace("تومان", "").strip()
            return float(clean)
        except ValueError:
            return 0.0

    text = "🛒 *سبد خرید شما:*\n\n"
    total = 0
    for item in cart:
        text += f"{item['name']} - {item['Price']}\n"
        total += clean_price(item['Price'])

    bot.send_message(chat_id, text)
    bot.send_message(chat_id, "اگر کد تخفیف دارید، وارد کنید (یا /skip برای ادامه بدون تخفیف):")
    bot.register_next_step_handler_by_chat_id(chat_id, apply_discount, total)


def apply_discount(message, total):
    user_id = message.from_user.id
    code = message.text.strip()
    file_path = "discount_codes.json"
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(
            telebot.types.InlineKeyboardButton("✅ تایید", callback_data=f"approve|{user_id}"),
            telebot.types.InlineKeyboardButton("❌ رد", callback_data=f"reject|{user_id}")
        )
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            discounts = json.load(f)
    except Exception as ex:
        bot.send_message(message.chat.id, f"❌ خطا در خواندن کدهای تخفیف: {ex}")
        return

    total_after_discount = total 

    if code == "/skip":
        
        bot.send_message(message.chat.id, f"💰 جمع کل: {total_after_discount} تومان")
        bot.send_photo(user_id, photo=open(photo_path, "rb"), caption=caption_text)
        bot.register_next_step_handler_by_chat_id(message.chat.id, handle_screenshot)
        return

    if code in discounts:
        percent = discounts[code]
        total_after_discount = total * (1 - percent)
        bot.send_message(message.chat.id, f"✅ کد تخفیف معتبر بود. {percent*100}% از مبلغ کم شد.\n💰 جمع کل پس از تخفیف: {int(total_after_discount)} تومان")
        bot.send_message(message.chat.id, f"منتظر تایید شدن سفارشتون توسط ادمین هابمونید")
        
        if percent == 1.0:
            for admin in ADMIN_IDS:
                try:
                    bot.send_message(
                        admin,
                        f"⚠️ خرید با کد ۱۰۰٪ تخفیفی\nUID: {user_id}\nزمان: {datetime.now()}\nجمع کل: {total}\nمحصول: {user_cart.get(user_id, [])}\nلطفاً سریع با کاربر ارتباط برقرار کنید.",
                        reply_markup=markup
                        )
                except:
                    pass

        
        del discounts[code]
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(discounts, f, ensure_ascii=False, indent=4)

    else:
        bot.send_message(message.chat.id, "❌ کد تخفیف معتبر نیست. ادامه بدون تخفیف.")
        bot.send_message(message.chat.id, f"💰 جمع کل: {int(total_after_discount)} تومان")

    
    bot.send_photo(user_id, photo=open(photo_path, "rb"), caption=caption_text)
    bot.register_next_step_handler_by_chat_id(message.chat.id, handle_screenshot)


def handle_screenshot(message):
    user_id = message.from_user.id

    if message.content_type != "photo":
        bot.send_message(message.chat.id, "❌ لطفاً فقط اسکرین‌شات ارسال کنید.")
        return

    
    user_info = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "cart": user_cart.get(user_id, []),
        "username": getattr(message.from_user, "username", ""),
        "first_name": getattr(message.from_user, "first_name", ""),
        "last_name": getattr(message.from_user, "last_name", ""),
        "chat_id": message.chat.id,
        "description": getattr(message, "caption", "")  
    }

   
    for admin in ADMIN_IDS:
        try:
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(
                telebot.types.InlineKeyboardButton("✅ تایید", callback_data=f"approve|{user_id}"),
                telebot.types.InlineKeyboardButton("❌ رد", callback_data=f"reject|{user_id}")
            )

            bot.send_photo(
                admin,
                message.photo[-1].file_id,
                caption=f"🧾 واریزی کاربر:\n\n{json.dumps(user_info, ensure_ascii=False, indent=2)}",
                reply_markup=markup
            )
        except:
            pass

    bot.send_message(message.chat.id, "📌 اسکرین‌شات شما برای بررسی به ادمین‌ها ارسال شد.\nبه محض تایید شدن توسط ادمینها به شما اطلاع داده خواهد شد")


@bot.callback_query_handler(func=lambda call: call.data.startswith(("approve","reject")))
def handle_admin_approval(call):
    action, user_id_str = call.data.split("|")
    user_id = int(user_id_str)
    if action == "approve":
        bot.send_message(user_id, "✅ واریزی شما تایید شد. با تشکر!")
        bot.answer_callback_query(call.id, "تایید شد")
    else:
        bot.send_message(user_id, "❌ واریزی شما رد شد. لطفا دوباره اقدام کنید.")
        bot.answer_callback_query(call.id, "رد شد")

        

@bot.message_handler(commands=["start"])
def start(message):
    try:
            
        user_id = message.from_user.id
        username = message.from_user.username or "بدون نام"
        
        for admin in ADMIN_IDS:
            if user_id == admin:
                bot.send_message(
                    user_id,
                    "👑 پنل مدیریت فعال شد:",
                    reply_markup=admin_panel_keyboard()
                    )
                return
        if activity_manager.is_loggin(user_id):
            bot.send_message(user_id, "خوش آمدید", reply_markup=main_markup())
        else:
            bot.send_message(user_id, "برای استفاده از ربات الزامی است وارد شورد!!")
            login(message)
    except Exception as ex:
        print(f"❌ [ERROR in /start] {ex}")
        bot.send_message(
            message.chat.id,
            "❌ یک خطای غیرمنتظره رخ داد. لطفاً دوباره تلاش کنید."
        )


def handle_admin_select_user(message):
    try:
        admin_id = message.from_user.id
        user_id = int(message.text.strip())
        msg = bot.send_message(admin_id, "📝 حالا متن پیام خود را وارد کنید:")
        bot.register_next_step_handler(msg, handle_admin_send_message, user_id)
    except ValueError:
        bot.send_message(message.chat.id, "❌ UID معتبر نیست. لطفاً فقط عدد وارد کنید.")
def handle_admin_send_message(message, user_id):
    ticket_text = message.text
    send_ticket_admin(user_id, ticket_text)
def handle_ticket_from_user(message):
    user_id = message.from_user.id
    ticket_text = message.text
    send_ticket(user_id, ticket_text)
    
def handle_ticket_from_admin(message):
    uid = message.text  
    msg = bot.send_message(message.chat.id, "پیغام خود را بفرستید:")
    

    bot.register_next_step_handler(msg, partial(handle_t, uid))

def handle_t(uid, message):
    ticket_text = message.text
    send_ticket_admin(uid, ticket_text, message)

def send_ticket_admin(user_id, ticket_text, message):
    try:
        bot.send_message(
            user_id,
            f"🆕 پیام جدید از ادمین\nتاریخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nمتن: {ticket_text}",
        )
        bot.send_message(message.chat.id, "✅ پیام ادمین با موفقیت ارسال شد.")
    except Exception as ex:
        print(f"❌ خطا در send_ticket_admin: {ex}")
        bot.send_message(user_id, "❌ ارسال پیام به کاربر با مشکل مواجه شد.")
@bot.message_handler(func=lambda message: message.chat.id)
def user_text_handler(message):
    try:
        text = message.text
        user_id = message.from_user.id

        if text == "login":
            bot.send_message(user_id, "🔑 لطفاً شماره خود را وارد کنید:")
            bot.register_next_step_handler(message, ) 
        elif text == "help":
            bot.send_message(user_id, ACTIVATION_TEXT)
        elif text == "قوانین" :
            bot.send_message(user_id, RULES_TEXT)
        elif text == "پشتیبانی":
            bot.send_message(message.chat.id, "📩 برای ارتباط با پشتیبانی با @Vahidrstn تماس بگیرید 📩")
        elif text == "ارسال تیکت":
            msg = bot.send_message(user_id, "📝 لطفاً متن تیکت خود را ارسال کنید:")
            bot.register_next_step_handler(msg, handle_ticket_from_user)
        elif text == "🧾 تسویه حساب":
            user_id = message.from_user.id
            account_settlement(user_id, message.chat.id)
        elif text == "قوانین":
            bot.send_message(message.chat.id, RULES_TEXT)   
        elif text == "آموزش استفاده از ربات":
            bot.send_message(message.chat.id, ACTIVATION_TEXT, reply_markup=main_markup())
        elif text == "محصولات":
            shopping_cart(message)
        elif text == "بازگشت" or text == "🔙 بازگشت به منو اصلی":
            bot.send_message(message.chat.id, "بازگشت به منوی اصلی:", reply_markup=main_markup())

        else:
            bot.send_message(message.chat.id, "❓ متوجه نشدم، لطفاً دوباره امتحان کنید.")

    except Exception as ex:
        print(f"❌ [ERROR in user_text_handler] {ex}")
        bot.send_message(message.chat.id, "❌ یک خطای غیرمنتظره رخ داد. دوباره تلاش کنید.")

#------------------------ MAIN ------------------------

if __name__ == "__main__":
    print("🤖 ربات شروع به کار کرد...")
    
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"❌ خطای کلی در اجرای ربات: {e}")