# StreamlitChatGPT
A Basic Raw ChatGPT interface in streamlit. Created by @AdamTomkins. Source Code: https://github.com/AdamRTomkins/StreamlitChatGPT. Modified to support Azure API by @HouWayne.

Please input api key in `config.yml` file before running the app with `streamlit run demo.py`.

Why we need this: Azure API need us to input base_url (ours: api.hku.hk), but almost all other apps choose to guess the base_url be like "YOUR_RESOURCE_NAME.openai.azure.com/", defined in Azure official Doc. Before they fix this, we need to use this app to specify the base_url.
## Requirements

This Demo requires users to have an OpenAI API key or Azure API key. Please input your API key in `config.yml` file.

## Installation

This simple application only needs to have the requirements file installed:

```pip install -r requirements.txt```

## Running the Demo.

This is a basic streamlit interface to the Open AI API. 
To access the demo, run:
```streamlit run demo.py```

After this command you should be able to access the UI at
```
Local URL: http://localhost:8501
Network URL: http://192.168.1.107:8501
```

