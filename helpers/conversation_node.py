
class ConversationNode:

    def __init__(self, question, replies):
        self.question = question
        self.replies = replies

        assert type(replies) == dict or type(replies) == list
        assert type(question) == str
