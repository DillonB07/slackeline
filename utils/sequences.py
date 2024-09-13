from .utils import get_user_data

import os
import random
import time


def run_dialogue(msg, body, say, app, thread_ts=None):
    new_msg = random.choice(msg["messages"])

    if "(pronouns)" in new_msg.lower():
        user = app.client.users_info(user=get_user_data(body, type="user_id"))
        pronouns = user["user"]["profile"].get("pronouns", "they/them")

        replaced = False
        for replacement in msg.get("replacements", []):
            if replacement["replace"] in pronouns:
                new_msg = new_msg.replace("(pronouns)", replacement["with"])
                replaced = True
                break

        if not replaced:
            default = next(
                (
                    replacement["with"]
                    for replacement in msg.get("replacements", [])
                    if replacement.get("default")
                ),
                None,
            )
            new_msg = new_msg.replace("(pronouns)", default)

    if "user_mention" in new_msg.lower():
        new_msg = new_msg.replace(
            "(user_mention)", f"<@{get_user_data(body, type='user_id')}>"
        )

    if msg.get("buttons"):
        blocks = [
            {"type": "section", "text": {"type": "mrkdwn", "text": new_msg}},
            {"type": "actions", "elements": []},
        ]
        for button in msg["buttons"]:
            blocks[1]["elements"].append(
                {
                    "type": "button",
                    "text": {"type": "plain_text", "text": button["text"]},
                    "action_id": button["action_id"],
                }
            )

        sent_msg = app.client.chat_postMessage(
            channel=os.environ.get("CHANNEL_ID"),
            blocks=blocks,
            icon_emoji=msg["icon_emoji"],
            username=msg["username"],
            thread_ts=thread_ts,
        )
    else:
        sent_msg = app.client.chat_postMessage(
            channel=os.environ.get("CHANNEL_ID"),
            text=new_msg,
            icon_emoji=msg["icon_emoji"],
            username=msg["username"],
            thread_ts=thread_ts,
        )

    return sent_msg


def run_sequence(seq, app, body=None, say=None, waited_for="", thread_ts=None, i=0):
    for msg in seq[i:]:

        if msg.get("wait_for", "") != waited_for:
            break

        sent_msg = run_dialogue(msg, body, say, app, thread_ts)

        if thread_ts is None:
            thread_ts = sent_msg["ts"]
        time.sleep(msg.get("delay", 1.8))
