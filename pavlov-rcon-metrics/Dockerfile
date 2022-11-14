
FROM debian
ENV G_ID -733708031
RUN apt-get clean && apt-get update && apt-get install -y cron python3 python3-pip vim
RUN pip3 install async-pavlov pyTelegramBotAPI sympy prometheus-client sympy aiohttp pyyaml

COPY root/ /
WORKDIR /apps
CMD ["/docker-entrypoint.sh"]
