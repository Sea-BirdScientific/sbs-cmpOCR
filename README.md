# Compare scale factors from two (H)OCR calibration files 

| module | Description |
| ------ | ----------- |
| **cmpOCR** | Simple command-line Python script to plot the scale factors of two (H)OCRS and their relative percent difference.|
| **cmpOCRst** | Streamlit version of cmpOCR.  Run using 'streamlit run ./src/sbs-cmpOCR/cmpOCRst.py' |
| **app.py** | Shiny version of cmpOCR.  Run using 'shiny run --reload --launch-browser ./app.py' |

### Example data
The example_data directory contains two HOCR files you can use to test and view results.

### Getting started
* git clone https://github.com/Sea-BirdScientific/sbs-cmpOCR.git
* cd sbs-cmpOCR/src/sbs-cmpOCR

### Streamlit
* Streamlit: `pip install streamlit` into a virtual environment that also has plotly, pandas, pathlib
* From OS command line: `streamlit run ./cmpOCRst.py` (This should open a browser window at http://localhost:8501)
* After you drag and drop the two HOCR calfiles found in ./example_data, you should see two plotly plots

### Shiny
* Shiny: `conda install shiny, shinywidgets, shinyswatch` into a virtual environment that also has plotly, pandas, pathlib
* From OS command line: `shiny run --reload --launch-browser ./app.py` (This should open a browser window at http://localhost:8000)
* After you select two HOCR calfiles found in ./example_data, you should see two plotly plots

<img width="652" alt="image" src="https://github.com/Sea-BirdScientific/sbs-cmpOCR/assets/68403249/1c602510-4915-4a18-84a1-3994254e6e1e">