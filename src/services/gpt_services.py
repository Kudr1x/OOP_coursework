import g4f
from g4f.errors import RetryProviderError, RateLimitError
import time

class chatBot():

    def reset_context(self, context):
        context = None

    def set_context(self, request, context=None):
        if context is not None:
            return context.append({"role": "user", "content": request})

        context = [{"role": "user", "content": request}]
        return context

    def add_to_context(self, context, full_response):
        return context.append({"role": "assistant", "content": full_response.choices[0].message.content})

    def get_last_resonse(self, full_response):
        return full_response.choices[0].message.content

    def get_response(self, request, client, current_model=g4f.models.mistral_large, context=None):
        context = self.set_context(request, context)

        retries = 3
        for attempt in range(retries):
            try:
                full_response = client.chat.completions.create(
                    model=current_model,
                    messages=context,
                )
                context = self.add_to_context(context, full_response)

                return self.get_last_resonse(full_response), context

            except RateLimitError:
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    raise
            except UnicodeDecodeError as e:
                print(f"Unicode decode error: {e}")
                return "An error occurred while processing your request."
            except RetryProviderError as e:
                print(f"Retry provider error: {e}")
                return "An error occurred while processing your request."
