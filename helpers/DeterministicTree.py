from helpers.ConversationNode import ConversationNode

NO_MASK_REPLIES = {
    3: "I'm lazy.",
    4: "It's against my beliefs",
    5: "COVID-19 is a hoax",
    6: "Health problems"
}

DETERMINISTIC_TREE = {
    0: ConversationNode(
        question="Welcome! Do you wear a mask when you go out?",
        replies={
            1: "No. Masks are bad.",
            2: "Sometimes",
            99: "Yes"
        }
    ),
    1: ConversationNode(
        question="Why won’t you wear a mask?",
        replies=NO_MASK_REPLIES
    ),
    2: ConversationNode(
        question="Why don’t you wear a mask sometimes?",
        replies=NO_MASK_REPLIES
    ),
    3: ConversationNode(
        question="COVID-19 can spread easily through droplets that you and others exhale. Masks prevent the inhalation"
                 " and exhalation of droplets. This makes it less likely that you contract COVID-19 and give it to "
                 "others. Are you more likely to wear a mask now knowing this?",
        replies={
            7: "Yes",
            8: "No"
        }
    ),
    4: ConversationNode(
        question="What kind of beliefs?",
        replies={
            11: "Freedom",
            12: "It gives the government too much power."
        }
    ),
    5: ConversationNode(
        question="Over 1M have died from COVID-19. Are you sure it's a hoax?",
        replies={
            8: "Yes!",
            7: "No..."
        }
    ),
    6: ConversationNode(
        question="I'm sorry to hear that.",
        replies={
            10: "OK."
        }
    ),
    7: ConversationNode(
        question="Great! On a scale of 0-10, 10 being 100% yes, how likely are you to wear a mask now?",
        replies={
            20: "0",
            21: "1",
            22: "2",
            23: "3",
            24: "4",
            25: "5",
            26: "6",
            27: "7",
            28: "8",
            29: "9",
            30: "10"
        }
    ),
    8: ConversationNode(
        question="Fuck you.",
        replies={}
    ),
    10: None,
    11: ConversationNode(
        question="The Founding Fathers defined freedom as those God-given personal liberties that should only be "
                 "limited when the exercise of those freedoms impinges on the freedoms of others. By refusing to "
                 "wear a mask, you are impinging on others' right to live.",
        replies={
            8: "I agree.",
            7: "I disagree."
        }
    )

}
