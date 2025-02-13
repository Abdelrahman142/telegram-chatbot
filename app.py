from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import subprocess

TOKEN = "7344446832:AAHZXENjs1m052UXN4epwZKyl5hT5dfKaLI"

async def start(update: Update, context: CallbackContext):
    keyboard = [
        ["📊 System Status", "🔍 Check Service"], 
        ["🔝 Top 10 Processes", "🏠 Start"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("👋 Welcome! Choose an option:", reply_markup=reply_markup)

async def get_services():
    """Fetch all active services."""
    try:
        output = subprocess.check_output(["systemctl", "list-units", "--type=service", "--no-pager"], text=True)
        services = [line.split()[0] for line in output.split("\n") if ".service" in line]
        return services
    except Exception as e:
        print(f"Error getting services: {e}")
        return []

async def check_service(update: Update, context: CallbackContext):
    await update.message.reply_text("📌 Enter the service name or part of it to search:")

async def get_service_status(service_name):
    """Return detailed service status."""
    try:
        output = subprocess.check_output(["systemctl", "is-active", service_name], text=True).strip()
        return f"✅ Service `{service_name}` is **{output.upper()}**"
    except subprocess.CalledProcessError:
        return f"❌ Service `{service_name}` not found or inactive."

async def get_status(update: Update, context: CallbackContext):
    """Show system performance status."""
    cpu = subprocess.getoutput("top -bn1 | grep 'Cpu(s)' | awk '{print $2}'")
    mem = subprocess.getoutput("free -m | awk 'NR==2{printf \"%.2f%%\", $3*100/$2 }'")
    disk = subprocess.getoutput("df -h / | awk 'NR==2{print $5}'")

    message = (
        "📊 **System Performance**\n"
        f"🖥 **CPU Usage:** `{cpu}%`\n"
        f"💾 **RAM Usage:** `{mem}`\n"
        f"📂 **Disk Usage:** `{disk}`"
    )

    await update.message.reply_text(message, parse_mode="Markdown")

async def get_top_processes(update: Update, context: CallbackContext):
    """Fetch top 10 resource-intensive processes."""
    try:
        output = subprocess.check_output(
            "ps -eo pid,comm,%cpu,%mem --sort=-%cpu | head -n 11", shell=True, text=True
        )
        processes = output.strip().split("\n")[1:]  # Skip header

        message = "🔝 **Top 10 Processes by CPU Usage:**\n"
        for proc in processes:
            parts = proc.split()
            pid, name, cpu, mem = parts[0], parts[1], parts[2], parts[3]
            message += f"🆔 `{pid}` | **{name}** | ⚡ CPU: `{cpu}%` | 🏗 RAM: `{mem}%`\n"

        await update.message.reply_text(message, parse_mode="Markdown")
    except Exception as e:
        print(f"Error fetching processes: {e}")
        await update.message.reply_text("❌ Failed to retrieve process list.")

async def handle_text(update: Update, context: CallbackContext):
    text = update.message.text.strip()

    if text == "📊 System Status":
        await get_status(update, context)
    elif text == "🔍 Check Service":
        await check_service(update, context)
    elif text == "🔝 Top 10 Processes":
        await get_top_processes(update, context)
    elif text == "🏠 Start":
        await start(update, context)
    else:
        services = await get_services()
        matched_services = [s for s in services if text.lower() in s.lower()]

        if not matched_services:
            await update.message.reply_text("❌ No matching service found.")
            return

        if len(matched_services) == 1:
            service_status = await get_service_status(matched_services[0])
            await update.message.reply_text(service_status, parse_mode="Markdown")
            return

        keyboard = [[s] for s in matched_services] + [["🏠 Start"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text("📌 Select a service:", reply_markup=reply_markup)

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("🚀 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

