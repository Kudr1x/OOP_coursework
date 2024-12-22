import g4f
from g4f.errors import RetryProviderError, RateLimitError

import time


def get(request, client, context=None):
    if context is None:
        context = []
    context.append({"role": "user", "content": request})

    retries = 3
    for attempt in range(retries):
        try:
            re = client.chat.completions.create(
                model=g4f.models.mistral_large,
                messages=context,
            )
            response = re.choices[0].message.content
            context.append({"role": "assistant", "content": response})
            return response, context
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