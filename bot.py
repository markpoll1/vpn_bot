from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import json
import os
from datetime import datetime

VERSION = "0.0.4"
ADMINS = [6357610038]

GITHUB_USERNAME = "markpoll1"
VPN_SUB_URL = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/vpn_bot/main/subscriptions/vpn.txt"

STATS_FILE = "stats.json"

def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"users": [], "total_vpn_uses": 0, "daily_uses": {}}

def save_stats(stats):
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

def get_today():
    return datetime.now().strftime("%Y-%m-%d")

async def start(update, context):
    user_id = str(update.effective_user.id)
    username = update.effective_user.username or "без имени"
    
    stats = load_stats()
    if user_id not in stats["users"]:
        stats["users"].append(user_id)
        save_stats(stats)
    
    date_str = datetime.now().strftime("%d.%m.%Y")
    
    keyboard = [
        [InlineKeyboardButton("📥 Подписка VPN", callback_data="sub_vpn")],
        [InlineKeyboardButton("❓ Как подключиться", callback_data="how_to")],
        [InlineKeyboardButton("📩 Связь со мной", callback_data="contact")],
    ]
    if update.effective_user.id in ADMINS:
        keyboard.append([InlineKeyboardButton("📊 Статистика", callback_data="stats")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"🌟 *ДОБРО ПОЖАЛОВАТЬ В VPN БОТ!*\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🌐 *VPN Сервера*\n"
        f"📅 Обновлено: {date_str}\n"
        f"📦 Версия: `{VERSION}`\n\n"
        f"👋 Привет, *@{username}*!\n\n"
        f"📥 *Используй подписку VPN:*\n"
        f"   • 📥 Подписка VPN\n\n"
        f"🔄 *Сервера обновляются периодически.*\n"
        f"📊 *Доступно 15 серверов.*\n\n"
        f"⚠️ *Если сервер не работает:*\n"
        f"Нажми на кнопку *«Связь со мной»*\n"
        f"и напиши мне — я помогу!\n\n"
        f"⚡ *Нажми кнопку ниже, чтобы начать!*",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def vpn(update, context):
    await start(update, context)

async def send_subscription(update, context):
    query = update.callback_query
    await query.answer()
    
    keyboard = [[InlineKeyboardButton("🔙 В главное меню", callback_data="back_to_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"📥 *ПОДПИСКА VPN*\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Скопируй ссылку и добавь в раздел *«Подписки»*\n"
        f"в своём VPN-клиенте (Hiddify, NekoBox, V2RayN):\n\n"
        f"`{VPN_SUB_URL}`\n\n"
        f"📋 *Как добавить:*\n"
        f"1️⃣ Открой клиент → раздел «Подписки»\n"
        f"2️⃣ Нажми «Добавить» → вставь ссылку\n"
        f"3️⃣ Нажми «Обновить» — все 15 серверов подгрузятся!\n\n"
        f"🔄 *Совет:*\n"
        f"Обновляйте подписку раз в 24 часа,\n"
        f"чтобы всегда иметь актуальные сервера.\n\n"
        f"📌 *При обновлении списка на GitHub,*\n"
        f"клиент сам подхватит новые сервера!",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def button_handler(update, context):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = update.effective_user.id
    
    if data == "back_to_menu":
        keyboard = [
            [InlineKeyboardButton("📥 Подписка VPN", callback_data="sub_vpn")],
            [InlineKeyboardButton("❓ Как подключиться", callback_data="how_to")],
            [InlineKeyboardButton("📩 Связь со мной", callback_data="contact")],
        ]
        if user_id in ADMINS:
            keyboard.append([InlineKeyboardButton("📊 Статистика", callback_data="stats")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🌐 *ГЛАВНОЕ МЕНЮ*\n━━━━━━━━━━━━━━━━━━━━━\n\n*Выбери действие:*",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
        return
    
    if data == "sub_vpn":
        await send_subscription(update, context)
        return
    
    if data == "how_to":
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "📖 *КАК ПОДКЛЮЧИТЬСЯ*\n━━━━━━━━━━━━━━━━━━━━━\n\n"
            "📥 *Способ 1 — Подписка (рекомендуемый):*\n"
            "1️⃣ Нажми на кнопку «Подписка VPN»\n"
            "2️⃣ Скопируй ссылку\n"
            "3️⃣ Открой VPN-клиент → раздел «Подписки»\n"
            "4️⃣ Вставь ссылку → нажми «Обновить»\n"
            "5️⃣ Все 15 серверов подгрузятся автоматически!\n"
            "6️⃣ Обновляйте подписку раз в 24 часа\n\n"
            "📱 *Лучшие клиенты для VPN:*\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "🔹 *Android / iOS:*\n"
            "   • Happ\n   • Streisland\n   • Hiddify\n"
            "   • INCY\n   • V2BOX\n   • V2RayTun\n\n"
            "🔹 *Windows:*\n"
            "   • V2RayN\n   • Throne",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
        return
    
    if data == "contact":
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "📩 *СВЯЗЬ СО МНОЙ*\n━━━━━━━━━━━━━━━━━━━━━\n\n"
            "💬 *Что ты можешь написать:*\n"
            "   • Сообщить о неработающем сервере\n"
            "   • Предложения по улучшению\n"
            "   • Идеи для новых функций\n"
            "   • Вопросы и отзывы\n\n"
            "✍️ *Напиши мне:*\n"
            "   @dsfk13\n\n"
            "💪 Спасибо, что пользуешься ботом!",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
        return
    
    if data == "stats":
        if user_id not in ADMINS:
            keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                "🔒 *ДОСТУП ЗАПРЕЩЁН*\n━━━━━━━━━━━━━━━━━━━━━\n\nСтатистика доступна только администратору.",
                parse_mode="Markdown",
                reply_markup=reply_markup
            )
            return
        
        stats = load_stats()
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"📊 *СТАТИСТИКА БОТА*\n━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"👤 Всего пользователей: `{len(stats['users'])}`\n"
            f"📡 Всего запросов: `{stats['total_vpn_uses']}`\n"
            f"📊 Сегодня: `{stats['daily_uses'].get(get_today(), 0)}`",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
        return

TOKEN = os.environ.get("TOKEN")

if not TOKEN:
    print("❌ Ошибка: Токен не найден! Добавьте TOKEN в переменные окружения на Bothost.")
    exit(1)

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("vpn", vpn))
app.add_handler(CallbackQueryHandler(button_handler))

print("✅ Бот запущен!")
print(f"📦 Версия: {VERSION}")
print(f"\n📥 Подписка VPN: {VPN_SUB_URL}")

app.run_polling()
