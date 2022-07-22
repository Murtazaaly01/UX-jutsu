# tools for jutsu plugins by @Kakashi_HTK(tg)/@ashwinstr(gh)

import re
import asyncio
import time
from typing import Union

from pymediainfo import MediaInfo
from pyrogram.errors import UserNotParticipant
from pyrogram.raw.functions.account import ReportPeer
from pyrogram.raw.types import (
    InputPeerUserFromMessage,
    InputReportReasonPornography,
    InputReportReasonSpam,
)
from userge import userge


# capitalise
def capitaled(query: str):
    query_split = query.split()
    cap_text = []
    for word_ in query_split:
        word_cap = word_.capitalize()
        cap_text.append(word_cap)
    return " ".join(cap_text)


# to report for spam or pornographic content
def report_user(chat: int, user_id: int, msg: dict, msg_id: int, reason: str):
    if ("nsfw" or "NSFW" or "porn") in reason:
        reason_ = InputReportReasonPornography()
        for_ = "pornographic message"
    else:
        reason_ = InputReportReasonSpam()
        for_ = "spam message"
    peer_ = (
        InputPeerUserFromMessage(
            peer=chat,
            msg_id=msg_id,
            user_id=user_id,
        ),
    )
    ReportPeer(
        peer=peer_,
        reason=reason_,
        message=msg,
    )
    return for_


# return time and date after applying time difference
def time_date_diff(year: int, month: int, date: int, hour: int, minute: int, diff: str):
    """time and date changer as per time-zone difference"""
    differ = diff.split(":")
    if int(differ[0]) >= 12 or int(differ[0]) <= -12 or int(differ[1]) >= 60:
        return "`Format of the difference given is wrong, check and try again...`"
    try:
        hour_diff = differ[0]
        hour_diff = int(hour_diff)
        min_diff = differ[1]
        min_diff = int(min_diff)

        if hour_diff < 0:
            minute -= min_diff
            if minute < 0:
                minute += 60
                hour -= 1
            hour -= hour_diff
            if hour < 0:
                date -= 1
                hour += 12
                ts = "PM"
            elif hour > 12 and hour < 24:
                hour -= 12
                ts = "PM"
            elif hour == 12:
                ts = "PM"
            else:
                ts = "AM"
            if date < 1:
                month -= 1
                if month < 1:
                    month = 12
                    year -= 1
                if month == (12 or 10 or 8 or 7 or 5 or 3 or 1):
                    date = 31
                elif month == (11 or 9 or 6 or 4):
                    date = 30
                else:
                    date = 29 if year % 4 == 0 else 28
        else:
            minute += min_diff
            if minute >= 60:
                hour += 1
                minute -= 60
            hour += hour_diff
            if hour > 12 and hour < 24:
                hour -= 12
                ts = "PM"
            elif hour == 12:
                ts = "PM"
            elif hour >= 24:
                hour -= 24
                date += 1
                ts = "AM"
            if date > 30 and month in {4, 6, 9, 11}:
                month += 1
                date -= 30
            elif date > 28 and month == 2 and year % 4 != 0:
                month += 1
                date -= 28
            elif date > 29 and month == 2 and year % 4 == 0:
                month += 1
                date -= 29
            elif date > 31 and month in {1, 3, 5, 7, 8, 10, 12}:
                month += 1
                date -= 31
                if month > 12:
                    month -= 12
                    year += 1
        hour = f"{hour:02}"
        minute = f"{minute:02}"
        date = f"{date:02}"
        month = f"{month:02}"
        return {
            "hour": hour,
            "min": minute,
            "stamp": ts,
            "date": date,
            "month": month,
            "year": year,
        }

    except Exception as e:
        return e

    
async def admin_or_creator(chat_id: int, user_id: int) -> dict:
    check_status = await userge.get_chat_member(chat_id, user_id)
    admin_ = check_status.status == "administrator"
    creator_ = check_status.status == "creator"
    return {"is_admin": admin_, "is_creator": creator_}


async def admin_chats(user_id: int) -> dict:
    list_ = []
    try:
        user_ = await userge.get_users(user_id)
    except:
        raise
    async for dialog in userge.iter_dialogs():
        if dialog.chat.type in ["group", "supergroup", "channel"]:
            try:
                check = await admin_or_creator(dialog.chat.id, user_.id)
                is_admin = check['is_admin']
                is_creator = check['is_creator']
            except UserNotParticipant:
                is_admin = False
                is_creator = False
            chat_ = dialog.chat
            if is_admin or is_creator:
                list_.append(
                    {
                        "chat_name": chat_.title,
                        "chat_id": chat_.id,
                        "chat_username": chat_.username,
                        "admin": is_admin,
                        "creator": is_creator,
                    }
                )
    return list_


