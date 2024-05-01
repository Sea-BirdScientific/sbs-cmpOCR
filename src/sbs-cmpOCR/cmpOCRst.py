import re
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from pathlib import Path

def read_file(file):
    df = pd.read_csv(file, delimiter=' ', header=None)
    df.columns = ['w', 'scaleFactor']
    return df

def SATgetCal(calFile):

    """Read Satlantic-formated (H)OCR cal files for wavelength and scale Factors"""

    # Lines we want start with these tags
    calTags = {'ES', 'ED', 'Eu', 'LU', 'LT', 'LI'}

    # Read HyperOCR cal file
    dfcal = pd.DataFrame(columns=['tag', 'w', 'scaleFactor', 'intTime'])
    iw = 1

    with calFile as fid :
        while True: 

            # get a line and split it 
            tline = str(fid.readline(), encoding='utf-8')
            if not tline:
                break
            tsplit = tline.strip().split(' ')
            tag = tsplit[0]

            # check if valid tag and OPTICx field
            # If so, extract:
            #   first line: tag and lambda (w)
            #   second line: calcoef (scaleFactor)
            #   third line: blank
            if tag in calTags :
                # if (tsplit[6] == 'OPTIC3') :
                if re.match(r'^OPTIC', tsplit[6]) :
                    w = float(tsplit[1])              # lambda                    
                    tline = str(fid.readline(), encoding='utf-8')
                    tsplit = tline.strip().split('\t')
                    scaleFactor = float(tsplit[1])     # coeff
                    if (len(tsplit) > 3) :
                        intTime = int(float(tsplit[3])*1000)
                    else :
                        intTime = 1
                    dfrow = pd.DataFrame( [{'tag': tag, 'w':w, 'scaleFactor': scaleFactor, 'intTime': intTime}])
                    dfcal = pd.concat([dfcal, dfrow], ignore_index=True)
                    
                tline = str(fid.readline(), encoding='utf-8');  # skip blank line

    return dfcal

def plot_files(file1, file2):
    # df1 = read_file(file1)
    # df2 = read_file(file2)
    print(file1, file2)
    df1 = SATgetCal(file1)
    df2 = SATgetCal(file2)

    fig = go.Figure()

    # Plotting each file on the top plot
    fig.add_trace(go.Scatter(x=df1['w'], y=df1['scaleFactor'], mode='lines', name=file1.name))
    fig.add_trace(go.Scatter(x=df2['w'], y=df2['scaleFactor'], mode='lines', name=file2.name))

    # Plotting the ratio on the bottom plot
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df1['w'], y=df2['scaleFactor'] / df1['scaleFactor'], mode='lines', name=f'{file2.name}/{file1.name}'))
    fig2.update_layout(title=f'{file2.name}/{file1.name}')

    return fig, fig2

def main():
    st.title('(H)OCR File Plotter')

    file1 = st.file_uploader('Upload File 1:', type=['cal'])
    file2 = st.file_uploader('Upload File 2:', type=['cal'])
    print(file1,file2)

    if file1 and file2:
        plot_top, plot_bottom = plot_files(file1, file2)

        st.plotly_chart(plot_top, use_container_width=True)
        st.plotly_chart(plot_bottom, use_container_width=True)

if __name__ == "__main__":
    main()