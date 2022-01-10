# crypto_rating_extra

This repository works as an additional repository to the main [repository](https://github.com/Pondo18/crypto-rating).
It provides necessary services, which should be executed through a cronjob running on Linux server.
[Main.py](main.py) should be executed

* * *

## Deployment 
There is a [docker-compose.yml](docker-compose.yml), which creates a postgres DB necessary for the main application. 
There should be added a config.yml in root directory, having following syntax: 
```yaml
database.postgres.host: <HOST>
database.postgres.user: <USER>
database.postgres.password: <PASS>
database.postgres.database: <DATABASE>

reddit.user_agent: <REDDIT_USER_AGENT>
reddit.client_id: <REDDIT_CLIENT_ID>
reddit.client_secret: <REDDIT_CLIENT_SECRET>
```

* * *

## Services 
The repository contains multiple service, each holding a README.md on its own. 

## Sequence 

![sequence_diagram](static/images/sequence_diagram_white.png)