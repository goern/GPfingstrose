# twitter tensorflow serving bot
This twitter bot, when mentioned in a tweet, looks for an attached image and sends that attached image to a tensorflow model serving endpoint (REST API).
It then replies to the original tweet with the response received from the tensorflow model.

## Configuration

The application is reading its configuration from environment variables:

```shell
export TWITTER_CONSUMER_KEY=<youneedthis>
export TWITTER_CONSUMER_SECRET=<youneedthis>
export TWITTER_ACCESS_TOKEN=<youneedthis>
export TWITTER_ACCESS_TOKEN_SECRET=<youneedthis>
export TF_SERVER_URL=<youneedthis>
```

... or use an `.env` file, it will be evaluated by pipenv.

`TF_SERVER_URL` is the url for the tensorfow model serving REST API endpoint. (Example: `http://127.0.0.1:8401/v1/models/saved_model:predict`)

## Run the bot

`./app.py`
