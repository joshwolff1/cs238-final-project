# cs238-final-project

Disagreement can make conversation difficult. In today’s world, issues of importance often become incredibly polarizing. Given the pandemic, certain conversations –withanti-maskers, for example –areall the more necessary. Taking the proper precautions could prevent tens of thousandsof deaths innationwide.We seek to develop achatbot that learns to have these difficult conversations, actively learning the best policy to convince a COVID-19 skeptic to take proper safety precautions regarding the pandemic.

## Host server locally

1) `cd` into the repository directory
2) Start the server with `python3 application.py` in the terminal.
3) Open a new terminal window. Run `./ngrok http 5000` in the terminal. This points domains to the local server.
4) Go to <a href="https://developers.facebook.com/apps/3387528317990455/messenger/settings/">the Facebook app</a>. 
5) On Facebook: Generate new token. Paste in messenger_webhook.py and edit the URL for the webhook.

