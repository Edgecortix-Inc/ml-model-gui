import streamlit as streamlit
import reportGenerator as reportGenerator
import streamlit as streamlit
from streamlit.logger import get_logger
import pandas as pd

LOGGER = get_logger(__name__)
def getFlowList():
    return ["deploy", "inference", "latency", "eval"]

def pretty_str(text: str, color: str):
    colors = {
        "BLUE": "\033[34m",
        "CYAN": "\033[36m",
        "GREEN": "\033[32m",
        "YELLOW": "\033[33m",
        "RED": "\033[31m",
        "ENDC": "\033[0m",
    }

    if color not in colors:
        raise Exception("Input color not supported.")

    return colors[color] + text + colors["ENDC"]

def get_targets_prec_list():
    return [
        "interpreter",
        "interpreterhwbf16",
        "simulatorbf16",
        "interpreterhw",
        "simulator",
        "ipbf16",
        "ip",
    ]

def get_mera_versions():
    return ['']

def get_architectures():
    return ['x86', 'aarch64']

def createHeader():
    streamlit.set_page_config(
        page_title="ML Model Pipeline",
        page_icon=":bar_chart:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    streamlit.title("ML Model Pipeline Report")
    streamlit.write(
        "This page provides a summary of the ML model pipeline, including the status of each model for different functions (deploy, inference, latency, eval)."
    )
    streamlit.write(
        "The table below shows the status of each model for different functions (deploy, inference, latency, eval)."
    )
    streamlit.write(
        "You can filter the models by flow, target, Mera version, and architecture using the dropdowns below."
    )

def createContainerSectionDropdown():
    with streamlit.container(height=100):
            col1, col2, col3, col4 = streamlit.columns(4)
            with col1:
                streamlit.selectbox("List of Flows", getFlowList())
            with col2:
                streamlit.selectbox("List of Targets", get_targets_prec_list())
            with col3:
                streamlit.selectbox("List of Mera Versions", get_mera_versions())
            with col4:
                streamlit.selectbox("List of Architectures", get_architectures())

def getReport(filter_by, passing_status):
    report = reportGenerator.get_latest_document_by(filter_by)
    reportInfo = reportGenerator.getModelsInfo(report, passing_status)
    dataframe = pd.DataFrame(reportInfo)

    streamlit.dataframe(
        dataframe,
        column_config={
            "Name": "ml-model-pipeline-tabulate", 
        }
    )

def run_web_frontend(filter_by='metadata.upload_data', passing_status='Y'):
    # Create Dropdown choices for filtering
    createHeader()
    createContainerSectionDropdown()

    getReport(filter_by, passing_status)

run_web_frontend()


#with streamlit.form("test_summary_form"):
#    streamlit.write("### Test Summary")
#    streamlit.write(
#        "This is a summary of the test results for the models deployed in the pipeline."
#    )
#    streamlit.write(
#        "The table below shows the status of each model for different functions (deploy, inference, latency, eval)."
#    )
#
#    # Get the latest report
#    report = reportGenerator.get_latest_document_by("created_at")
#
#    # Get the models info
#    finalReport = reportGenerator.getModelsInfo(report, "Y")
#
#    # Convert to DataFrame
#    df = pd.DataFrame(finalReport)
#
#    # Style the DataFrame
#    styled_df = style_dataframe(df)
#
#    # Display the styled DataFrame
#    streamlit.dataframe(styled_df)