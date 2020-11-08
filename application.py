from flask import Flask
from flask_restful import Api
from helpers.crossdomain import *
from messenger_webhook import MessengerWebhook

application = Flask(__name__, template_folder='template', static_url_path='/static')
application.config.from_object(__name__)
application.config['SECRET_KEY'] = '1ex13eu103me91i-sdf'
application.url_map.strict_slashes = False
api = Api(application, decorators=[crossdomain(origin="*")])

api.add_resource(
    MessengerWebhook,
    f'/messenger-webhook',
    endpoint=f'/messenger-webhook'
)


def main():
    pass


main()


if __name__ == "__main__":

    print("------------------- Local Application Start ---------------------")
    application.run(host='0.0.0.0', debug=True)
