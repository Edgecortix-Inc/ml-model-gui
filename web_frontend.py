import streamlit as streamlit
import query as query
import streamlit as streamlit
from streamlit.logger import get_logger
import pandas as pd

LOGGER = get_logger(__name__)

def getQueryFilter():
    return [
        "metadata.upload_data",
        "jenkins_params.MERA_INSTALL_VERSION", 
        "jenkins_params.EC_MODEL_BRANCHMARKING_BRANCH", 
        "jenkins_params.DEVICE",
        "jenkins_params.MERA_DEMOS_BRANCH",
        "jenkins_params.HOST_ARCH",
    ]

def returnDesiredStatus():
    return [
        "Y",
        "N",
    ]

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
    return ['2.3.0']

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
        "The table below shows the level of support of each model"
    )
    streamlit.write(
        "You can filter the models by flow, target, Mera version, and architecture using the dropdowns below."
    )

def createContainerSectionDropdown():
    flowSelected, targetsSelected, meraVersionsSelected, archSelected, statusSelected, queryFilterSelected = '', '', '', '', '', ''
    with streamlit.container(height=100):
        flow, targets, meraVersions, arch, status, queryFilter = streamlit.columns(6)
        with flow:
            flowSelected = streamlit.selectbox("List of Flows", getFlowList())
        with targets:
            targetsSelected = streamlit.selectbox("List of Targets", get_targets_prec_list())
        with meraVersions:
            meraVersionsSelected = streamlit.selectbox("List of Mera Versions", get_mera_versions())
        with arch:
            archSelected = streamlit.selectbox("List of Architectures", get_architectures())
        with status:
            statusSelected = streamlit.selectbox("List of Status", returnDesiredStatus())
        with queryFilter:
            queryFilterSelected = streamlit.selectbox("List of Query Filters", getQueryFilter())

    return [flowSelected, targetsSelected, meraVersionsSelected, archSelected, statusSelected, queryFilterSelected]

def getReport(filter_by, passing_status):
    report = query.get_latest_document_by(filter_by)
    reportInfo = query.getModelsInfo(report, passing_status)
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

    # This will be used to create the queries for the report
    selections = createContainerSectionDropdown
    createContainerSectionDropdown()
    

    # Add a submit button to trigger report generation
    if streamlit.button("Submit"):
        getReport(filter_by, passing_status)

run_web_frontend()

