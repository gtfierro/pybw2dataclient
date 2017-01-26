import msgpack
import random
import time
from datetime import timedelta

from bw2python import ponames
from bw2python.bwtypes import PayloadObject
from bw2python.client import Client


class BW2DataClient(object):
    """
    Simple wrapper class for interacting with data services exposed over BOSSWAVE
    """
    def __init__(self, client=None, archivers=None):
        """
        Creates a BW2 Data client

        Arguments:
        [client]: if this is None, we use environment vars to configure a client
                  automatically; else, we use the client provided
        [archivers]: this is a list of base archiver URIs. These can be found by
                  running "pundat scan <namespace>"
        """
        # bw2 client
        if client is None:
            client = Client()
            client.setEntityFromEnviron()
            client.overrideAutoChainTo(True)
        if not isinstance(client, Client):
            raise TypeError("first argument must be bw2python.client.Client or None")
        self.c = client
        self.vk = client.vk


        self.archivers = []
        # scan for archiver liveness
        for archiver in archivers:
            responses = self.c.query("{0}/*/s.giles/!meta/lastalive".format(archiver))
            for resp in responses:
                # get the metadata records from the response
                md_records = filter(lambda po: po.type_dotted == ponames.PODFSMetadata, resp.payload_objects)
                # get timestamp field from the first metadata record
                last_seen_timestamp = msgpack.unpackb(md_records[0].content).get('ts')
                # get how long ago that was
                now = time.time()*1e9 # nanoseconds
                # convert to microseconds and get the timedelta
                diff = timedelta(microseconds = (now - last_seen_timestamp)/1e3)
                print "Saw [{0}] archiver {1}".format(archiver, pretty_print_timedelta(diff))
                if diff.total_seconds() < 20:
                    self.archivers.append(archiver)

    def query(self, query, archiver=""):
        """
        Runs the given pundat query and returns the results as a Python object.

        Arguments:
        [query]: the query string
        [archiver]: if specified, this is the archiver to use. Else, it will run on the first archiver passed
                    into the constructor for the client
        """
        if archiver == "":
            archiver = self.archivers[0]

        def _handleresult(msg):
            # decode, throw away if not mance nonce
            print msg

        vk = self.vk[:-1] # remove last part of VK because archiver doesn't expect it

        # set up receiving
        self.c.subscribe("{0}/s.giles/_/i.archiver/signal/{1},queries".format(archiver, vk), _handleresult)

        # execute query
        nonce = random.randint(0, 2**32)
        q_struct = msgpack.packb({"Query": query, "Nonce": nonce})
        po = PayloadObject((2,0,8,1), None, q_struct)
        self.c.publish("{0}/s.giles/_/i.archiver/slot/query".format(archiver), payload_objects=(po,))

        # TODO: need a way to wait for data
        time.sleep(5)


def pretty_print_timedelta(td):
    res = ""
    if td.days:
        res += "{0} hours ".format(td.days)
    if td.seconds:
        res += "{0} seconds ".format(td.seconds)
    return res+"ago"
