import pandas as pd
from helpers.conversation import Conversation
from helpers.my_util import AlgorithmType


if __name__ == '__main__':
    data = pd.read_csv("policy_generation_algorithms/unseen-samples.csv")

    n_samples = 10000

    sum_reward = 0
    for i in range(n_samples):
        reward = data['r'][i]
        if reward == 0:
            continue

        state = data['s'][i]

        correct_action = data['a'][i]

        policy_action = Conversation(AlgorithmType.VALUE_ITERATION).get_action_integer(int(state))

        if policy_action == correct_action:
            sum_reward += reward

    print("Sum Reward", sum_reward)
