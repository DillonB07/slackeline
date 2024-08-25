# Slackeline

Slackeline is a bot for my personal channel in the Hack Club Slack, [#dillan-waffles](https://hackclub.slack.com/archives/C06R5NKVCG5). The name comes from the Madeline who is the protaganist in Celeste, my favourite game - an indie puzzle platformer.

Currently, Slackeline only welcomes people, but I plan to add more functionality to increase channel interaction! Stories, questions and mysteries are some things planned.

## Welcoming

Slackeline detects when a new user joins a channel she is in and then starts a dialogue sequence using custom avatars and names. The dialogue is reminiscent of the prologue in Celeste.

![Part of the dialogue](https://cloud-6cqevouz9-hack-club-bot.vercel.app/0image.png)
> _Part of the dialogue sequence_

I built a custom dialogue system for this so I can easily expand it using JSON (well, dictionaries but close enough).

I would like to expand on this system with buttons and trees to make dialogue more interesting.

## Setup

Create a virtual environment
```sh
python3.12 -m venv .venv
```
Activate it
```sh
source .venv/bin/activate`
```
Install packages
```sh
python3.12 -m pip install -r requirements.txt
```
Run
```sh
python3.12 main.py
```

You will also need the following environment variables for your Slack app:

```
SLACK_SIGNING_SECRET=""
SLACK_CLIENT_SECRET=""
SLACK_BOT_TOKEN=""
```

Here's an app manifest that has the necessary permissions:

```
{
    "display_information": {
        "name": "Madeline"
    },
    "features": {
        "bot_user": {
            "display_name": "Madeline",
            "always_online": false
        }
    },
    "oauth_config": {
        "scopes": {
            "bot": [
                "channels:read",
                "chat:write",
                "groups:read",
                "mpim:read",
                "users.profile:read",
                "users:read",
                "chat:write.customize"
            ]
        }
    },
    "settings": {
        "event_subscriptions": {
            "request_url": "URL",
            "bot_events": [
                "member_joined_channel"
            ]
        },
        "interactivity": {
            "is_enabled": true,
            "request_url": "URL"
        },
        "org_deploy_enabled": false,
        "socket_mode_enabled": false,
        "token_rotation_enabled": false
    }
}
```