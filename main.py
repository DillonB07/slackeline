import os
from re import X
import time
import random
import pytz

from dotenv import load_dotenv
from dialogue import SCHEDULED, WELCOME
from croniter import croniter
from datetime import datetime, timezone


from utils.airtable import AirtableManager
from utils.slack import app
from utils.utils import get_user_data
from utils.sequences import run_sequence

load_dotenv()

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
                run_sequence(seq, app)
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
                                    app,
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


if __name__ == "__main__":
    generate_handlers(app)

    import threading

    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()

    app.start(port=int(os.environ.get("PORT", 3000)))
