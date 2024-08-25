import os
import time
from slack_bolt import App
from dotenv import load_dotenv
from dialogue import WELCOME

load_dotenv()

# Initialize your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

@app.event("member_joined_channel")
def handle_member_joined_channel(body, say):
    user = app.client.users_info(user=body['event']['user'])
    pronouns = user['user']['profile']['pronouns']

    welcome_seq = WELCOME[0]
    initial_msg = None
    for msg in welcome_seq:
        new_msg = msg["message"]

        if "(pronouns)" in new_msg.lower():
            replaced = False
            for replacement in msg.get("replacements", []):
                if replacement["replace"] in pronouns:
                    new_msg = new_msg.replace("(pronouns)", replacement["with"])
                    replaced = True
                    break

            if not replaced:
                default = next((replacement["with"] for replacement in msg.get("replacements", []) if replacement.get("default")), None)
                new_msg = new_msg.replace("(pronouns)", default)

        if "user_mention" in new_msg.lower():
            new_msg = new_msg.replace("(user_mention)", f"<@{body['event']['user']}>")

        sent_msg = say(text=new_msg, icon_emoji=msg["icon_emoji"], username=msg["username"], thread_ts=initial_msg)

        if initial_msg is None:
            initial_msg = sent_msg["ts"]

        time.sleep(msg.get("delay", 1.8))


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
