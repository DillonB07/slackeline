def generate_home_view(client, event, logger):
    view = {
	"type": "home",
	"blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": ":celeste-madeline-normal04: Slackeline's Dashboard :celeste-madeline-normal04:",
				"emoji": True
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f":waveline: Hiii <@{event['user']}>! What would you like me to do?"
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": ":celeste-madelineph-normal05: Make a call",
				"emoji": True
			}
		},
		{
			"type": "input",
			"block_id": "username",
			"element": {
				"type": "plain_text_input",
				"action_id": "username"
			},
			"label": {
				"type": "plain_text",
				"text": "Should I pretend to be someone else?",
				"emoji": True
			}
		},
		{
			"type": "input",
			"block_id": "emoji",
			"element": {
				"type": "plain_text_input",
				"action_id": "emoji"
			},
			"label": {
				"type": "plain_text",
				"text": "What should I look like?",
				"emoji": True
			}
		},
		{
			"type": "input",
			"block_id": "message_input",
			"element": {
				"type": "plain_text_input",
				"multiline": True,
				"action_id": "message_input"
			},
			"label": {
				"type": "plain_text",
				"text": "Call to make",
				"emoji": True
			}
		},
		{
			"type": "input",
			"block_id": "conversations_select",
			"element": {
				"type": "conversations_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select conversation",
					"emoji": True
				},
				"action_id": "conversations_select-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Who should I call?",
				"emoji": True
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Make the call",
						"emoji": True
					},
					"style": "primary",
					"action_id": "submit_phone_call"
				}
			]
		}
	]
    }
    client.views_publish(user_id=event['user'], view=view)
