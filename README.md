# GPfingstrose

## Configuration

The application is reading its configuration from environment variables:

```shell
export PFINGSTROSE_CONSUMER_KEY=<youneedthis>
export PFINGSTROSE_CONSUMER_SECRET=<youneedthis>
export PFINGSTROSE_ACCESS_TOKEN=<youneedthis>
export PFINGSTROSE_ACCESS_TOKEN_SECRET=<youneedthis>
```

... or use an `.env` file, it will be evaluated by pipenv.

## Run the bot

`./app.py`

### Sentiment Analysis

If you set `GOOGLE_APPLICATION_CREDENTIALS`to some service account JSON file path (see https://cloud.google.com/docs/authentication/getting-started for details), the bot will do a sentiment analysis of each incoming tweet.
