import re
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

log_path = Path("../2021-highload-dht/sharding.logs")

with open(log_path) as fp:
    lines = fp.readlines()

df_roots = pd.DataFrame(
    [
        {
            'host': re.sub(".+PARTITIONING: ", "", line).split(",")[1].replace(" ", "").replace('\n', ''),
            'hash': re.sub(".+PARTITIONING: ", "", line).split(",")[0]
        }
        for line in lines
        if 'PARTITIONING' in line
    ]
).drop_duplicates()

df_load = pd.DataFrame(
    [
        {
            'host': re.sub(".+by myself ", "", line).replace('\n', ''),
        }
        for line in lines
        if 'processing by myself' in line
    ]
)

res_df = pd.merge(df_load, df_roots, on=['host'])
res_df_hist = res_df.groupby(by=['host']).count().rename(columns={'hash': 'records_num'})

res_df_hist.plot.bar()

plt.xticks(rotation=45)
plt.show()
