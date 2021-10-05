import os
from pathlib import Path
from plotly import graph_objects as go
import pandas as pd
import re


def get_table_from_wrk_text(wrk_text: str) -> pd.DataFrame:
    table = wrk_text.split("Value   Percentile   TotalCount 1/(1-Percentile)")[1].split("#[Mean    =")[0]
    rows = [re.sub(" +", ' ', line).split(' ') for line in table.split('\n') if line != '']
    return pd.DataFrame({
        'value': [float(row[1]) for row in rows],
        'percentile': [float(row[2]) for row in rows],
        'total': [float(row[3]) for row in rows]
    })


class WrkReport:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.name = file_path.name
        with open(file_path) as fp:
            filet_txt = fp.read()
        self.table = get_table_from_wrk_text(wrk_text=filet_txt)

        summary_line = [line for line in filet_txt.split('\n') if 'requests in' in line]
        assert len(summary_line) == 1
        self.requests_num = int(summary_line[0].split(' ')[2])


def draw_requests(target_dir: str, title: str, res_path: str):
    wrk_reports = [
        WrkReport(file_path=Path(f"{target_dir}/{file_name}"))
        for file_name in sorted(os.listdir(target_dir))
        if 'wrk' in file_name
    ]

    fig = go.Figure()

    for wrk_report in wrk_reports:
        fig.add_trace(
            go.Scatter(
                x=wrk_report.table['percentile'],
                y=wrk_report.table['value'],
                mode="markers+lines",
                name=wrk_report.name,
                text=wrk_report.requests_num - wrk_report.table['total']
            )
        )

    fig.update_layout(
        xaxis_title="percentile",
        yaxis_title="time",
        title=title
    )
    fig.write_html(res_path)


draw_requests(
    target_dir="../2021-highload-dht/src/main/resources/reports/stage2/put_results",
    title="different implementations of POST-requests comparison",
    res_path="put.html"
)

draw_requests(
    target_dir="../2021-highload-dht/src/main/resources/reports/stage2/get_results",
    title="different implementations of GET-requests comparison",
    res_path="get.html"
)
