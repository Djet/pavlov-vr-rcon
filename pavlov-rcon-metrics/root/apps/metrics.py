
import asyncio
from pavlov import PavlovRCON
import logging
import yaml
import time
from pathlib import Path
import prometheus_client
from prometheus_client import start_http_server,Gauge


async def players_info(pavlov):
    RefreshList = await pavlov.send("RefreshList")
    players_list=[]
    for player in RefreshList["PlayerList"]:
        player_info = await pavlov.send("InspectPlayer " + player["UniqueId"])
        UniqueId = player_info["PlayerInfo"]["UniqueId"]
        Kill = player_info["PlayerInfo"]["KDA"].split("/")[0]
        Dead = player_info["PlayerInfo"]["KDA"].split("/")[1]
        Assists = player_info["PlayerInfo"]["KDA"].split("/")[2]
        Score = player_info["PlayerInfo"]["Score"]
        players_list.append({
          "UniqueId":UniqueId,
          "Kill":Kill,
          "Dead":Dead,
          "Assists":Assists,
          "Score":Score
        })
    return players_list

async def get_server_info(pavlov):
    ServerInfo = await pavlov.send("ServerInfo")
    return {
    "MapLabel":ServerInfo["ServerInfo"]["MapLabel"],
    "GameMode":ServerInfo["ServerInfo"]["GameMode"],
    "ServerName":ServerInfo["ServerInfo"]["ServerName"],
    "PlayerCount":ServerInfo["ServerInfo"]["PlayerCount"].split("/")[0],
    "Players":await players_info(pavlov)
    }

async def main():
    logging.info("Start Service")
    conf = yaml.safe_load(Path('config.yaml').read_text())

    for server in conf['servers'].keys():
        pavlov = PavlovRCON(
            conf['servers'][server]['host'],
            conf['servers'][server]['port'],
            conf['servers'][server]['password'])
        server_info = await get_server_info(pavlov)
        server_statistic_cont.labels(
            server_name=server,
            MapLabel=server_info['MapLabel'],
            GameMode=server_info['GameMode']
            ).set(server_info['PlayerCount'])
        for player in server_info['Players']:
            player_statistic_kill.labels(
                server_name=server,
                MapLabel=server_info['MapLabel'],
                GameMode=server_info['GameMode'],
                UniqueId=player['UniqueId']
                ).set(player['Kill'])
            player_statistic_dead.labels(
                server_name=server,
                MapLabel=server_info['MapLabel'],
                GameMode=server_info['GameMode'],
                UniqueId=player['UniqueId']
                ).set(player['Dead'])
            player_statistic_assists.labels(
                server_name=server,
                MapLabel=server_info['MapLabel'],
                GameMode=server_info['GameMode'],
                UniqueId=player['UniqueId']
                ).set(player['Assists'])
            player_statistic_score.labels(
                server_name=server,
                MapLabel=server_info['MapLabel'],
                GameMode=server_info['GameMode'],
                UniqueId=player['UniqueId']
                ).set(player['Score'])
        print(await get_server_info(pavlov))



if __name__ == '__main__':
    server_statistic_cont = Gauge(
        'server_statistic',
        'Server player statistics',
        ['server_name','MapLabel','GameMode'])
    player_statistic_kill = Gauge(
        'player_kills',
        'Player Kills statistics',
        ['server_name','MapLabel','GameMode','UniqueId'])
    player_statistic_dead = Gauge(
        'player_dead',
        'Player dead statistics',
        ['server_name','MapLabel','GameMode','UniqueId'])
    player_statistic_assists = Gauge(
        'player_assists',
        'Player assists statistics',
        ['server_name','MapLabel','GameMode','UniqueId'])
    player_statistic_score = Gauge(
        'player_score',
        'Player score statistics',
        ['server_name','MapLabel','GameMode','UniqueId'])
    start_http_server(9001)
    while True:
        asyncio.run(main())
        time.sleep(50)
