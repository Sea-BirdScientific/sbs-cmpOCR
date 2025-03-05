"""
Shiny app to plot two Satlantic (H)OCR calibration files.

shiny run --reload --launch-browser ./app.py
"""

import re
import pandas as pd
import plotly.graph_objs as go
from shiny import App, ui, reactive
import shinyswatch
from shinywidgets import output_widget, render_widget


# Function to read calibration file
def SATgetCal(calFile):
    """Read Satlantic-formated (H)OCR cal files for wavelength, scale Factors, and integration time"""
    calTags = {'ES', 'ED', 'Eu', 'LU', 'LT', 'LI'}
    dfcal = pd.DataFrame(columns=['tag', 'w', 'scaleFactor', 'intTime'])

    with open(calFile, 'r', encoding='utf-8') as fid:
        while True:
            tline = fid.readline()
            if not tline:
                break
            tsplit = tline.strip().split(' ')
            tag = tsplit[0]

            if tag in calTags and re.match(r'^OPTIC', tsplit[6]):
                w = float(tsplit[1])
                tline = fid.readline()
                tsplit = tline.strip().split('\t')
                scaleFactor = float(tsplit[1])
                intTime = int(float(tsplit[3]) * 1000) if len(tsplit) > 3 else 1
                dfrow = pd.DataFrame([{'tag': tag, 'w': w, 'scaleFactor': scaleFactor, 'intTime': intTime}])
                dfcal = pd.concat([dfcal, dfrow], ignore_index=True)
                fid.readline()  # Skip blank line

    return dfcal

# Function to plot files
def plot_files(df1, df2, name1, name2):
    """Plot the scale factors of two calibration files and their ratio"""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df1['w'], y=df1['scaleFactor'], mode='lines', name=name1))
    fig.add_trace(go.Scatter(x=df2['w'], y=df2['scaleFactor'], mode='lines', name=name2))
    fig.update_layout(legend=dict(x=0.50, y=0.95, xanchor='center', yanchor='top'), autosize=True, height=None)

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df1['w'], y=df2['scaleFactor'] / df1['scaleFactor'], mode='lines', name=f'{name2}/{name1}'))
    fig2.update_layout(title=f'{name2}/{name1}', autosize=True, height=None)

    return fig, fig2

def app_ui(request) :
    """Define the Shiny app's UI."""
    return ui.page_sidebar (
        ui.sidebar(
            ui.input_file('file1', 'Upload File 1:', accept=['.cal']),
            ui.input_file('file2', 'Upload File 2:', accept=['.cal']),
            open="always",  # Always keep the sidebar open
            width="25%",    # Set the sidebar width"
        ),
        ui.card(
            output_widget('plot_top'),
            output_widget('plot_bottom'),
        ),
        title='(H)OCR Cal File Plotter',
        theme=shinyswatch.theme.sandstone(),  # Apply a clean Bootstrap theme
    )

def server(input, output, session):
    """Define the Shiny app's server logic."""
    @reactive.calc
    def get_data():
        file1 = input.file1()
        file2 = input.file2()
        if not file1 or not file2:
            return None, None, None, None
        df1 = SATgetCal(file1[0]['datapath'])
        df2 = SATgetCal(file2[0]['datapath'])
        return df1, df2, file1[0]['name'], file2[0]['name']

    @output
    @render_widget
    def plot_top():
        df1, df2, name1, name2 = get_data()
        if df1 is None or df2 is None:
            return None
        fig, _ = plot_files(df1, df2, name1, name2)
        return fig

    @output
    @render_widget
    def plot_bottom():
        df1, df2, name1, name2 = get_data()
        if df1 is None or df2 is None:
            return None
        _, fig2 = plot_files(df1, df2, name1, name2)
        return fig2

app = App(app_ui, server)
