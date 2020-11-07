from policy_generation_algorithms.value_iteration import MLEAndAsyncValueIteration

if __name__ == '__main__':
    val_it_instance = MLEAndAsyncValueIteration(gamma=0.9)
    val_it_instance.initialize_reward_and_transition()
    val_it_instance.train()
    val_it_instance.get_policy()
