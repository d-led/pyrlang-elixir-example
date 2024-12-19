import asyncio
import logging
import sys
import os
from asyncio import sleep

from term import Atom
from pyrlang.node import Node
from pyrlang.process import Process

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s [%(name)s]: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z")
LOG = logging.getLogger()

class MyProcess(Process):
    def __init__(self) -> None:
        self.count = 0
        self.erlang_node = os.getenv("ERLANG_NODE", 'erl@127.0.0.1')
        LOG.info(f"ERLANG_NODE={self.erlang_node}")
        Process.__init__(self)
        self.get_node().register_name(self, Atom('my_process'))
        LOG.info("Registering process - 'my_process'")

    def handle_one_inbox_message(self, msg):
        LOG.info("Incoming %s", msg)
        self.get_node().send_nowait(sender=self.pid_,
                  receiver=(Atom(self.erlang_node), Atom('hello')),
                  message=(Atom('hello_from_python'),self.pid_, self.count))
        self.count = self.count + 1


async def main():
    LOG.info("starting the python node")
    my_node = os.getenv("MY_NODE", "py@127.0.0.1")
    LOG.info(f"MY_NODE={my_node}")
    n = Node(node_name=my_node, cookie="COOKIE")

    # reduce low-level logging
    logging.getLogger("pyrlang.dist_proto.base_dist_protocol").setLevel(logging.CRITICAL)
    logging.getLogger("pyrlang.node").setLevel(logging.CRITICAL)

    MyProcess()
    await sleep(20)
    LOG.info("stopped the python node")


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
