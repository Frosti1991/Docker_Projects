# Docker_Projects

Twitter-Bot-Pipeline
docker compose pipeline:

- collecting tweets via the twitter API on a given hashtag
- storing tweets in a MongoDB
- ETL job 
  - Extract from MongoDB
  - Transform: Regular Expression, evaluation of sentiment score per tweet
  - Load: into a docker postgres db

- Slackbot which posts tweets to a specific Slack channel
- additionally postgresdb is connected to local Metabase to visualize sentiment score results

Tools:
Docker
MongoDB
PostgreSQL
API
Slackbot
Metabase
