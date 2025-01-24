import logging
import os

from aiogram import Bot, Dispatcher
from aiohttp import web
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.environ.get("BOT_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def notify(request):
    try:
        data = await request.json()
        telegram_id = data.get('telegram_id')
        order_id = data.get('order_id')
        new_status = data.get('new_status')
        # Добавьте обработку других необходимых полей

        if not telegram_id or not order_id or not new_status:
            return web.json_response({'error': 'Missing required fields'}, status=400)

        message = f'Ваш заказ #{order_id} изменил статус на: {new_status}'
        await bot.send_message(chat_id=telegram_id, text=message)
        return web.json_response({'status': 'success'})
    except Exception as e:
        logging.error(f'Ошибка при отправке сообщения: {e}')
        return web.json_response({'error': str(e)}, status=500)

app = web.Application()
app.router.add_post('/notify/', notify)

if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=8080)