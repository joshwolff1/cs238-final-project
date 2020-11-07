
class ConversationNode:

    def __init__(self, question, replies):
        self.question = question
        self.replies = replies

        assert type(replies) == dict
        assert type(question) == str
