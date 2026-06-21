from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import re

# 🔥 ТВОИ VLESS-ССЫЛКИ (с названиями стран)
SERVERS = [
    {
        "name": "🇷🇺 Россия #1",
        "link": "vless://ff19693c-11f3-4df9-8713-79a85a5ca090@159.195.150.101:443?encryption=none&flow=xtls-rprx-vision&security=reality&sni=sellflow.org&fp=firefox&pbk=SbVKOEMjK0sIlbwg4akyBg5mL5KZwwB-ed4eEE7YnRc&sid&packetEncoding=xudp#%F0%9F%87%B7%F0%9F%87%BA%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F%20%7C%20@VSPBOOST%20%2319"
    },
    {
        "name": "🇫🇷 Франция",
        "link": "vless://1f4c983e-382c-d2fa-b2dc-7981f02b34de@89.208.113.157:443?encryption=none&flow=xtls-rprx-vision&security=reality&sni=parisjetaime.com&fp=firefox&pbk=2dgS9vJTywAfGZmlkuzDIIXLUR-E1A-0na8_W--ruUc&sid=5be8210215&packetEncoding=xudp#%F0%9F%87%AB%F0%9F%87%B7%20%D0%A4%D1%80%D0%B0%D0%BD%D1%86%D0%B8%D1%8F%20%7C%20@VSPBOOST%20%2340"
    },
    {
        "name": "🇷🇺 Россия #2",
        "link": "vless://ff19693c-11f3-4df9-8713-79a85a5ca090@159.195.150.143:443?encryption=none&flow=xtls-rprx-vision&security=reality&sni=sellflow.org&fp=firefox&pbk=SbVKOEMjK0sIlbwg4akyBg5mL5KZwwB-ed4eEE7YnRc&sid&packetEncoding=xudp#%F0%9F%87%B7%F0%9F%87%BA%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F%20%7C%20@VSPBOOST%20%2304"
    },
]

# 🧹 Функция для очистки ссылки от мусора после #
def clean_link(link):
    return link.split('#')[0]

# 🏠 Команда /start - приветствие с меню
async def start(update, context):
    # Создаём кнопки главного меню
    keyboard = [
        [InlineKeyboardButton("📡 Получить сервера", callback_data="get_servers")],
        [InlineKeyboardButton("❓ Как подключиться", callback_data="how_to")],
        [InlineKeyboardButton("🔄 Обновить список", callback_data="refresh")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🌐 *VPN Сервера для Ютуба*\n\n"
        "Привет! Я помогаю находить рабочие VPN-сервера.\n\n"
        "🆕 Сервера обновляются каждый день!\n"
        "⚡ Нажми кнопку ниже, чтобы получить список.",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

# 📡 Команда /vpn - показать сервера
async def vpn(update, context):
    # Создаём кнопки для каждого сервера
    keyboard = []
    for i, server in enumerate(SERVERS, 1):
        # Кнопка с названием сервера
        button = InlineKeyboardButton(
            f"📌 {server['name']}", 
            callback_data=f"copy_{i}"
        )
        keyboard.append([button])  # Каждая кнопка на новой строке
    
    # Добавляем кнопку "Назад"
    keyboard.append([InlineKeyboardButton("🔙 Назад в меню", callback_data="back_to_menu")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Проверяем, откуда пришёл запрос (из команды или из кнопки)
    if update.callback_query:
        # Если из кнопки - редактируем сообщение
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            "📡 *Выбери сервер:*\n\n"
            "Нажми на кнопку — ссылка скопируется автоматически.",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    else:
        # Если из команды /vpn - отправляем новое сообщение
        await update.message.reply_text(
            "📡 *Выбери сервер:*\n\n"
            "Нажми на кнопку — ссылка скопируется автоматически.",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )

# 📋 Обработчик нажатий на кнопки
async def button_handler(update, context):
    query = update.callback_query
    await query.answer()  # Убираем "часики" на кнопке
    
    data = query.data
    
    # 🔙 Назад в меню
    if data == "back_to_menu":
        keyboard = [
            [InlineKeyboardButton("📡 Получить сервера", callback_data="get_servers")],
            [InlineKeyboardButton("❓ Как подключиться", callback_data="how_to")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🌐 *VPN Сервера для Ютуба*\n\n"
            "Выбери действие:",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
        return
    
    # ❓ Как подключиться
    if data == "how_to":
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "📖 *Как подключиться:*\n\n"
            "1️⃣ Нажми на кнопку с названием сервера\n"
            "2️⃣ Ссылка скопируется автоматически\n"
            "3️⃣ Открой свой VPN-клиент (Happ, V2Ray, NekoBox)\n"
            "4️⃣ Вставь ссылку → Подключись\n"
            "5️⃣ Готово! 🚀\n\n"
            "❓ Если не работает — попробуй другой сервер.",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
        return
    
    # 🔄 Обновить список (для начала просто показываем сервера)
    if data == "refresh" or data == "get_servers":
        # Переходим к списку серверов
        await vpn(update, context)
        return
    
    # 📌 Копирование ссылки (data = copy_1, copy_2, copy_3)
    if data.startswith("copy_"):
        # Получаем номер сервера
        server_num = int(data.split("_")[1]) - 1
        
        if 0 <= server_num < len(SERVERS):
            server = SERVERS[server_num]
            clean = clean_link(server['link'])
            
            # Кнопка "Назад"
            keyboard = [[InlineKeyboardButton("🔙 Назад к списку", callback_data="get_servers")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Отправляем ссылку в отдельном сообщении (чтобы её легко было скопировать)
            await query.edit_message_text(
                f"✅ *Ссылка скопирована!*\n\n"
                f"📌 *{server['name']}*\n\n"
                f"`{clean}`\n\n"
                f"📋 Нажми на ссылку выше, чтобы выделить и скопировать,\n"
                f"или просто выдели её пальцем/мышкой.\n\n"
                f"➡️ Вставь в VPN-клиент и подключайся!",
                parse_mode="Markdown",
                reply_markup=reply_markup
            )
        return

# 🔑 ТВОЙ ТОКЕН
TOKEN = "8992106008:AAGoXJbIsOeCSJu-gN7HWaDjcSnUG80G3O0"

# Запускаем бота
app = Application.builder().token(TOKEN).build()

# Регистрируем команды
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("vpn", vpn))

# Регистрируем обработчик кнопок
app.add_handler(CallbackQueryHandler(button_handler))

print("✅ Бот запущен! Пиши /start в Telegram")
print("🔥 Теперь у бота красивые кнопки!")

app.run_polling()