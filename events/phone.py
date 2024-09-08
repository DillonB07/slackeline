import json

BLACKLISTED_CHANNELS = []


def send_phone_message(body, client, airtable):
    user_id = body["user"]["id"]
    user_data = airtable.get_user(user_id)

    if not user_data or (not user_data['fields'].get('Allowed to Phone') and not user_data['fields'].get('Admin')):
        client.chat_postMessage(channel=user_id, text="You are not allowed to use this feature.")
        return

    location = body["view"]["state"]["values"]["conversations_select"][
        "conversations_select-action"
    ]["selected_conversation"]
    message = body["view"]["state"]["values"]["message_input"]["message_input"]["value"]
    emoji = body["view"]["state"]["values"]["emoji"]["emoji"]["value"]
    username = body["view"]["state"]["values"]["username"]["username"]["value"]
    print(
        f"Sending {message} as {username} with {emoji} to {location} - {body['user']}"
    )

    # check if the bot is in the channel
    # if not, invite the bot to the channel
    # if location[0] == "C":
    #     if not client.conversations_members(channel=location)["members"].__contains__("U07JRF405L1"):
    #         print("Not in channel, joining")
    #         client.conversations_invite(channel=location, users="U07JRF405L1")

    client.chat_postMessage(channel=location, text=message, icon_emoji=emoji, username=username)
    if location in BLACKLISTED_CHANNELS:
        client.chat_postMessage(channel=body["user"]["id"], text="Nice try")