async def get_response(msg, filter_user: Union[int, str] = 0, timeout: int = 5, mark_read: bool = False):
    await asyncio.sleep(timeout)
    if filter_user:
        try:
            user_ = await userge.get_users(filter_user)
        except:
            raise "Invalid user."
    for msg_ in range(1, 6):
        msg_id = msg.message_id + msg_
        try:
            response = await userge.get_messages(msg.chat.id, msg_id)
        except:
            raise "No response found."
        if response.reply_to_message.message_id == msg.message_id and (
            filter_user
            and response.from_user.id == user_.id
            or not filter_user
        ):
            if mark_read:
                await userge.send_read_acknowledge(msg.chat.id, response)
            return response
    raise "No response found in time limit."


def full_name(user: dict):
    try:
        f_name = " ".join([user.first_name, user.last_name or ""])
    except:
        raise
    return f_name


def msg_type(message):
    type_ = None
    if message.text:
        type_ = "text"
    elif message.audio:
        type_ = "audio"
    elif message.animation:
        type_ = "gif"
    elif message.photo:
        type_ = "photo"
    elif message.sticker:
        type_ = "sticker"
    elif message.video:
        type_ = "video"
    elif message.document:
        doc_ = message.document
        if doc_.file_name.endswith((".jpg", ".jpeg", ".png", "webp")):
            type_ = "photo"
        elif doc_.file_name.endswith((".mp4", ".gif", "webm")):
            type_ = "video"
        else:
            type_ = "file"
    return type_


def extract_id(mention):
    if str(mention).isdigit():
        return "Input is not a mention but an ID..."
    elif mention.startswith("@"):
        return "Input is not a mention but a username..."
    try:
        men = mention.html
    except:
        return "Input is not a mention."
    return filter[0] if (filter := re.search(r"\d+", men)) else "ID not found."


async def get_profile_pic(user_: Union[int, str]):
    try:
        user_entity = await userge.get_users(user_)
    except Exception as e:
        return e
    if user_entity.photo:
        pfp_ = await userge.download_media(user_entity.photo.big_file_id)
        return pfp_
    else:
        return None


class Media_Info:
    def data(self) -> dict:
        "Get downloaded media's information"
        found = False
        media_info = MediaInfo.parse(self)
        for track in media_info.tracks:
            if track.track_type == "Video":
                found = True
                type_ = track.track_type
                format_ = track.format
                duration_1 = track.duration
                other_duration_ = track.other_duration
                duration_2 = f"{other_duration_[0]} - ({other_duration_[3]})" if other_duration_ else None
                pixel_ratio_ = [track.width, track.height]
                aspect_ratio_1 = track.display_aspect_ratio
                other_aspect_ratio_ = track.other_display_aspect_ratio
                aspect_ratio_2 = other_aspect_ratio_[0] if other_aspect_ratio_ else None
                fps_ = track.frame_rate
                fc_ = track.frame_count
                media_size_1 = track.stream_size
                other_media_size_ = track.other_stream_size
                media_size_2 = [other_media_size_[1], other_media_size_[2], other_media_size_[3], other_media_size_[4]] if other_media_size_ else None

        return (
            {
                "media_type": type_,
                "format": format_,
                "duration_in_ms": duration_1,
                "duration": duration_2,
                "pixel_sizes": pixel_ratio_,
                "aspect_ratio_in_fraction": aspect_ratio_1,
                "aspect_ratio": aspect_ratio_2,
                "frame_rate": fps_,
                "frame_count": fc_,
                "file_size_in_bytes": media_size_1,
                "file_size": media_size_2,
            }
            if found
            else None
        )


def current_time(hour_diff: float) -> dict:
    "get current time with time difference in hours as input"
    time_sec = time.time()
    diff_in_hour = hour_diff
    diff_in_seconds = diff_in_hour * 60 * 60
    current_time_in_seconds = time_sec + diff_in_seconds
    day_ = current_time_in_seconds / (60 * 60 * 24)
    hour_ = (day_ - int(day_)) * 24
    minutes_ = (hour_ - int(hour_)) * 60
    minutes_ = int(minutes_)
    hour_ = int(hour_)
    if minutes_ > 59:
        hour_ += 1
        minutes_ -= 60
    if hour_ > 23:
        hour_ -= 24
    stamp_ = "AM" if hour_ < 12 else "PM"
    minutes_ = f"{minutes_:02}"
    hour_ = f"{hour_:02}"
    return {"H": hour_, "M": minutes_, "STAMP": stamp_}