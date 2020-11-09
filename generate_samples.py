import pandas as pd
from random import randint
import numpy as np
from collections import defaultdict
import csv


class SampleGeneration:

    __MIN_INDEX = 0
    __MAX_INDEX = 40

    __ACHIEVEMENT_STATE = 16
    __DEATH_STATE = 17

    # Maps (s, a) to (sp) probabilities dict
    __probabilities = defaultdict(dict)
    __samples = list()

    def __init__(self):
        self.data = pd.read_csv("tree/tree.csv")
        self.states = self.data["s"]
        self.actions = self.data["a"]
        self.rewards = self.data["r"]
        self.state_primes = self.data["sp"]

    def generate_samples(self, n):
        self.__samples = list()
        for _ in range(n):
            self.__generate_random_sample()
        self.__write_samples_to_file()

    def __generate_random_sample(self):
        """

        :return:
        """
        state_action_index = randint(self.__MIN_INDEX, self.__MAX_INDEX)

        # Choose a state
        states_possible = SampleGeneration.parse_ranges(self.states[state_action_index])
        state = np.random.choice(states_possible)

        # Choose an action
        actions_possible = SampleGeneration.parse_ranges(self.actions[state_action_index])
        action = np.random.choice(actions_possible)

        # Generate a state prime
        if len(self.__probabilities[(state, action)].keys()) == 0:
            state_primes_possible = SampleGeneration.parse_ranges(self.state_primes[state_action_index])
            # We have not defined the probability distribution yet
            self.__probabilities[(state, action)] = SampleGeneration.get_state_prime_probabilities(
                state_primes_possible
            )
        state_prime = SampleGeneration.multinomial_sample(self.__probabilities[(state, action)])

        # Determine reward
        if state_prime == self.__ACHIEVEMENT_STATE:
            reward = 100
        elif state_prime == self.__DEATH_STATE:
            reward = -100
        else:
            reward = 0

        # Add the sample
        sample = [state, action, reward, state_prime]
        self.__samples.append(sample)

    def __write_samples_to_file(self):
        with open('samples-2.csv', 'w', newline='') as csv_file:
            spam_writer = csv.writer(
                csv_file,
                delimiter=',',
                quotechar='|',
                quoting=csv.QUOTE_MINIMAL
            )
            spam_writer.writerow(["s", "a", "r", "sp"])
            for sample in self.__samples:
                spam_writer.writerow(sample)

    @staticmethod
    def get_state_prime_probabilities(state_prime_list):
        state_prime_probabilities = dict()
        for state_prime in state_prime_list:
            state_prime_probabilities[state_prime] = randint(1, 100)
        normalization_term = np.sum(list(state_prime_probabilities.values()))
        for state_prime in state_prime_list:
            state_prime_probabilities[state_prime] /= normalization_term
        return state_prime_probabilities

    @staticmethod
    def multinomial_sample(probabilities_dict):
        """

        :param probabilities_dict:
        :return:
        """

        # Sort the state primes and probabilities in order to randomly select one based on the multinomial distribution
        state_primes = list(probabilities_dict.keys())
        state_prime_probabilities = list(probabilities_dict.values())

        state_primes_sorted = list()
        state_prime_probabilities_sorted = list(state_prime_probabilities)
        state_prime_probabilities_sorted.sort()

        indices_chosen = list()
        for spp_s in state_prime_probabilities_sorted:
            current_index = 0
            for spp in state_prime_probabilities:
                if current_index in indices_chosen:
                    current_index += 1
                    continue
                if round(spp, 3) == round(spp_s, 3):
                    indices_chosen.append(current_index)
                    state_primes_sorted.append(state_primes[current_index])
                    break
                current_index += 1

        # Select the state prime
        random_value = np.random.uniform(0, 1)
        current_index = 0
        last_prob = None

        cum_state_prime_probabilities_sorted = list()
        for i in range(len(state_prime_probabilities_sorted)):
            cum_state_prime_probabilities_sorted.append(np.sum(state_prime_probabilities_sorted[:i + 1]))

        for prob in cum_state_prime_probabilities_sorted:

            if last_prob is None and random_value <= prob:
                return state_primes_sorted[current_index]
            elif last_prob is not None and last_prob <= random_value <= prob:
                return state_primes_sorted[current_index]

            last_prob = prob
            current_index += 1

    @staticmethod
    def parse_ranges(range_str):
        """
        Parses the ranges in the document (e.g. 48-50 to [48,49,50] and 48,49,50 to [48,49,50])
        :return: A list of numbers in the input range string
        """
        if "-" in range_str:
            return list(range(int(range_str.split("-")[0]), int(range_str.split("-")[1])))
        elif "," in range_str:
            number_list = list()
            str_number_list = range_str.split(',')
            for item in str_number_list:
                number_list.append(int(item))
            return number_list
        else:
            try:
                return [int(range_str)]
            except ValueError as e:
                print(range_str)
                raise(Exception(e))

    @staticmethod
    def generate_multinomial_distribution(n):
        """

        :param n:
        :return:
        """
        probabilities = list()
        for i in range(n):
            probabilities.append(randint(1, 10))
        probabilities = np.array(probabilities)
        probabilities /= np.sum(probabilities)
        return probabilities


def main():
    sample_generation_instance = SampleGeneration()
    sample_generation_instance.generate_samples(n=10000)


if __name__ == '__main__':
    main()
