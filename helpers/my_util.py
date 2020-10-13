from flask import jsonify
import jsonpickle
import json
from urllib.parse import unquote_plus


class Util:

    # noinspection SpellCheckingInspection
    @staticmethod
    def make_json_response(message_to_send, dict_to_send, status_code=200):
        assert message_to_send is not None or dict_to_send is not None
        assert message_to_send is None or dict_to_send is None
        if message_to_send is not None:
            jsonified_dict = jsonify({
                "data": [
                    {
                        "message": message_to_send
                    }
                ]
            })
        else:
            jsonified_dict = jsonify(dict_to_send)
        jsonified_dict.status_code = status_code
        print(jsonified_dict)
        return jsonified_dict

    @staticmethod
    def merge_info_and_args(request_returned, should_read_data_stream=True, read_data=None):

        data = None
        if should_read_data_stream:
            try:
                raw_data_str = request_returned.stream.read()
                if read_data is not None:
                    raw_data_str = read_data
                data = raw_data_str.decode("utf-8").strip()
            except UnicodeDecodeError:
                pass

        if data is not None:
            try:
                request_data = jsonpickle.decode(data)
            except json.decoder.JSONDecodeError:
                key_value_pairs = data.split("&")
                payload = {}
                for pair in key_value_pairs:
                    if "=" in pair:
                        key, value = pair.split("=")
                        payload[key] = unquote_plus(value)
                request_data = dict(payload)
        else:
            request_data = {}

        # noinspection PyBroadException
        try:
            request_form = dict(request_returned.form)

            request_form_data = dict()
            for key in request_form.keys():
                request_form_data[key] = request_form[key]

        except Exception:
            request_form_data = dict()

        request_args = request_returned.args
        final_dict = {}
        for key in request_data.keys():
            final_dict[key] = request_data[key]
        for key in request_args.keys():
            final_dict[key] = request_args[key]
        for key in request_form_data.keys():
            final_dict[key] = request_form_data[key]
        return final_dict
