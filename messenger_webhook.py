from helpers.crossdomain import *
from flask_restful import Resource
from flask import request
from helpers.my_util import Util
import requests
import json


class MessengerWebhook(Resource):

    method_decorators = [crossdomain(origin="*")]

    # noinspection SpellCheckingInspection
    __token = "EAAwI8GYPdjcBAIK7UK41jYOYZA0zvwrdxlQuofjXQzFVCGQLI1rxwLOC758UJ1ntx4qrbppxhTfHkLl8unZCIcgZCydS7CnpL" \
              "eWhq8ZBQmCf1KZBuS0wViuuZBZClS3QGMgBVqhjZBUdaEnDqZB8jtZCfQRc2Yzy6BBiGbuZAC6ZAIuFCAZDZD"

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

        # Send a message in response.
        self.__send_message(
            recipient_id=data_received['entry'][0]['messaging'][0]['sender']['id'],
            message="Hello!",
            responses=["Lilly", "Michelle"]
        )

        return Util.make_json_response(None, {
            "message": {
                "text": "Hello!"
            }
        }, 200)
        # return "Success", 200

    # noinspection PyMethodMayBeStatic
    def patch(self):
        pass
