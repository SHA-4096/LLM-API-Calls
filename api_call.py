import json
import time

def generate_with_api(
        messages: list, 
        api_key, 
        base_url = "https://api.deepseek.com", 
        path = "deepseek-reasoner",
        args = None
    ):
    assert args is not None, "args must be provided for API generation, this assertion fails due to legacy code"
    # print(f"API call with path: {path}")
    from openai import OpenAI
    success = False
    timeout = 600
    max_tokens = 50
    if args.cot:
        max_tokens = 30000
        timeout = 3000
    if "DeepSeek-R1" in path or "o3-mini" in path or "deepseek-reasoner" in path or "deepseek-r1" in path: # reasoning models
        # max_tokens = 2500
        max_tokens = 30000
        timeout = 3000
    response = None
    while not success:
        try:
            client = OpenAI(api_key=api_key, base_url=base_url)
            response = client.chat.completions.create(
                model=path,
                messages=messages,
                timeout=timeout,
                max_completion_tokens=max_tokens,
                stream=stream
            )
            success = True
        except Exception as e:
            print(f"API call failed: {e}, retrying...")
    
    assert response is not None, "Response should not be None"

    assert response.choices[0].message.role == "assistant"
    
    content = response.choices[0].message.content
    
    reasoning_content = None # only for deepseek-reasoner
    if path == "deepseek-reasoner":
        reasoning_content = response.choices[0].message.reasoning_content
        content = f"<think>\n\n{reasoning_content}</think>\n\n{content}"
        
    usage = response.usage
    
    
    return content, usage


def generate_with_api_zhipu(
        messages: list, 
        api_key, 
        path,
        max_tokens=50
    ):
    success = False
    from zhipuai import ZhipuAI
    client = ZhipuAI(api_key=api_key)
    try:
        while not success:
            response = client.chat.completions.create(
                model=path,
                messages=messages,
                max_tokens=max_tokens
            )
            success = True
    except Exception as e:
        print(f"API call failed: {e}, retrying...")
        time.sleep(0.5)

    assert response.choices[0].message.role == "assistant"
    
    content = response.choices[0].message.content
    
    usage = response.usage
    
    return content, usage


def generate_with_api_azure(
        messages: list, 
        api_key, 
        base_url, 
        path
    ):
    from openai import AzureOpenAI
    client = AzureOpenAI( api_key=api_key,api_version='2023-05-15', azure_endpoint=base_url)
    success = False
    while not success:
        try:
            response = client.chat.completions.create(
                model=path,
                messages=messages,
                timeout=600,
                max_completion_tokens=50,
            )
            success = True
        except Exception as e:
            print(f"API call failed: {e}, retrying...")
            time.sleep(2)

    assert response.choices[0].message.role == "assistant"
    
    content = response.choices[0].message.content
    
    usage = response.usage
    
    return content, usage

if __name__ == "__main__":
    #### Example usage ####
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, can you introduce yourself?"},
    ]
    
    model2path = json.load(open("config/model2path_api.json", "r"))
    model2api_auth = json.load(open("config/model2api_auth.json", "r"))
    
    # model = "glm-4-long"
    model = "llama3.1-8b"
    response = None
    usage = None
    
    if model2api_auth[model]["api_type"] == "openai":
        response, usage = generate_with_api(
            messages=messages, 
            api_key=model2api_auth[model]["api_key"], 
            path=model2path[model],
            max_tokens=50
        )
    elif model2api_auth[model]["api_type"] == "zhipu":
        response, usage = generate_with_api_zhipu(
            messages=messages, 
            api_key=model2api_auth[model]["api_key"], 
            base_url=model2api_auth[model]["base_url"], 
            path=model2path[model],
            max_tokens=50
        )
    elif model2api_auth[model]["api_type"] == "azure":
        response, usage = generate_with_api_azure(
            messages=messages, 
            api_key=model2api_auth[model]["api_key"], 
            base_url=model2api_auth[model]["base_url"], 
            path=model2path[model],
            max_tokens=50
        )
    
    print(f"Response is {response}")
    print(f"Input tokens count: {usage.prompt_tokens}")
    print(f"Output tokens count: {usage.completion_tokens}")
    print(f"Usage struct: {usage}")