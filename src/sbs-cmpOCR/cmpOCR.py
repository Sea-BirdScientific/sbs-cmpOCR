"""cmpOCR.py"""

import re
import argparse
import pandas as pd
from pathlib import Path
from plotly.subplots import make_subplots
import plotly.graph_objects as go



def SATgetCal(calFile):

    """Read Satlantic-formated (H)OCR cal files for wavelength and scale Factors"""

    # Lines we want start with these tags
    calTags = {'ES', 'ED', 'Eu', 'LU', 'LT', 'LI'}

    # Read HyperOCR cal file
    dfcal = pd.DataFrame(columns=['tag', 'w', 'scaleFactor', 'intTime'])
    iw = 1
    with open(calFile, "r") as fid :
        while True: 

            # get a line and split it 
            tline = fid.readline()
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
                    tline = fid.readline()
                    tsplit = tline.strip().split('\t')
                    scaleFactor = float(tsplit[1])     # coeff
                    dfrow = pd.DataFrame( [{'tag': tag, 'w':w, 'scaleFactor': scaleFactor}])
                    dfcal = pd.concat([dfcal, dfrow], ignore_index=True)
                    
                tline = fid.readline();  # skip blank line

    return dfcal




def main() :

    """Main routine to parse args, read cal files, and plot scale Factors of two (H)OCR Cal files"""

    # rootDir = '/Volumes/Public/Calib/Radiometers/504/504I/OCR504ICSA-2339/'
    # cal1 = 'Cal01/Cal Data/CalA/DI42339A.cal'
    # cal2 = 'Cal02/CalC2/DI42339C.cal'
    rootDir = ''

    # Instantiate the command line argument parser
    parser = argparse.ArgumentParser(description='Compare OCR')

    # Required positional argument
    parser.add_argument('cal1', type=str, 
                    help='(H)OCR cal file 1')

    # Required positional argument
    parser.add_argument('cal2', type=str, 
                    help='(H)OCR cal file 2')

    # Optional arguments
    parser.add_argument('--root', '-r', type=str, dest='rootDir',
                    help='Optional root directory; cal1 and cal2 are relative to this root')

    parser.add_argument('--hocr', dest='isHOCR', action='store_true',
                    help='This is an HOCR, simplify plotting')

    # Parse command line arguments
    args = parser.parse_args()
    cal1 = Path(args.cal1)
    cal2 = Path(args.cal2)
    rootDir = args.rootDir
    isHOCR = args.isHOCR

    # Add rootDir, if supplied
    if rootDir :
        rootDir = Path(rootDir)
        cal1 = rootDir / cal1
        cal2 = rootDir / cal2

    # Get calibration files and compute RPD
    dfcal1 = SATgetCal(cal1)
    dfcal2 = SATgetCal(cal2)
    rpd = 100*(dfcal2.scaleFactor - dfcal1.scaleFactor)/(dfcal1.scaleFactor)

    # Plot control
    if isHOCR:
        mode = 'lines'
    else:
        mode = 'lines+markers'

    # Subplots
    fig = make_subplots(rows=2, cols=1)

    fig.add_trace(
        go.Scatter(x=dfcal1.w, y=dfcal1.scaleFactor, mode = mode, name = cal1.name ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=dfcal2.w, y=dfcal2.scaleFactor, mode = mode, name = cal2.name),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=dfcal1.w, y=rpd, mode = mode, name = 'RPD %'),
        row=2, col=1
    )

    fig['layout']['xaxis2']['title']='Wavelength (nm)'
    fig['layout']['yaxis']['title']='Scale Factor'
    fig['layout']['yaxis2']['title']='Rel. Percent Difference (%)'
    fig.update_layout(height=600, width=800, title_text="Compare OCR Calibrations")
    fig.show()

    return


if __name__ == '__main__' :
    main()