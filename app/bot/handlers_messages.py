from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramForbiddenError
from aiogram.types import Message
from filter_media import SupportedMediaFilter

from app.bot.utils import check_user_is_banned, extract_user_id
from app.core.config import settings
from app.core.db import get_async_session
from app.crud.message import crud_message
from app.crud.user import crud_user

router = Router()


@router.message(F.chat.type == 'private', F.text)
@router.message(F.chat.type == 'private', SupportedMediaFilter())
async def handle_user_request(message: Message, bot: Bot):
    print('FUNC: handle_user_request')

    # Проверка длины
    content = message.text or message.caption
    if content and len(content) > 3500:
        return await message.reply('Слишком длинное сообщение. Пожалуйста, сократите его до 3500 символов.')

    # Отправка в группу
    if message.content_type == 'text':
        await bot.send_message(
            chat_id=settings.GROUP_ID,
            text=(f'{message.text}\n\nИмя: {message.from_user.full_name}\nUsername: #id{message.from_user.id}'),
            message_thread_id=settings.MESSAGE_THREAD_ID,
            parse_mode='HTML',
        )
    else:
        await message.copy_to(
            chat_id=settings.GROUP_ID,
            message_thread_id=settings.MESSAGE_THREAD_ID,
            caption=((message.caption or '') + f'Имя: {message.from_user.full_name}\nUsername: #id{message.from_user.id}'),
            parse_mode='HTML',
        )

    # Работа с БД
    session_generator = get_async_session()
    session = await session_generator.__anext__()
    db_user = await crud_user.get_or_create_user_by_tg_message(message, session)

    if check_user_is_banned(db_user):
        return None

    # Сохраняем в БД
    message_data = {
        'telegram_user_id': message.from_user.id,
        'attachments': message.content_type != 'text',
    }
    if content:
        message_data['text'] = content

    await crud_message.create(message_data, session)

    await message.answer('Спасибо за обращение! Мы передали ваш запрос в техподдержку, пожалуйста, ожидайте 😊')


@router.message(F.chat.id == int(settings.GROUP_ID), F.reply_to_message)
async def send_message_answer(message: Message, bot: Bot):
    if not message.reply_to_message.from_user.is_bot:
        return None
    try:
        chat_id = extract_user_id(message.reply_to_message)
    except ValueError as err:
        return await message.reply(text=f'Не могу извлечь Id.  Возможно он некорректный. Текст ошибки:\n{err!s}')
    try:
        await message.copy_to(chat_id)
    except TelegramForbiddenError:
        await message.reply(text='Сообщение не доставлено. Бот был заблокировн пользователем, либо пользователь удален')
    session_generator = get_async_session()
    session = await session_generator.__anext__()
    db_user = await crud_user.get_or_create_user_by_tg_message(message, session)
    await crud_user.register_admin(db_user, session)
    message_data = {
        'telegram_user_id': message.from_user.id,
        'answer_to_user_id': chat_id,
    }
    if message.text:
        message_data['text'] = message.text
    elif message.caption:
        message_data['text'] = message.caption
        message_data['attachments'] = True

    await crud_message.create(message_data, session)
