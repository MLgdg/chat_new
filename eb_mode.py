import os
import sys
import json
import requests
import time

def main_eb4(messages):
    res = ''
    token = ''
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/api6?access_token=" + token

    payload = json.dumps({
        "messages": messages,
        "extra_parameters": {"training_task_id": "meg_baiduapp_article_dialog"},
        "max_output_tokens": 2048
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    result = json.loads(response.text)
    finish_reason = result.get("finish_reason", "")
    #print(result)
    if finish_reason == "normal":
        res = result.get('result')
    return res
      
