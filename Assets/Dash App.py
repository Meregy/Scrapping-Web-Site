import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from Assets.Scraper import Scrapping
from Assets.utils import diff_, total, div_

building_name = 'HUAWEI'
sc = Scrapping(building_name)
file = sc.downloader()
df = pd.read_csv(file)
log_out = sc.logging_out()
df[['Task Reported Date', 'Finish Date', 'Task Due By Date']] = df[
    ['Task Reported Date', 'Finish Date', 'Task Due By Date']].apply(pd.to_datetime)
df = df.set_index("Task Reported Date")
df = df.sort_values('Task Reported Date')

year_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
total_ppm = total("PPM", "2020")
total_break_down = total("BREAKDOWN", "2020")
total_bd_completed = total("BREAKDOWN", "2020", 'Completed')
total_bd_outstading = diff_(total_bd_completed, total_break_down)
total_ppm_completed = total("PPM", "2020", 'Completed')
total_ppm_outstading = diff_(total_ppm, total_ppm_completed)
bd_completed_pres = [div_(total_bd_completed, total_break_down)[i] * 100 for i in range(len(total_break_down))]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='HUAWIE Dashboard'),

    html.Div(children='''
        Dashboard for HUAWIE Building.
    '''),

    dcc.Graph(
        id='B',
        figure={
            'data': [
                {'x': total_bd_completed, 'type': 'bar', 'name': 'SF'},
                {'x': total_bd_outstading, 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Breakdowns VS Outstanding'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)