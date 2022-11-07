
FROM debian
ENV G_ID -733102031
RUN apt-get clean && apt-get update && apt-get install -y cron python3 python3-pip vim
RUN pip3 install async-pavlov pyTelegramBotAPI sympy
RUN crontab -l | { cat; echo "* * * * * cd /apps/; python3 rcon.py -s  pavlov1.host.com -w passWOrd -p 9001 'ShowNametags False'"; } | crontab -
RUN crontab -l | { cat; echo "* * * * * cd /apps/; python3 rcon.py -s  pavlov2.host.com -w passWOrd -p 9002 'ShowNametags False'"; } | crontab -

RUN mkfifo --mode 0666 /var/log/cron.log

COPY root/ /
ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["/bin/bash", "-c", "cron && tail -f /var/log/cron.log"]
