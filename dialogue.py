WELCOME = [
    [
        {
            "icon_emoji": ":flyingbirb:",
            "username": "Bird",
            "message": "_*SQUAWK SQUAWK* (user_mention) has started the trail_",
            "messages": [
                "_*SQUAWK SQUAWK* (user_mention) has started the trail_",
                "_*CAWH, CAWH* (user_mention) approaches the trail_",
                "_*SQWAAAWK* Hungrily wanting waffles, (user_mention) walks up to the trail, not knowing what to expect_",
            ],
        },
        {
            "icon_emoji": ":distracteline:",
            "username": "Madeline",
            "messages": [
                "Excuse me, ma'am\nThe sign out front is busted... is this the trail to the _:sparkles:waffle house:sparkles:_?",
                "Ma'am, the sign out front is busted... am I near the _:sparkles:waffle house:sparkles:_?",
            ],
        },
        {
            "icon_emoji": ":grannycreep:",
            "username": "Old Lady",
            "messages": [
                "_You're almost there, (pronouns). It's just across the bridge._",
                "_You're nearly there, (pronouns). It's just over the bridge._",
                "_The _:sparkles:waffle house:sparkles:_ is just over the bridge (pronouns)_",
            ],
            "replacements": [
                {"replace": "she", "with": "miss"},
                {"replace": "they", "with": "strange person", "default": True},
                {"replace": "he", "with": "mister"},
            ],
        },
        {
            "icon_emoji": ":scaredeline:",
            "username": "Madeline",
            "messages": [
                "By the way, you should call someone about your driveway. The ridge collapsed and I nearly died."
            ],
        },
        {
            "icon_emoji": ":grannylaughing:",
            "username": "Old Lady",
            "messages": [
                '_If my "driveway" almost did you in, the trail might be a bit much for you._'
            ],
        },
        {
            "icon_emoji": ":madeline:",
            "username": "Madeline",
            "messages": [
                "Well, if an old thing like _you_ can survive out here, I think I'll be fine."
            ],
        },
        {
            "icon_emoji": ":grannycreep:",
            "username": "Old Lady",
            "messages": ["_Suit yourself._"],
            "delay": 1,
        },
        {
            "icon_emoji": ":grannycreep:",
            "username": "Old Lady",
            "messages": [
                "_But you should know, you'll find more than :sparkles:waffles:sparkles: at the end of this trail._"
            ],
            "delay": 1,
        },
        {
            "icon_emoji": ":grannycreep:",
            "username": "Old Lady",
            "messages": ["_This is a strange place._"],
            "delay": 1,
        },
        {
            "icon_emoji": ":grannycreep:",
            "username": "Old Lady",
            "messages": ["_You might see things._"],
            "delay": 1,
        },
        {
            "icon_emoji": ":grannylaugh:",
            "username": "Old Lady",
            "messages": ["_Things you ain't ready to see._"],
            "delay": 2,
        },
        {
            "icon_emoji": ":sadeline:",
            "username": "Madeline",
            "messages": ["You should seek help, lady."],
            "delay": 0.4,
        },
        {
            "icon_emoji": ":grannylaughing:",
            "username": "Old Lady",
            "messages": [
                "\n",
                "Hahahahahahahahahahahahahahahahahahahaha",
                "Haha, I suppose I'm in the right place..",
            ],
        },
        {
            "icon_emoji": ":unimpressedbirb:",
            "username": "Bird",
            "messages": [
                "_*SQUAWK*_",
                "_*CACAWHR*_",
            ],
            "buttons": [
                {
                    "text": "Dash",
                    "type": "wait",
                    "action_id": "end-of-welcome"
                }
            ],
        },
        {
            "icon_emoji": ":flyingbirb:",
            "username": "Bird",
            "messages": [
                "Meow :3"
            ],
            "wait_for": "end-of-welcome"
        }
    ]
]
