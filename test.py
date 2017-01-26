import client

c = client.BW2DataClient(client=None, archivers=["ucberkeley"])

c.query("select *")
