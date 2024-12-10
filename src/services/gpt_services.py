import g4f
from g4f import client, Client
from g4f.errors import RetryProviderError, RateLimitError

import time

client = Client()

def get(s):
    retries = 3
    for attempt in range(retries):
        try:
            re = client.chat.completions.create(
                model=g4f.models.gemini_pro,
                messages=[{"role": "user", "content": s}],
            )
            print(re.choices[0].message.content)
            return re.choices[0].message.content
        except RateLimitError:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise
        except UnicodeDecodeError as e:
            print(f"Unicode decode error: {e}")
            return "An error occurred while processing your request."
        except RetryProviderError as e:
            print(f"Retry provider error: {e}")
            return "An error occurred while processing your request."