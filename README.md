# 🤖 Telegram Sales Management Bot  

A **powerful and fully automated Telegram bot** built with **Python** to manage product sales, user authentication, and order processing — all inside Telegram.  
This bot provides everything needed to run a full e-commerce workflow directly in chat, including admin control, discounts, product categories, and payment verification.

---

## 🚀 Features

- 💬 **Complete user system** — phone and email verification (OTP-based)  
- 🛍️ **Product management system** — supports categories, URLs, and dynamic product lists  
- 💳 **Cart and checkout system** with user-friendly inline menus  
- 📸 **Payment verification** through uploaded screenshots  
- 🏷️ **Discount code system** with admin creation and tracking  
- 👑 **Admin dashboard** with:  
  - Real-time user stats  
  - Product/category management  
  - Discount management  
  - Broadcast messaging  
  - Ticket system for user communication  
- 📦 Local **JSON database** for users, products, and discounts  
- 🔐 Secure, modular design ready for scaling  
- 🧠 Smart error handling & logging system

---

## ⚙️ Installation Guide

### 1️⃣ Clone the repository
```bash
git clone https://github.com/NIPROOT/powerful-and-fully-automated-Telegram-bot.git
cd <repo-name>
```

### 2️⃣ Install dependencies
```bash
pip install pyTelegramBotAPI
```

### 3️⃣ Create required files
Make sure the following files exist in your project directory:

```
users.json
admins.json
products.json
discount_codes.json
images.png
```

### 4️⃣ Add your bot token and admin IDs in `main.py`

```python
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
ADMIN_IDS = [1111111,9999999]
```

Then run the bot:

```bash
python main.py
```

---

## 🛒 How the Bot Works

1. User starts the bot with `/start`  
2. Bot requests phone number & email for verification  
3. Email OTP is sent to verify identity  
4. After successful login, user can:
   - Browse product categories  
   - View product details and add to cart  
   - Proceed to checkout  
   - Upload payment screenshot  
5. Admin receives order notification for approval or rejection  
6. Once approved, order is marked as completed  

---

## 🧩 Admin Features Overview

| Feature | Description |
|----------|-------------|
| 📊 **User Statistics** | View registered users and last activity |
| 🏷️ **Discount Codes** | Create, list, and delete codes dynamically |
| 📦 **Product Manager** | Add or remove categories and products |
| 📢 **Broadcast Message** | Send announcements to all users |
| 💬 **Ticket System** | Reply to user-submitted tickets |

---

## 🗂️ Project Structure

```
├── main.py                # Core bot logic
├── manage.py              # User management and activity tracking
├── users.json             # Registered users data
├── admins.json            # List of bot administrators
├── products.json          # Product database with categories
├── discount_codes.json    # Discount code storage
├── images.png             # Payment QR or account image
└── README.md              # Project documentation
```

---

## 🧠 Example Data

### 🛍 products.json
```json
{
  "smart_keys": {
    "product1": {
      "name": "Smart Door Lock",
      "Price": "1,500,000",
      "Url": "https://example.com/lock"
    }
  }
}
```

### 🎟 discount_codes.json
```json
{
  "SALE20": 0.2,
  "VIP100": 1.0
}
```

---

## 💡 Developer Notes

- Use **Python 3.9+** for best compatibility  
- Never share your **bot token** publicly  
- For production, use a **VPS or screen session** to keep the bot always running  
- You can modify `manage.py` to integrate real databases like SQLite or MongoDB

---
