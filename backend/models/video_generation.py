import requests

def generate_video(token, prompt):
    url = "https://api.rhymes.ai/v1/generateVideoSyn"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "refined_prompt": prompt,
        "num_step": 100,
        "cfg_scale": 7.5,
        "user_prompt": prompt,
        "rand_seed": 12345
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}