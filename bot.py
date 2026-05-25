import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8230162109:AAFvdA1hMNTBHcuAgSS04EIVjm5KOdJSeA4"

def get_habr_news():
    url = "https://habr.com/ru/news/"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("article", class_="tm-articles-list__item")
        news = []
        for article in articles[:5]:
            title_tag = article.find("a", class_="tm-title__link")
            if title_tag:
                title = title_tag.get_text(strip=True)
                link = "https://habr.com" + title_tag["href"]
                news.append(f"- {title}\n  {link}")
        return "\n".join(news) if news else "Новостей пока нет."
    except Exception as e:
        return f"Ошибка: {e}"

def get_vc_news():
    url = "https://vc.ru/"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("div", class_="feed__item")
        news = []
        for article in articles[:5]:
            title_tag = article.find("a", class_="content-link")
            if title_tag:
                title = title_tag.get_text(strip=True)
                link = title_tag["href"]
                if not link.startswith("http"):
                    link = "https://vc.ru" + link
                news.append(f"- {title}\n  {link}")
        return "\n".join(news) if news else "Новостей пока нет."
    except Exception as e:
        return f"Ошибка: {e}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я InfoDigger.\n\n"
        "/news — сводка с Habr и VC.ru\n"
        "/habr — только Habr\n"
        "/vc — только VC.ru\n"
        "/help — помощь"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/news — полная сводка\n"
        "/habr — IT-новости\n"
        "/vc — бизнес и стартапы"
    )

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Собираю новости...")
    habr_news = get_habr_news()
    vc_news = get_vc_news()
    message = f"Habr:\n{habr_news}\n\nVC.ru:\n{vc_news}"
    await update.message.reply_text(message)

async def habr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Собираю Habr...")
    await update.message.reply_text(get_habr_news())

async def vc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Собираю VC.ru...")
    await update.message.reply_text(get_vc_news())

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("news", news))
    app.add_handler(CommandHandler("habr", habr))
    app.add_handler(CommandHandler("vc", vc))
    print("Бот запущен.")
    app.run_polling()

if __name__ == "__main__":
    main()