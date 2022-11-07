
FROM debian:11
RUN apt-get clean && apt-get update && apt-get install -y python3 python3-pip vim
RUN pip3 install async-pavlov pyTelegramBotAPI sympy aiohttp pyyaml
COPY root/ /
CMD ["/docker-entrypoint.sh"]
