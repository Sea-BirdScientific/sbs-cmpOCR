# Compare scale factors from two (H)OCR calibration files 

| module | Description |
| ------ | ----------- |
| **cmpOCR** | Simple command-line Python script to plot the scale factors of two (H)OCRS and their relative percent difference.|
| **cmpOCRst** | Streamlit version of cmpOCR.  Run using 'streamlit run ./src/sbs-cmpOCR/cmpOCRst.py' |

### Example data
The example_data directory contains two HOCR files you can use to test and view results.

### Getting started
* **pip install streamlit** into a virtual environment that also has plotly, pandas, pathlib
* git clone https://github.com/Sea-BirdScientific/sbs-cmpOCR.git
* cd sbs-cmpOCR
* From OS command line: **streamlit run ./src/sbs-cmpOCR/cmpOCRst.py** (This should open a browser window at http://localhost:8501)
* After you drag and drop the two HOCR calfiles found in ./example_data, you should see two plotly plots

<img width="652" alt="image" src="https://github.com/Sea-BirdScientific/sbs-cmpOCR/assets/68403249/1c602510-4915-4a18-84a1-3994254e6e1e">
