import argparse
import json
from bson import ObjectId
from pymongo import MongoClient
from dotenv import load_dotenv
import os

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

def get_latest_document_by(filter):
    client = MongoClient(os.getenv("MONGO_DB_LOCAL_CLIENT_ENDPOINT"))
    db = client["jenkins_automated"]
    collection = db["ml-model-pipeline"]

    # Find the latest document based on the creation timestamp
    latest_doc = collection.find_one(
        {},
        sort=[(filter, -1)]
    )
    
    return latest_doc


def getModelsInfo(report, filter):
    finalReport = []
   
    for i in report['models_deployed']:
        if report['models_deployed'][i]['working_status'] == filter:
            modelId = report['metadata']['jenkins_deploy_id']
            element = {
                'model_id': report['models_deployed'][i]['unique_id'],
                'network_desc': report['models_deployed'][i]['network_desc'],
                'working_status': report['models_deployed'][i]['working_status'],
                'model_arch': report['models_deployed'][i]['model_arch'],
                'model_category': report['models_deployed'][i]['model_category'],
                'InputType': report['models_deployed'][i]['InputType'],
                'FileType': report['models_deployed'][i]['FileType'],
                'Target': report['jenkins_params']['TARGET'],
                'Device': report['jenkins_params']['DEVICE'],
                'Precision': report['jenkins_params']['PRECISION'],
                'Mera Version': report['sys_specs']['MERA Version'],
                'MERA-TVM Version': report['sys_specs']['MERA-TVM Version'],
                'Mera-DNA Version': report['sys_specs']['MERA-DNA Version'],
                'Mera2-RUNTIME Version': report['sys_specs']['MERA2-RUNTIME Version'],
                'UploadedAt': report['metadata']['upload_data'],
                'JenkinsDeployId': report['metadata']['jenkins_deploy_id'],
                'Jenkins Pipeline': report['metadata']['jenkins_pipeline_id'],
                'Build URL': f"http://jenkins.edgecortix.local:8080/blue/organizations/jenkins/ml%2Fml-model-pipeline/detail/ml-model-pipeline/{modelId}/pipeline"
            }

            finalReport.append(element)

    return finalReport

def main(args):
    report = get_latest_document_by(args.filter_by)
    
    print(getModelsInfo(report, args.model_passing_status))
    return report

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_passing_status",
        default="",
        required=True,
        choices=["Y", "N"],
        type=str,
        help="Get Successful (Y) or Not Succesful (N) models",
    )
    parser.add_argument(
        "--filter_by",
        default="metadata.upload_data",
        required=False,
        choices=[
            "metadata.upload_data",
            "jenkins_params.MERA_INSTALL_VERSION", 
            "jenkins_params.EC_MODEL_BRANCHMARKING_BRANCH", 
            "jenkins_params.DEVICE",
            "jenkins_params.MERA_DEMOS_BRANCH",
            "jenkins_params.HOST_ARCH",
            ],
        type=str,
        help="Filter by information you want in database. Note: currently, it will return the latest added document based on the filter you choose"
    )

    return parser.parse_args()

if __name__ == "__main__":
    import sys

    sys.exit(main(get_args()))
