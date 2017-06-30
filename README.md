# Python BW2 Data Client

**Current Version: 0.6.4**

This is a simple Python library for accessing data services exposed over BOSSWAVE.

Currently, this just interfaces with the [pundat archiver](https://github.com/gtfierro/pundat), and uses the sMAP-like [pundat query language](https://github.com/gtfierro/PunDat/wiki).

## Installation

Requirements (do once):

* install [BOSSWAVE](https://github.com/immesys/bw2) and configure an entity
* get access to the archiver (ask someone to make the appropriate DOTs for you)
* install [BOSSWAVE Python bindings](https://github.com/SoftwareDefinedBuildings/bw2python),
  though this package will try to install them for you
* configure a default entity (`$BW2_DEFAULT_ENTITY`) or otherwise make note of where your entity file is
* install this library
    * using `pip`:
    
      ```bash
      pip install bw2dataclient
      ```
    * from source:
    
      ```bash
      git clone github.com/gtfierro/pybw2dataclient
      cd pybw2dataclient
      pip install -r requirements.txt
      python setup.py install
      ```

## Usage

```python
from bw2dataclient import DataClient, timestamp, make_dataframe

# we supply a list of archivers we want to be able to query
# to find archivers on a namespace, install the pundat tool and run 'pundat scan'
client = DataClient(archivers=["ucberkeley"])

# get UUIDs
uuids = client.uuids('name = "air_temp" and Deployment = "CIEE"')

# get timestamps
start = timestamp('6/25/2017')
end = timestamp('6/28/2017')

# get 1-hour window data for the first uuid
data = client.window_uuids(uuids[0], start, end, '1h')

# get a dataframe from the results, keyed by the UUID
dfs = make_dataframe(data)
print dfs[uuids[0]].describe()

#                     min         mean          max         count
#      count    71.000000    71.000000    71.000000     71.000000
#      mean   -140.014085  -109.968192   -71.845070   6964.591549
#      std     384.719508   320.405044   222.238459   9745.533602
#      min   -1597.000000 -1407.781121 -1224.000000      0.000000
#      25%     -23.000000   -21.734729   -20.500000      0.000000
#      50%       0.000000     0.000000     0.000000      0.000000
#      75%       0.000000     0.000000     0.000000  20079.000000
#      max       0.000000     0.000000     0.000000  21600.000000
```

### Caveats

Doesn't play nicely with Jupyter notebook if you run a cell more than once. This is more than likely some bad interaction with threads
