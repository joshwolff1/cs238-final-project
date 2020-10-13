from helpers.crossdomain import *
from flask_restful import Resource
from flask import request
from helpers.my_util import Util
from pymessenger.bot import Bot
import requests
import json


class MessengerWebhook(Resource):

    method_decorators = [crossdomain(origin="*")]

    # noinspection SpellCheckingInspection
    __token = "EAAwI8GYPdjcBAIK7UK41jYOYZA0zvwrdxlQuofjXQzFVCGQLI1rxwLOC758UJ1ntx4qrbppxhTfHkLl8unZCIcgZCydS7CnpL" \
              "eWhq8ZBQmCf1KZBuS0wViuuZBZClS3QGMgBVqhjZBUdaEnDqZB8jtZCfQRc2Yzy6BBiGbuZAC6ZAIuFCAZDZD"

    def __send_test_message(self):
        #
        # bot = Bot(self.__token)
        # response = bot.send_text_message("3387111534710086", "hello, world!")
        # print(response)
        link = f"https://graph.facebook.com/v8.0/me/messages?access_token={self.__token}"
        body = {
            "messaging_type": "Text",
            "recipient": {
                "id": "3387111534710086"
            },
            "message": {
                "text": "hello, world!"
            }
        }
        r = requests.request(
            "POST",
            url=link,
            data=json.dumps(body)
        )
        json_content = json.loads(r.content)
        print("-----")
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

        # TODO:- Send the message in response.

        """
        message:{
            text: 'I have an issue with an order'
            mid: '<MID>'
            reply_to: {
                mid: '<MID_OF_MESSAGE_BEING_REPLIED_TO>',
            }
        }
        """

        self.__send_test_message()

        return Util.make_json_response(None, {
            "message": {
                "text": "Hello!"
            }
        }, 200)
        # return "Success", 200

    # noinspection PyMethodMayBeStatic
    def patch(self):
        pass
