# Crypto Tracker

crypto_tracker is supposed to keep track on the top 100 cryptocurrencies. Therefore, it uses the [Messari-Api](https://messari.io/api).
Executes "upsert" to update database table. Old currencies won't be deleted. Instead, the rank is set to none and active_top is set to false
The Service should be executed on regular bases through a Cronjob.