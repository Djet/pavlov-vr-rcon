import asyncio
import logging
from pavlov import PavlovRCON
import yaml
import time
from pathlib import Path
import prometheus_client
from prometheus_client import start_http_server,Gauge
logging.basicConfig(level=logging.DEBUG)

logging.info("Start Service")

prometheus_client.REGISTRY.unregister(prometheus_client.GC_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.PLATFORM_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.PROCESS_COLLECTOR)

conf = yaml.safe_load(Path('config.yaml').read_text())

current_players_cont = Gauge('current_players', 'Current player on server of counter', ['server_name'])

async def server_info(server):
    pavlov = PavlovRCON(
        conf['servers'][server]['host'],
        conf['servers'][server]['port'],
        conf['servers'][server]['password']
    ,timeout=20)
    info = await pavlov.send("ServerInfo",auto_close=True)
    current_players=int(info["ServerInfo"]["PlayerCount"].split("/")[0])
    current_players_cont.labels(server_name=server).set(current_players)
    logging.info("Coletct player count from " + server)

async def main():
    for server in conf['servers'].keys():
        await server_info(server)

if __name__ == '__main__':
    start_http_server(9001)
    while True:
        asyncio.run(main())
        time.sleep(50)
