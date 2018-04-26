import plotly.plotly as py
import plotly
import plotly.graph_objs as go
import json
from datetime import datetime
import numpy as np

apiKey = "zVXlB8fr3eWh9p6lZBjk"
userName = "codenamekiller1"
plotly.tools.set_credentials_file(username=userName, api_key=apiKey)

y0 = np.random.randn(50) - 1
y1 = np.random.randn(50) + 1

y0 = [97, 93, 86, 89, 101, 153, 71, 86, 102, 83, 89, 87, 93, 99, 91, 85, 71]
y1 = [96, 79, 70, 93, 72, 74, 75, 66, 88, 74, 83, 87, 77, 74, 87, 79, 102]
y2 = [84, 90, 92, 115, 85, 96, 77, 95, 91, 88, 99, 88, 103, 92, 78]
y3 = [79, 86, 86, 71, 113, 82, 80, 86, 96, 77, 77, 84]
region_1 = go.Box(
    y=y0,
    name="Region 1"
)
region_2 = go.Box(
    y=y1,
    name="Region 2"
)
region_3 = go.Box(
    y=y2,
    name="Region 3"
)
region_4 = go.Box(
    y=y3,
    name="Region 4"
)
data = [region_1, region_2, region_3, region_4]
py.iplot(data, filename="test")
