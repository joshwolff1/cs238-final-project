from helpers.crossdomain import *
from flask_restful import Resource
from flask import request
from helpers.my_util import Util
from helpers.deterministic.deterministic_tree import DETERMINISTIC_TREE
import requests
import json
from helpers.my_util import AlgorithmType
from helpers.conversation import Conversation


ALGORITHM_TO_USE = AlgorithmType.SARSA


class MessengerWebhook(Resource):

    method_decorators = [crossdomain(origin="*")]

    # noinspection SpellCheckingInspection
    __token = "EAAwI8GYPdjcBAFLSpSFnqcBMhyy8XHZByHgqvq66RfWZBzDFLtqzZBnsgIAHmvXt3K4YYmMnOu0XbpRWPAti1TgUd6o29" \
              "BMyVo11TTIXfN5Ip2gx9w2h0C9eRHb6Kmw3mXOGUhVM0YsEbzZBJxuV7cadas47WZAcj6NOiGRk3pgZDZD"

    def __send_message(self, recipient_id, message, responses):

        def construct_quick_replies():
            quick_replies = list()
            for resp in responses:
                quick_replies.append({
                    "content_type": "text",
                    "title": resp,
                    "payload": "<POSTBACK_PAYLOAD>",
                })
            return quick_replies

        link = f"https://graph.facebook.com/v8.0/me/messages?access_token={self.__token}"
        body = {
            "messaging_type": "RESPONSE",
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": message,
                "quick_replies": construct_quick_replies()
            }
        }
        if len(construct_quick_replies()) == 0:
            body["message"].pop("quick_replies")
        r = requests.request(
            "POST",
            url=link,
            data=json.dumps(body),
            headers={'content-type': 'application/json'}
        )
        json_content = json.loads(r.content)
        print(json_content)

    # noinspection PyMethodMayBeStatic
    def get(self):
        data_received = Util.merge_info_and_args(request)
        mode = data_received['hub.mode']
        token = data_received['hub.verify_token']
        challenge = data_received['hub.challenge']

        print(mode, token, challenge)

        if mode == 'subscribe':
            if token == self.__token:
                return challenge, 200

        return Util.make_json_response("Error", None, 403)

    # noinspection PyMethodMayBeStatic
    def post(self):
        data_received = Util.merge_info_and_args(request)
        print("\n\n")
        print(data_received)

        try:
            message = data_received['entry'][0]['messaging'][0]['message']['text']
        except KeyError:
            return Util.make_json_response("Error", None, 403)
        print("MESSAGE!", message)
        print("a")

        if ALGORITHM_TO_USE.value == AlgorithmType.DETERMINISTIC.value:
            node = None
            for _, item in DETERMINISTIC_TREE.items():
                if item is None:
                    node = 0
                    continue
                should_break = False
                for key, reply in item.replies.items():
                    if reply == message:
                        node = key
                        should_break = True
                        break
                if should_break:
                    break

            try:
                if node is None or DETERMINISTIC_TREE[node] is None:
                    node = 0
            except KeyError:
                node = 0

            message = DETERMINISTIC_TREE[node].question
            replies = DETERMINISTIC_TREE[node].replies.values()
        else:
            conversation_node = Conversation(ALGORITHM_TO_USE).get_next_action_from_policy(reply_str=message)

            if conversation_node is None:
                return Util.make_json_response("Ok", None, 200)

            message = conversation_node.question
            replies = conversation_node.replies

        # Send a message in response.
        self.__send_message(
            recipient_id=data_received['entry'][0]['messaging'][0]['sender']['id'],
            message=message,
            responses=replies
        )

        print("Make response....")

        return Util.make_json_response(None, {
            "message": {
                "text": "Need to send something back!"
            }
        }, 200)

    # noinspection PyMethodMayBeStatic
    def patch(self):
        pass
