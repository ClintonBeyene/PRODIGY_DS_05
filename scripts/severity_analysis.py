import pandas as pd
from plotly import graph_objs as go


def severity_analysis(df):
    # create a dataframe of Severity and the corresponding accident cases
    severity_df = pd.DataFrame(df['Severity'].value_counts()).rename(columns={'index':'Severity', 'count':'Cases'})
    fig = go.Figure(go.Funnelarea(
        text = ["Severity - 2","Severity - 3", "Severity - 4", "Severity - 1"],
        values = severity_df.Cases,
        title = {"position": "top center", 
                "text": "<b>Impact on the Traffic due to the Accidents</b>", 
                'font':dict(size=18,color="#7f7f7f")},
        marker = {"colors": ['#14a3ee', '#b4e6ee', '#fdf4b8', '#ff4f4e'],
                    "line": {"color": ["#e8e8e8", "wheat", "wheat", "wheat"], "width": [7, 0, 0, 2]}}
        ))

    fig.show()