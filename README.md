# ML Model GUI

This project aims to be a GUI for our current models and their respective maturity status. All information is gathered on our database, so if data don't seem correct, please check the respective pipelines that populate MongoDB.

# Requirements

1. Export MongoDB internal endpoint in your `~/.zshrc`, `~/.bashrc` or similar by. Please ask someone from the team if you don't know what is the endpoint

```sh
export MONGO_DB_LOCAL_CLIENT_ENDPOINT="<endpoint>"
```

2. Install python-dotenv:
```sh 
pip install python-dotenv
```

3. This is a CLI. In order to use it, you can call `filterReportBy.py` passing some arguments along

| CLI arg option       | Possible Values           |       Required        |  Default Value                    |
|----------------------|---------------------------|-----------------------|-----------------------------------|
|--model_passing       |    ["Y", "N" ]                                    |      Yes     |                    |
|--filter_by           | ["metadata.upload_data"]                          |      No      |metadata.upload_data|
|--filter_by           | ["jenkins_params.MERA_INSTALL_VERSION"]           |      No      |metadata.upload_data|
|--filter_by           | ["jenkins_params.EC_MODEL_BRANCHMARKING_BRANCH"]  |      No      |metadata.upload_data|
|--filter_by           | ["jenkins_params.DEVICE"]                         |      No      |metadata.upload_data|
|--filter_by           | ["jenkins_params.MERA_DEMOS_BRANCH"]              |      No      |metadata.upload_data|
|--filter_by           | ["jenkins_params.HOST_ARCH"]                      |      No      |metadata.upload_data|
