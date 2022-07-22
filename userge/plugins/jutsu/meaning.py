from PyDictionary import PyDictionary

from userge import Message, userge


@userge.on_cmd(
    "mng",
    about={
        "header": "use this to find meaning of any word.",
        "examples": [
            "{tr}mng [word] or [reply to msg]",
        ],
    },
)
async def meaning_wrd(message: Message):
    """meaning of word"""
    await message.edit("`Searching for meaning...`")
    if word := message.input_str or message.reply_to_message.text:
        dictionary = PyDictionary()
        words = dictionary.meaning(word)
        output = f"**Word :** __{word}__\n"
        try:
            for a, b in words.items():
                output = f"{output}\n**{a}**\n"
                for i in b:
                    output = f"{output}• __{i}__\n"
            await message.edit(output)
        except Exception:
            await message.err(f"Couldn't fetch meaning of {word}")

    else:
        await message.err("no input!")


@userge.on_cmd(
    "syn",
    about={
        "header": "use this to find synonyms of any word.",
        "examples": [
            "{tr}syn [word] or [reply to msg]",
        ],
    },
)
async def synonym_wrd(message: Message):
    """synonym of word"""
    await message.edit("`Searching for synonyms...`")
    if word := message.input_str or message.reply_to_message.text:
        dictionary = PyDictionary()
        words = dictionary.synonym(word)
        output = f"**Synonym for :** __{word}__\n"
        try:
            for a in words:
                output = f"{output}• __{a}__\n"
            await message.edit(output)
        except Exception:
            await message.err(f"Couldn't fetch synonyms of {word}")

    else:
        await message.err("no input!")


@userge.on_cmd(
    "ayn",
    about={
        "header": "use this to find antonym of any word.",
        "examples": [
            "{tr}ayn [word] or [reply to msg]",
        ],
    },
)
async def antonym_wrd(message: Message):
    """antonym of word"""
    await message.edit("`Searching for antonyms...`")
    if word := message.input_str or message.reply_to_message.text:
        dictionary = PyDictionary()
        words = dictionary.antonym(word)
        output = f"**Antonym for :** __{word}__\n"
        try:
            for a in words:
                output = f"{output}• __{a}__\n"
            await message.edit(output)
        except Exception:
            await message.err(f"Couldn't fetch antonyms of {word}")

    else:
        await message.err("no input!")
