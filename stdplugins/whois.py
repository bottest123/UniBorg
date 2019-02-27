from telethon import events
from telethon.tl.functions.users import GetFullUserRequest
import os
from telethon.tl.types import MessageEntityMentionName
from telethon.utils import get_input_location


@borg.on(events.NewMessage(pattern="\.whois ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    replied_user = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.forward:
            replied_user = await borg(GetFullUserRequest(previous_message.forward.from_id or previous_message.forward.channel_id))
        else:
            replied_user = await borg(GetFullUserRequest(previous_message.from_id))
    else:
        input_str = event.pattern_match.group(1)
        if event.message.entities is not None:
            mention_entity = event.message.entities
            probable_user_mention_entity = mention_entity[0]
            if type(probable_user_mention_entity) == MessageEntityMentionName:
                user_id = probable_user_mention_entity.user_id
                replied_user = await borg(GetFullUserRequest(user_id))
            else:
                # the disgusting CRAP way, of doing the thing
                try:
                    user_object = await borg.get_entity(input_str)
                    user_id = user_object.id
                    replied_user = await borg(GetFullUserRequest(user_id))
                except e:
                    await event.edit(str(e))
                    return None
        else:
            try:
                user_object = await borg.get_entity(input_str)
                user_id = user_object.id
                replied_user = await borg(GetFullUserRequest(user_id))
            except Exception as e:
                await event.edit(str(e))
                return None
    user_id = replied_user.user.id
    first_name = replied_user.user.first_name
    # some weird people (like me) have more than 4096 characters in their names
    first_name = first_name.replace("\u2060", "")
    # inspired by https://telegram.dog/afsaI181
    user_bio = replied_user.about
    common_chats = replied_user.common_chats_count
    try:
        dc_id, location = get_input_location(replied_user.profile_photo)
        photo = await borg.download_profile_photo(
            user_id,
            Config.TMP_DOWNLOAD_DIRECTORY + str(user_id) + ".jpg",
            download_big=True
        )
    except TypeError as e:
        dc_id = "__ need a Profile Picture for this to work __"
        photo = "http://telegra.ph/file/457126e7cd1ade29d2a65.jpg"
    caption = "ID: `{}` \nName: [{}](tg://user?id={}) \nBio: {}\nDC ID: {}\nGroups In Common: {}".format(user_id, first_name, user_id, user_bio, dc_id, common_chats)
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = event.message.id
    await borg.send_file(
        event.chat_id,
        photo,
        caption=caption,
        force_document=False,
        reply_to=message_id_to_reply
    )
    if not photo.startswith("http"):
        os.remove(photo)
    await event.delete()