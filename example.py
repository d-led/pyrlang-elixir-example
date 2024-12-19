import asyncio
import logging
import sys
import os
from asyncio import sleep

from term import Atom
from pyrlang.node import Node
from pyrlang.process import Process

LOG = logging.getLogger()
my_node = os.getenv("MY_NODE", "py@127.0.0.1")

class MyProcess(Process):
    def __init__(self) -> None:
        self.count = 1
        self.erlang_node = os.getenv("ERLANG_NODE", 'erl@127.0.0.1')
        LOG.info(f"ERLANG_NODE={self.erlang_node}")

        Process.__init__(self)

        LOG.info("Registering process 'my_process' on this node")
        self.get_node().register_name(self, Atom('my_process'))

    def handle_one_inbox_message(self, msg):
        LOG.info("received %s", msg)

        self.get_node().send_nowait(sender=self.pid_,
                  receiver=(Atom(self.erlang_node), Atom('hello')),
                  message=(Atom('hello_from_python'),self.pid_, my_node, self.count))
        
        self.count = self.count + 1

def set_up_logging():
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="%(asctime)s [%(name)s]: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z"
    )

    # reduce low-level logging
    logging.getLogger("pyrlang.dist_proto.base_dist_protocol").setLevel(logging.CRITICAL)
    logging.getLogger("pyrlang.node").setLevel(logging.CRITICAL)


async def main():
    LOG.info("starting the python node")
    LOG.info(f"MY_NODE={my_node}")
    n = Node(node_name=my_node, cookie="COOKIE")
    set_up_logging()

    # start the named async process that accepts incoming messages
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
