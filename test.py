from client import BW2DataClient
from client import timestamp

c = BW2DataClient(client=None, archivers=["ucberkeley"])

c.query("select *")

uuids = c.uuids('path like "tedmain"')
#print c.data_uuids(uuids, "now", "now -10sec")
#print c.stats('path like "tedmain"', "now", "now -5min", 38)
print c.window_uuids(uuids, "now", "now -1d", "8h")
