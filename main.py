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
    button_ids = []
    for seq in WELCOME:
        for msg in seq:
            if msg.get("buttons"):
                for button in msg["buttons"]:
                    if not button.get("manually_defined", False):
                        button_ids.append(button["action_id"])

    for button_id in button_ids:
        @app.action(button_id)
        def handle_button_click(ack, body, say):
            ack()
            say("button go clicky :sleepybirb:", thread_ts=body["container"]["message_ts"])



@app.event("member_joined_channel")
def handle_member_joined_channel(body, say):
    user = app.client.users_info(user=body["event"]["user"])
    pronouns = user["user"]["profile"]["pronouns"]

    welcome_seq = WELCOME[0]
    initial_msg = None
    for msg in welcome_seq:
        new_msg = random.choice(msg["messages"])

        if "(pronouns)" in new_msg.lower():
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
            new_msg = new_msg.replace("(user_mention)", f"<@{body['event']['user']}>")

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

            sent_msg = say(blocks=blocks, icon_emoji=msg["icon_emoji"], username=msg["username"], thread_ts=initial_msg)
        else:
            sent_msg = say(
                text=new_msg,
                icon_emoji=msg["icon_emoji"],
                username=msg["username"],
                thread_ts=initial_msg,
            )

        if initial_msg is None:
            initial_msg = sent_msg["ts"]

        time.sleep(msg.get("delay", 1.8))




if __name__ == "__main__":
    generate_handlers(app)
    app.start(port=int(os.environ.get("PORT", 3000)))
