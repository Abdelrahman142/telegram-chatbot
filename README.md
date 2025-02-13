# Telegram System Monitor Bot 🚀  

This is a Telegram bot that allows you to monitor system performance, check running services, and list top resource-consuming processes.

## Features  
✅ Get system status (CPU, RAM, Disk usage)  
✅ Check if a service is running  
✅ List all active services and search for a specific one  
✅ Show the top 10 processes consuming the most CPU & RAM  

## Installation  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/Abdelrahman142/telegram-chatbot.git
cd telegram-chatbot
```
2️⃣ Install Dependencies
```
pip install -r requirements.txt
```
3️⃣ Set Up Your Bot
```
    Create a bot on Telegram using BotFather
    Get your bot token and replace TOKEN = "YOUR_BOT_TOKEN" in bot.py
```
4️⃣ Run the Bot
```
python bot.py
```
Usage

- Start the bot with /start and choose options from the keyboard.
Deployment

To keep the bot running, you can use:

    PM2 (for auto-restarting)

    pm2 start bot.py --interpreter python3
    pm2 save

    Systemd Service (for running as a background service)

License

This project is licensed under the MIT License.

Developed by Abdelrahman Ghazy 😎
