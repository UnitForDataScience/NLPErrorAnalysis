import plotly.plotly as py
import plotly
import plotly.graph_objs as go
import json
from datetime import datetime
import numpy as np

apiKey = "zVXlB8fr3eWh9p6lZBjk"
userName = "codenamekiller1"
plotly.tools.set_credentials_file(username=userName, api_key=apiKey)
finalDateData = json.load(open('./dataFinds.json'))
yearWiseEveryPlant = dict()
for plants in finalDateData:
    yearWiseEveryPlant[plants] = dict()
    for report in finalDateData[plants]:
        year = datetime.strptime(finalDateData[plants][report], "%Y-%m-%d").year
        if year in yearWiseEveryPlant[plants]:
            yearWiseEveryPlant[plants][year] += 1
        else:
            yearWiseEveryPlant[plants][year] = 1

plotlyData = list()
x_Axis = [w for w in range(1999, 2018)]
scatterThis = list()
for plants in yearWiseEveryPlant:
    y_Axis = list()
    for year in x_Axis:
        if year in yearWiseEveryPlant[plants]:
            y_Axis.append(yearWiseEveryPlant[plants][year])
        else:
            y_Axis.append(0)
    trace = go.Scatter(
        x=x_Axis,
        y=y_Axis,
        mode='lines+markers',
        visible='legendonly',
        name=plants
    )
    plotlyData.append(trace)

py.iplot(plotlyData, filename='line-mode')
