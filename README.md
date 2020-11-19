# Introduction
Disagreement can make conversation difficult. In today’s world, issues of importance often become incredibly polarizing. Given the pandemic, certain conversations –withanti-maskers, for example –areall the more necessary. Taking the proper precautions could prevent tens of thousandsof deaths innationwide. We seek to develop a chatbot that learns to have these difficult conversations, actively learning the best policy to convince a COVID-19 skeptic to take proper safety precautions regarding the pandemic.

# Approach
First, we created a Facebook chat using Facebook API. Then, we took three reinforcement learning algorithms: Q-learning, Sarsa and Value Iteration, and applied them on synthetic data to train the chatbot. To sample the data, we designed an algorithm that uses Multinomial distribution.

# Outcome
We found that after training, Q-Learning and Sarsa underperformed Value Iteration algorithm. This occurred due to the small size of the data set. The small size leads to Q-Learning and Sarsa producing policies that have unrewarding cycles as learning doesn’t adequately cover the state space.

# Video

https://www.youtube.com/watch?v=W9qSnNPnw2M&ab_channel=MeileeZhou

## Host server locally

1) `cd` into the repository directory
2) Start the server with `python3 application.py` in the terminal.
3) Open a new terminal window. Run `./ngrok http 5000` in the terminal. This points domains to the local server.
4) Go to <a href="https://developers.facebook.com/apps/3387528317990455/messenger/settings/">the Facebook app</a>. 
5) On Facebook: Generate new token. Paste in messenger_webhook.py and edit the URL for the webhook.

