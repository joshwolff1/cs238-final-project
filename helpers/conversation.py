import pandas as pd
from helpers.my_util import AlgorithmType
from helpers.conversation_node import ConversationNode
from generate_samples import SampleGeneration


class Conversation:

    START_STR = "START"
    END_STR = "END"

    def __init__(self, algorithm_type):

        action_csv = pd.read_csv(f'tree/action-keys.csv')
        state_csv = pd.read_csv(f'tree/state-keys.csv')
        policy_csv = pd.read_csv(f'policy_generation_algorithms/policies/{algorithm_type.value.lower()}.policy')

        self.action_dict = dict(zip(action_csv["a#"],  action_csv["aval"]))
        self.state_dict = dict(zip(state_csv["s#"],  state_csv["sval"]))
        self.sp_to_action_dict = dict(zip(state_csv["s#"], policy_csv["p"]))

        self.__get_action_sp_indices_dict()

        print(self.action_dict)
        print(self.state_dict)
        print(self.sp_to_action_dict)

    def __get_action_sp_indices_dict(self):
        tree_csv = pd.read_csv(f'tree/tree.csv')

        self.action_to_sp_indices_dict = dict()
        for i in range(len(tree_csv['a'])):
            actions = SampleGeneration.parse_ranges(tree_csv['a'][i])
            states_prime = SampleGeneration.parse_ranges(tree_csv['sp'][i])

            for action in actions:
                self.action_to_sp_indices_dict[action] = states_prime

    @staticmethod
    def __get_state_prime_from_reply(reply_str):
        """
        Formatted like:

        Good (1)

        Where sp = 1
        :return: The state prime contained in the reply
        """
        try:
            return int(reply_str.split('(')[1].split(')')[0])
        except IndexError:
            return None
        except ValueError:
            return None
        except TypeError:
            return None

    def get_action_integer(self, state_prime_int):
        return self.sp_to_action_dict[state_prime_int]

    def get_next_action_from_policy(self, reply_str):
        """

        :param reply_str: The reply sent by the user
        :return:
        """
        state_prime_int = self.__get_state_prime_from_reply(reply_str)
        if state_prime_int is None:
            state_prime_int = 0
        if state_prime_int == 110:
            return None

        try:
            reply_indices = self.action_to_sp_indices_dict[self.sp_to_action_dict[state_prime_int]]
            user_replies = list()
            for reply_index in reply_indices:
                user_replies.append(f"{self.state_dict[reply_index]} ({reply_index})")

            bot_reply = self.action_dict[self.sp_to_action_dict[state_prime_int]]

            conversation_node = ConversationNode(
                bot_reply,
                user_replies
            )
        except Exception as e:
            print(str(e))
            return None

        return conversation_node


if __name__ == '__main__':
    Conversation(AlgorithmType.VALUE_ITERATION)
