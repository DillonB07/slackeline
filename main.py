import os
import time
import random

from slack_bolt import App
from dotenv import load_dotenv
from dialogue import WELCOME

load_dotenv()

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)

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
                                    print('not found message')
                                    say.info(f"No message found with the `wait_for` value {button_id}")
                                    return

                                original_blocks = body["message"]["blocks"]

                                updated_blocks = [block for block in original_blocks if block["type"] != "actions"]

                                btn_text = next(
                                    (
                                        element["text"]["text"] for block in original_blocks if block["type"] == "actions" for element in block["elements"] if element["type"] == "button" and element["action_id"] == button_id
                                    ), None
                                )

                                clicker = get_user_data(body, "user_id")
                                updated_blocks.append({
                                    "type": "section",
                                    "text": {
                                        "type": "mrkdwn",
                                        "text": f"_<@{clicker}> pressed {btn_text}_"
                                    }
                                })


                                app.client.chat_update(
                                    channel=body["container"]["channel_id"],
                                    ts=body["container"]["message_ts"],
                                    blocks=updated_blocks,
                                )

                                run_sequence(sequence, next_msg[1], body, say, waited_for=button_id, thread_ts=body["container"]["message_ts"])

                        case "custom":
                            # A custom handler should be created - we are not auto generating
                            pass
                        case _:
                            @app.action(button["action_id"])
                            def handle_button_click(ack, body, say):
                                ack()
                                button_id = body["actions"][0]["action_id"]
                                say(f"Ruh roh! Hey <@U054VC2KM9P>, <@{body['user']['id']}> clicked a button with an unknown type: {button['type']}", thread_ts=body["container"]["message_ts"])

                            raise ValueError(f"Unknown button type: {button['type']}")

def get_user_data(body, type=None):
    if body.get('type') == 'block_actions':
        match type:
            case "user_id":
                return body['user']['id']
            case _:
                return body['user']
    else:
        match type:
            case "user_id":
                return body['event']['user']
            case _:
                return body['event']

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
        new_msg = new_msg.replace("(user_mention)", f"<@{get_user_data(body, type='user_id')}>")

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

        sent_msg = say(blocks=blocks, icon_emoji=msg["icon_emoji"], username=msg["username"], thread_ts=thread_ts)
    else:
        sent_msg = say(
            text=new_msg,
            icon_emoji=msg["icon_emoji"],
            username=msg["username"],
            thread_ts=thread_ts,
        )

    return sent_msg


def run_sequence(seq, i, body, say, waited_for="", thread_ts=None):
    for msg in seq[i:]:

        if msg.get("wait_for", "") != waited_for:
            break

        sent_msg = run_dialogue(msg, body, say, thread_ts)

        if thread_ts is None:
            thread_ts = sent_msg["ts"]
        time.sleep(msg.get("delay", 1.8))


@app.event("member_joined_channel")
def handle_member_joined_channel(body, say):
    welcome_seq = random.choice(WELCOME)
    run_sequence(welcome_seq, 0, body, say)


if __name__ == "__main__":
    generate_handlers(app)
    app.start(port=int(os.environ.get("PORT", 3000)))
