import os
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
        new_msg =""

        if "she" in pronouns.lower():
            new_msg = msg["message"].replace("(ma'am/sir/strange person)", "miss")
        elif "he" in pronouns.lower():
            new_msg = msg["message"].replace("(ma'am/sir/strange person)", "sir")
        else:
            new_msg = msg["message"].replace("(ma'am/sir/strange person)", "strange person")
        msg = say(new_msg, icon_emoji=msg["icon_emoji"], username=msg["username"], thread_ts=initial_msg)
        if initial_msg is None:
            initial_msg = msg["ts"]


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
