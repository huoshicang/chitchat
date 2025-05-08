from typing import List


def transition_message(data: List[dict]) -> List[dict]:
    for index, item in enumerate(data):
        if 'id' in item:
            new_dict = {
                "role": item.get("choices", [{}])[0].get("delta", {}).get("role", ""),
                "content": item.get("choices", [{}])[0].get("delta", {}).get("content", "")
            }
            data[index] = new_dict

    return data