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

3. This is a GUI project. In order to use it, please select which filters you want to query on the UI
