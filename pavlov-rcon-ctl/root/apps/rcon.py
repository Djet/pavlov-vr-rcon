import argparse
import asyncio
import json
from pavlov import PavlovRCON
parser = argparse.ArgumentParser(description="Rcon script")

parser.add_argument("-s", dest="server_host", required=True)
parser.add_argument("-w", dest="password", required=True)
parser.add_argument("-p", dest="port", required=True)
parser.add_argument("command")

args = parser.parse_args()

pavlov = PavlovRCON(args.server_host, args.port, args.password)

async def main():

 result = await pavlov.send(args.command)
 print(json.dumps(result))
asyncio.run(main())
