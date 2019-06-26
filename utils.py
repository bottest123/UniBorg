import os, logging
from . import __main__
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
def get_args(message):
    try:
        message = message.message
    except AttributeError:
        pass
    if not message:
        return False
    return list(filter(lambda x: len(x) > 0, message.split(' ')))[1:]

def get_args_raw(message):
    try:
        message = message.message
    except AttributeError:
        pass
    if not message:
        return False
    args = message.split(' ', 1)
    if len(args) > 1:
        return args[1]

def get_args_split_by(message, s):
    m = get_args_raw(message)
    mess = m.split(s)
    return [st.strip() for st in mess]

def get_chat_id(message):
    chat = message.to_id
    attrs = chat.__dict__
    if len(attrs) != 1:
        return None
    return next(iter(attrs.values()))

def escape_html(text):
    return str(text).replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")

def escape_quotes(text):
    return str(text).replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;").replace('"', "&quot;")

def get_base_dir():
    return os.path.relpath(os.path.dirname(__main__.__file__))

async def get_user(message):
    try:
        return await message.client.get_entity(message.from_id)
    except ValueError: # Not in database. Lets go looking for them.
        logging.debug("user not in session cache. searching...")
    if isinstance(message.to_id, PeerUser):
        await message.client.get_dialogs()
        return await message.client.get_entity(message.from_id)
    elif isinstance(message.to_id, PeerChat) or isinstance(message.to_id, PeerChannel):
        async for user in message.client.iter_participants(message.to_id, aggressive=True):
            if user.id == message.from_id:
                return user
        logging.error("WTF! user isn't in the group where they sent the message")
        return None
    else:
        logging.error("WTF! to_id is not a user, chat or channel")
        return None
