# Echo Bot powered by [Roman](https://github.com/dkovacevic/roman)
![Publish Docker Image](https://github.com/wireapp/echo-bot-roman/workflows/Publish%20Docker%20Image/badge.svg)

Echo Bot implementation that uses [Roman](https://github.com/dkovacevic/roman) to communicate with [Wire](https://wire.com/en/) backend.
Echo Bot that directly uses [lithium](https://github.com/wireapp/lithium) can be found [here](https://github.com/wireapp/echo-bot). 

## Deployment and runtime
The Echo Bot is deployed to docker hub as `lukaswire/echo-bot-roman`. 
To run the instance one needs to set following env variables:
```bash
# URL of roman
ROMAN_URL=http://proxy.services.zinfra.io
# Bearer token which is send by Roman to the bot
ROMAN_TOKEN=<token> 
```
