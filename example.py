# start example.exs, then
# python example.py

import asyncio
import logging
import sys
from asyncio import sleep

from term import Atom
from pyrlang.node import Node
from pyrlang.process import Process

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z")
LOG = logging.getLogger()

class MyProcess(Process):
    def __init__(self) -> None:
        self.count = 0
        Process.__init__(self)
        self.get_node().register_name(self, Atom('my_process'))
        LOG.info("Registering process - 'my_process'")

    def handle_one_inbox_message(self, msg):
        LOG.info("Incoming %s", msg)
        self.get_node().send_nowait(sender=self.pid_,
                  receiver=(Atom('erl@127.0.0.1'), Atom('hello')),
                  message=(Atom('hello_from_python'),self.pid_, self.count))
        self.count = self.count + 1


async def main():
    LOG.info("starting the python node")
    n = Node(node_name="py@127.0.0.1", cookie="COOKIE")

    MyProcess()
    await sleep(20)
    LOG.info("stopped the python node")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
