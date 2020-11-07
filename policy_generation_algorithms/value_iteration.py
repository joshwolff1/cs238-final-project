from collections import defaultdict
from helpers.my_util import Algorithm, AlgorithmType
import pandas as pd


class MLEAndAsyncValueIteration(Algorithm):

    k_max = 1000
    __neg_inf = -1e6

    def __init__(self, gamma):
        super().__init__(AlgorithmType.VALUE_ITERATION)
        self.gamma = gamma

        self.data = pd.read_csv("samples.csv")

        self.states = self.data["s"]
        self.actions = self.data["a"]
        self.rewards = self.data["r"]
        self.state_primes = self.data["sp"]

        self.n_samples = len(self.states)

        self.n_actions = len(set(self.actions))
        self.t = defaultdict(dict)
        self.r = defaultdict(dict)
        self.q = defaultdict(dict)

        self.initialize_reward_and_transition()

    def initialize_reward_and_transition(self):
        state_action_counts = defaultdict(dict)
        for i in range(self.n_samples):

            action = self.actions[i]

            if self.t[self.states[i]].get(action, None) is None:
                self.t[self.states[i]][action] = {
                    self.state_primes[i]: 1
                }
            else:
                self.t[self.states[i]][action][self.state_primes[i]] = \
                    1 + self.t[self.states[i]][action].get(self.state_primes[i], 0)

            self.r[self.states[i]][action] = self.rewards[i] + self.r[self.states[i]].get(action, 0)
            state_action_counts[self.states[i]][action] = 1 + state_action_counts[self.states[i]].get(action, 0)

        did_add = defaultdict(dict)

        for i in range(len(self.states)):
            action = self.actions[i]

            if did_add[self.states[i]].get(action, None) is None:
                did_add[self.states[i]][action] = dict()
            if self.state_primes[i] in did_add[self.states[i]][action].keys():
                continue
            # noinspection PyTypeChecker
            did_add[self.states[i]][action][self.state_primes[i]] = True

            self.t[self.states[i]][action][self.state_primes[i]] /= \
                state_action_counts[self.states[i]][action]

            self.r[self.states[i]][action] /= state_action_counts[self.states[i]][action]

        for key, value in self.t.items():
            print(key, value)

    def train(self):

        print(self.t)

        states = list(set(self.states))
        states.sort()

        actions = list(set(self.actions))

        print(actions)

        for k in range(self.k_max):

            for s in states:

                for a in actions:
                    update_score = 0

                    s_primes = self.t[s].get(a, None)

                    if s_primes is not None:
                        for s_prime in s_primes:
                            action_values = list(self.q[s_prime].values())
                            if len(action_values) == 0:
                                break
                            # noinspection PyTypeChecker
                            update_score += float(self.t[s][a][s_prime]) * max(action_values)
                    else:
                        continue

                    new_q_value = self.r[s].get(a, 0) + self.gamma * update_score
                    self.q[s][a] = new_q_value
