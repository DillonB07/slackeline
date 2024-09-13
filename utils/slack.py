from dotenv import load_dotenv
from slack_bolt import App
from dialogue import WELCOME
from events.phone import send_phone_message
from views.home import generate_home_view
from .sequences import run_sequence
from .airtable import airtable
import os
import random

load_dotenv()

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)

CHANNEL_ID = os.environ.get("CHANNEL_ID")


@app.event("member_joined_channel")
def handle_member_joined_channel(body, say):
    channel_id = body["event"]["channel"]
    if channel_id != CHANNEL_ID:
        return
    welcome_seq = random.choice(WELCOME)
    run_sequence(welcome_seq, app, body, say)


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
