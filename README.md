# LLM API Calls

## Acquiring your APIKey

Go to the corresponding site to acquire API keys:

Deepinfra(hosts open models such as llama): https://deepinfra.com/dash/api_keys

OpenAI: https://platform.openai.com/api-keys

Zhipu: https://bigmodel.cn/usercenter/proj-mgmt/apikeys

DeepSeek: https://platform.deepseek.com/api_keys

2233.ai(A proxy site for OpenAI and Claude): https://2233.ai/api


## Updating your APIKey

Update the corresponding APIKeys to `config/model2api_auth.json`

## You're Ready to Go!

API calling functions and usage example is written in `api_call.py`, you can give it a try by simply running the following command:

```bash
pip install -r requirements.txt
python api_call.py
```

## Adding your own config

You can add your own config by modifying `model2api_auth.json` and `model2path_api.json`.

A configuration looks like the following:

```json
"deepseek-v3-official": {
        "base_url": "https://api.deepseek.com",
        "api_key": "DEEPSEEK_API_KEY",
        "api_type": "openai"
    },
```

Check the official documentations for `base_url` and `api_key`. For `api_type`, now we support `openai `, `zhipu `and `azure`.
