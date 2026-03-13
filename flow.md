```python
from anthropic import Anthropic
from dotenv import load_dotenv
import os
import sys
import json

load_dotenv(override=True)

if __name__ == "__main__":
    client = Anthropic(base_url=os.getenv("ANTHROPIC_BASE_URL"), api_key=os.getenv("ANTHROPIC_API_KEY"))
    MODEL = os.getenv("MODEL_ID")
    print(f"Model: {MODEL}")

    if len(sys.argv) > 1:
        # noinspection PyTypeChecker
        response = client.messages.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": sys.argv[1]}
            ],
            max_tokens=200,
        )
        print(json.dumps(response.to_dict(), indent=2, ensure_ascii=False))

```