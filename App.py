import pandas as pd
from Assets.Scraper import Scrapping
from Assets.utils import diff_, total, div_, category_count
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

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
total_ppm = total(df, "Task Type", "PPM")
total_break_down = total(df, "Task Type", "BREAKDOWN")
total_bd_completed = total(df, "Task Type", "BREAKDOWN", "Level Of Completion", "Completed")
total_bd_outstading = diff_(total_bd_completed, total_break_down)
total_ppm_completed = total(df, "Task Type", "PPM", "Level Of Completion", "Completed")
total_ppm_outstading = diff_(total_ppm, total_ppm_completed)
bd_completed_pres =[round(num, 1) for num in [div_(total_bd_completed, total_break_down)[i] * 100 for i in range(len(total_break_down))]]
category = df['Category'].unique().tolist()
category.remove('PPM')
total_category = category_count(df, category)
labels = ["Total Breakdown", "HVAC", 'Emergency', 'High', 'Medium', 'low','very low', "Electrical", 'Emergency', 'High', 'Medium', 'low','very low', "BMS", 'Emergency', 'High', 'Medium', 'low','very low', "Mechanical", 'Emergency', 'High', 'Medium', 'low','very low', "Civil", 'Emergency', 'High', 'Medium', 'low','very low', "Fire Alarm", 'Emergency', 'High', 'Medium', 'low','very low']

# -------------------------Dashboard-----------------------
fig1 = go.Figure(data=[
    go.Bar(name='Completed Breakdown', x=year_months, y=total_bd_completed, text=total_bd_completed, textposition='auto',),
    go.Bar(name='Outstanding Breakdown', x=year_months, y=total_bd_outstading, text=total_bd_outstading, textposition='auto',)
])
fig1.update_layout(title="Breakdowns Completed VS Outstanding",barmode='stack', yaxis=dict(title='Breakdown Tasks', titlefont_size=16,tickfont_size=14,))

fig2 = go.Figure(data=[
    go.Bar(name='Completed PPM', x=year_months, y=total_ppm_completed, text=total_ppm_completed, textposition='auto',),
    go.Bar(name='Outstanding PPM', x=year_months, y=total_ppm_outstading, text=total_ppm_outstading, textposition='auto',)
])
fig2.update_layout(title="PPM Completed VS Outstanding",barmode='stack', yaxis=dict(title='PPM Tasks', titlefont_size=16,tickfont_size=14,))

fig3 = go.Figure(data=[
    go.Bar(name='Task Completed Performance', x=year_months, y=bd_completed_pres, text=bd_completed_pres, textposition='auto',)
])
fig3.update_layout(title="Task Completed Performance",barmode='stack', yaxis=dict(title='% of Completed Ontime', titlefont_size=16,tickfont_size=14,))

fig4 = fig = go.Figure(data=[go.Pie(labels=category, values=total_category, hole=.3)])
fig4.update_layout(title_text="Breakdown By Category")


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {'background': '#111111',
          'text': '#1e702b'}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='HAUWEI DASHBOARD',
        style={
            'textAlign': 'left',
            'color': colors['text']
        }
    ),

    html.Div(children='Dashboard for HUAWIE Building.', style={
        'textAlign': 'left',
        'color': colors['text']
    }),

    dcc.Graph(
        id='Breakdowns Completed VS Outstanding',
        figure=fig1
    ),

    dcc.Graph(
        id='PPMs Completed VS Outstanding',
        figure=fig2
    ),
    dcc.Graph(
        id='Task Completed Performance',
        figure=fig3
    ),
    dcc.Graph(
        id='Category Breakdown Tasks',
        figure=fig4
    )
])

if __name__ == '__main__':
    app.run_server(debug=False)

