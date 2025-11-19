from dotenv import load_dotenv
from slack_bolt import App
from slack_sdk import WebClient
from dialogue import WELCOME
from events.phone import send_phone_message
from views.home import generate_home_view
from views.answer import generate_view as generate_answer_view
from .sequences import run_sequence
from .airtable import airtable
import os
import random
import json

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
    invited_by = body["event"].get("inviter", "U054VC2KM9P")
    user_id = body["event"]["user"]
    app.client.chat_postMessage(
        channel="U054VC2KM9P",
        text=f"<@{user_id}> just joined <#{channel_id}>! :tada: Invited by <@{invited_by}>",
    )
    run_sequence(welcome_seq, app, body, say)


@app.event("member_left_channel")
def handle_member_left_channel(client, body, say):
    channel_id = body["event"]["channel"]
    user_id = body["event"]["user"]
    if channel_id != CHANNEL_ID:
        return
    client.chat_postMessage(
        channel="U054VC2KM9P",
        text=f"<@{user_id}> just left <#{channel_id}> :(",
    )


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
@app.view("answer_call")
def handle_phone_submit(ack, body, client):
    ack()
    send_phone_message(body, client, airtable)


@app.shortcut("respond_to_call")
def respond_to_call(ack, body, client: WebClient):
    ack()
    ts = body["message"]["ts"]
    channel_id = body["channel"]["id"]
    view = generate_answer_view(ts, channel_id)
    client.views_open(
        trigger_id=body["trigger_id"],
        view=view
    )


@app.command("/joinamberschannel")
def join_ambers_channel(ack, body, client):
    ack()
    user_id = body["user_id"]

    client.conversations_invite(
        channel=CHANNEL_ID,
        users=user_id
    )

@app.command("/find-mailee")
def find_mailee(ack, body, client, respond):
    ack()
    user_id = body["user_id"]

    if user_id != "U054VC2KM9P":
        client.chat_postMessage(
            channel=user_id,
            text="Sorry, this command is only available for amber!"
        )
        return
    
    records = client.slackLists_items_list(list_id=os.environ.get("MAIL_LIST_ID"), limit=100)
    mailee = random.choice(records["items"])
    id = None
    address = None
    for field in mailee["fields"]:
        if field["key"] == "Person":
            id = json.loads(field["user"])[0]
        if field["key"] == "Address":
            address = field["rich_text"]
    
    if not id or not address:
        respond(
            text="Could not find a valid mailee!"
        )
        return
    
    respond(
        text=f"you need to send mail too.... <@{id}>!! :tada:!"
    )
    
    client.chat_postMessage(
        channel=user_id,
        blocks=[
            address
        ]
    )