import os
from re import X
import time
import random
import pytz

from slack_bolt import App
from dotenv import load_dotenv
from airtable import AirtableManager
from dialogue import SCHEDULED, WELCOME
from croniter import croniter
from datetime import datetime, timezone

from events.phone import send_phone_message
from views.home import generate_home_view

load_dotenv()

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)
airtable = AirtableManager(
    api_key=os.environ.get("AIRTABLE_API_KEY"),
    base_id=os.environ.get("AIRTABLE_BASE_ID"),
)

CHANNEL_ID = "C06R5NKVCG5" if os.environ.get("PORT", 3000) != 3000 else "C07AVPX7NM9"
WHITELISTED_USERS = ["U054VC2KM9P"]


def run_scheduler():
    tz = pytz.timezone("Europe/London")
    base_time = tz.localize(datetime.now())
    times = []
    for schedule in SCHEDULED:
        cron = croniter(schedule["cron"], base_time)
        next_time = cron.get_next(datetime)
        times.append(next_time)

    while True:
        now = tz.localize(datetime.now())
        for i, t in enumerate(times):
            if now >= t:
                seqs = SCHEDULED[i]["sequences"]
                seq = random.choice(seqs)
                run_sequence(seq)
                cron = croniter(SCHEDULED[i]["cron"], now)
                times[i] = cron.get_next(datetime)
        time.sleep(60)


def generate_handlers(app):
    for seq in WELCOME:
        for msg in seq:
            for button in msg.get("buttons", []):
                if button.get("type", "wait") != "custom":
                    match button.get("type"):
                        case "wait":

                            @app.action(button["action_id"])
                            def handle_wait_button_click(ack, body, say):
                                ack()
                                button_id = body["actions"][0]["action_id"]

                                next_msg = None
                                sequence = []
                                for seq in WELCOME:
                                    sequence = seq
                                    for i, msg in enumerate(seq):
                                        if msg.get("wait_for", "") == button_id:
                                            next_msg = (msg, i)

                                if not next_msg:
                                    print("not found message")
                                    say.info(
                                        f"No message found with the `wait_for` value {button_id}"
                                    )
                                    return

                                original_blocks = body["message"]["blocks"]

                                updated_blocks = [
                                    block
                                    for block in original_blocks
                                    if block["type"] != "actions"
                                ]

                                btn_text = next(
                                    (
                                        element["text"]["text"]
                                        for block in original_blocks
                                        if block["type"] == "actions"
                                        for element in block["elements"]
                                        if element["type"] == "button"
                                        and element["action_id"] == button_id
                                    ),
                                    None,
                                )

                                clicker = get_user_data(body, "user_id")
                                updated_blocks.append(
                                    {
                                        "type": "section",
                                        "text": {
                                            "type": "mrkdwn",
                                            "text": f"_<@{clicker}> pressed {btn_text}_",
                                        },
                                    }
                                )

                                app.client.chat_update(
                                    channel=body["container"]["channel_id"],
                                    ts=body["container"]["message_ts"],
                                    blocks=updated_blocks,
                                )

                                run_sequence(
                                    sequence,
                                    body,
                                    say,
                                    waited_for=button_id,
                                    thread_ts=body["container"]["message_ts"],
                                    i=next_msg[1],
                                )

                        case "custom":
                            # A custom handler should be created - we are not auto generating
                            pass
                        case _:

                            @app.action(button["action_id"])
                            def handle_button_click(ack, body, say):
                                ack()
                                button_id = body["actions"][0]["action_id"]
                                say(
                                    f"Ruh roh! Hey <@U054VC2KM9P>, <@{body['user']['id']}> clicked a button with an unknown type: {button['type']}",
                                    thread_ts=body["container"]["message_ts"],
                                )

                            raise ValueError(f"Unknown button type: {button['type']}")


def get_user_data(body, type=None):
    if body.get("type") == "block_actions":
        match type:
            case "user_id":
                return body["user"]["id"]
            case _:
                return body["user"]
    else:
        match type:
            case "user_id":
                return body["event"]["user"]
            case _:
                return body["event"]


def run_dialogue(msg, body, say, thread_ts=None):
    new_msg = random.choice(msg["messages"])

    if "(pronouns)" in new_msg.lower():
        user = app.client.users_info(user=get_user_data(body, type="user_id"))
        pronouns = user["user"]["profile"]["pronouns"]
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
            channel=CHANNEL_ID,
            blocks=blocks,
            icon_emoji=msg["icon_emoji"],
            username=msg["username"],
            thread_ts=thread_ts,
        )
    else:
        sent_msg = app.client.chat_postMessage(
            channel=CHANNEL_ID,
            text=new_msg,
            icon_emoji=msg["icon_emoji"],
            username=msg["username"],
            thread_ts=thread_ts,
        )

    return sent_msg


def run_sequence(seq, body=None, say=None, waited_for="", thread_ts=None, i=0):
    for msg in seq[i:]:

        if msg.get("wait_for", "") != waited_for:
            break

        sent_msg = run_dialogue(msg, body, say, thread_ts)

        if thread_ts is None:
            thread_ts = sent_msg["ts"]
        time.sleep(msg.get("delay", 1.8))


@app.event("member_joined_channel")
def handle_member_joined_channel(body, say):
    channel_id = body["event"]["channel"]
    if channel_id != CHANNEL_ID:
        return
    welcome_seq = random.choice(WELCOME)
    run_sequence(welcome_seq, body, say)


@app.event("message")
def handle_message(body, say):
    # check if message is DM and that dillon is running it
    if (
        body["event"].get("channel_type") == "im"
        and body["event"].get("user") == "U054VC2KM9P"
    ):
        message = body["event"]["text"]
        # message should be in the following format: "message <message> as <username> with <icon> in <channel/user>"
        if message.startswith("message"):
            message.replace("”", '"')
            message.replace("“", '"')
            message = message.split('message "')[1]
            message = message.split('" as "')
            message_text = message[0]
            message = message[1].split('" with "')
            username = message[0]
            message = message[1].split('" in ')
            icon = message[0]
            channel_unparsed = message[1]
            channel = channel_unparsed.split("|")[0]
            channel = channel[2:]
            channel = channel.strip(">")

            app.client.chat_postMessage(
                channel=channel,
                text=message_text,
                icon_emoji=icon,
                username=username,
            )


@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    generate_home_view(client, event, logger, airtable)


@app.action("submit_phone_call")
def handle_phone_submit(ack, body, client):
    ack()
    send_phone_message(body, client, airtable)


if __name__ == "__main__":
    generate_handlers(app)

    import threading

    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()

    app.start(port=int(os.environ.get("PORT", 3000)))
