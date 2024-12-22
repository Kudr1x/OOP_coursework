import g4f
from g4f.errors import RetryProviderError, RateLimitError, ModelNotFoundError
import time

class chatBot():

    def set_context(self, request, context=None):
        if context is not None:
            context.append({"role": "user", "content": request})
            return context

        context = [{"role": "user", "content": request}]
        return context

    def add_to_context(self, context, full_response):
        context.append({"role": "model", "content": full_response.choices[0].message.content})
        return context

    def get_last_response(self, full_response):
        return full_response.choices[0].message.content

    def get_response(self, request, client, current_model, context=None):
        context = self.set_context("ПИШИ ВСЕГДА НА РУССКОМ" + request, context)

        retries = 3
        for attempt in range(retries):
            try:
                if context is None or len(context) == 0:
                    context = [{"role": "user", "content": request}]

                full_response = client.chat.completions.create(
                    model=current_model,
                    messages= context,
                )
                context = self.add_to_context(context, full_response)

                return self.get_last_response(full_response), context

            except RateLimitError:
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    raise
            except UnicodeDecodeError as e:
                print(f"Unicode decode error: {e}")
                return "An error occurred while processing your request.", context
            except RetryProviderError as e:
                print(f"Retry provider error: {e}")
                return "An error occurred while processing your request.", context
            except ModelNotFoundError as e:
                print(f"Model not found error: {e}")
                return "The specified model was not found.", context