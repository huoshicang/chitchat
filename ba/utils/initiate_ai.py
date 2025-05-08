import json
from typing import List

from openai import OpenAI
from fastapi import WebSocket
from utils import ws_send_response


async def initiate_ai(ai_config: dict, model_config: dict, websocket: WebSocket ) -> List[dict]:

    completion = OpenAI(**ai_config).chat.completions.create(**model_config)

    data = {
        "reasoning_content": "",
        "content": ""
    }

    for chunk in completion:
        chunk_data = json.loads(chunk.model_dump_json())
        choice = chunk_data.get('choices', [{}])[0]
        finish_reason = choice.get('finish_reason')

        delta = choice.get("delta", {})
        reasoning_content = delta.get('reasoning_content')
        content = delta.get('content')

        if reasoning_content is not None:
            data['reasoning_content'] += reasoning_content
        elif content is not None:
            data['content'] += content

        if finish_reason == 'stop':
            if data['reasoning_content']:
                chunk_data['choices'][0]['delta']['reasoning_content'] = data['reasoning_content']
            chunk_data['choices'][0]['delta']['content'] = data['content']
            return chunk_data
        else:
            await ws_send_response(websocket, chunk_data)




# initiate_ai(ai_config={}, model_config={})
