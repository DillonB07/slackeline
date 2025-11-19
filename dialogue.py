WELCOME = [
    [
        {
            "icon_emoji": ":flyingbirb:",
            "username": "Bird",
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
                    "action_id": "end-of-welcome",
                }
            ],
        },
        {
            "icon_emoji": ":giggline:",
            "username": "Madeline",
            "messages": ["That's gonna make things a lot easier! Thanks, birdie."],
            "wait_for": "end-of-welcome",
        },
    ],[
        {
            "icon_emoji": ":neodog_floof:",
            "username": "Neodog",
            "messages": [
                "Wrrf, wrrf! wrrf, WRRF (user_mention)!! _wrrf_",
                "Wrrf! (user_mention), wrrf! Wrrf! _Wrrrrrrf!_"
            ],
        },
        {
            "icon_emoji": ":neocat_floof:",
            "username": "Neocat",
            "messages": [
                "Mrrw, mrrow, meow, mrrow",
                "meow, mrow, mrrw, mrrow",
            ]
        },
        {
            "icon_emoji": ":neodog_floof:",
            "username": "Neodog",
            "messages": [
                "Welcome to the mine (user_mention)!! _welcome_",
                "Greetings! (user_mention), welcome! _Welcome!_"
            ]
        },
        {
            "icon_emoji": ":neocat_floof:",
            "username": "Neocat",
            "messages": [
                "Another servant to the mines has arrived.",
                "Amber, gold, shining pearls, those minerals you shall mine...",
            ]
        }
    ]
]

SCHEDULED = [
    {
        "cron": "0 9 * * *",
        "sequences": [
            [
                {
                    "icon_emoji": ":flyingbirb:",
                    "username": "Bird",
                    "messages": [
                        "_*SQUAWK SQUAWK* Good morning everyone!_",
                    ],
                },
                {
                    "icon_emoji": ":shockedeline:",
                    "username": "Madeline",
                    "messages": [
                        "_yawhnnn_ wahtt time is it??!\nwait... how is it morning already :sleepybirb:"
                    ],
                },
            ]
        ],
    },
    {
        "cron": "30 7 * * 1",
        "sequences": [
            [
                {
                    "icon_emoji": ":celeste-mom-normal00:",
                    "username": "Mum",
                    "messages": [
                        "Amber, be sure to ask your friends a question to _make some new pals_!",
                    ],
                }
            ],
            [
                {
                    "icon_emoji": ":celeste-mom-normal01:",
                    "username": "Mum",
                    "messages": [
                        "Amber, do you know what time it is? It's *question-asking time*!",
                    ],
                }
            ],
        ],
    },
    {
        "cron": "30 21 * * *",
        "sequences": [
            [
                {
                    "icon_emoji": ":distracteline:",
                    "username": "Madeline",
                    "messages": [
                        "Hey Amber.... what have you been up to today?"
                    ],
                }
            ],
            [
                {
                    "icon_emoji": ":unimpressedbirb:",
                    "username": "Bird",
                    "messages": [
                        "_*SQUAWK SQUAWK* it's time for your daily breakdown, Amber_",
                    ],
                }
            ],
        ],
    },
    {
         "cron": "0 10 25 12 *",
         "sequences": [
             [
                 {
                        "icon_emoji": ":flyingbirb:",
                        "username": "Bird",
                        "messages": [
                            "_*SQUAWK SQUAWK*_ Merry Christmas everyone!",
                        ],
                    },
                    {
                        "icon_emoji": ":celeste-madeline-peaceful00:",
                        "username": "Madeline",
                        "messages": [
                            "Merry Christmas, Amber!"
                        ],
                 }
             ],
             [
                 {
                     "icon_emoji": ":neocat_santa:",
                        "username": "Neocat",
                        "messages": [
                            "Merry Christmas, Amber! :3"
                        ],
                 },
                    {
                        "icon_emoji": ":neodog_santa:",
                            "username": "Neodog",
                            "messages": [
                                "_Wrrf, wrrf!_ Merry Christmas, Amber! :3"
                            ],
                    }
             ],
             [{
                 "icon_emoji": ":neodog_santa:",
                    "username": "Neodog",
                    "messages": [
                        "_Wrrf, wrrf!_ Merry Christmas, Amber! :3"
                    ],
             },
                {
                    "icon_emoji": ":neocat_santa:",
                        "username": "Neocat",
                        "messages": [
                            "Merry Christmas, Amber! >:3"
                        ],
                }
             ]
         ]
    },
    {
         "cron": "0 10 22 4 *",
         "sequences": [
             [
                 {
                        "icon_emoji": ":flyingbirb:",
                        "username": "Bird",
                        "messages": [
                            "_*SQUAWK SQUAWK SQUAWK*_ Happy Slackversary Amber!",
                        ],
                    },
                    {
                        "icon_emoji": ":celeste-madeline-peaceful00:",
                        "username": "Madeline",
                        "messages": [
                            "Woo, congrats! :D"
                        ],
                 }
             ],
             [
                 {
                     "icon_emoji": ":neocat_happy:",
                        "username": "Neocat",
                        "messages": [
                            "OH MY GOD IT'S YOUR SLACKVERSARY, CONGRATULATIONS AMBER!!!!!!!!"
                        ],
                 },
                    {
                        "icon_emoji": ":neodog_happy:",
                            "username": "Neodog",
                            "messages": [
                                "wow, another year on slack... it really does not feel like that long"
                            ],
                    }
             ],
             [{
                 "icon_emoji": ":neodog_happy:",
                    "username": "Neodog",
                    "messages": [
                        "_wow, amber! i can't believe it's been another year since you join the slack already"
                    ],
             },
                {
                    "icon_emoji": ":neocat_happy:",
                        "username": "Neocat",
                        "messages": [
                            "WAIT WHAT?! IT'S HER SLACKVERSARY?!!! OMG OMG CONGRATS AMBER!!!!!"
                        ],
                }
             ]
         ]
    }

]
