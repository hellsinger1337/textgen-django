import os
from openai import OpenAI
from celery import shared_task
from django.conf import settings
from .models import Prompt, PromptContent

@shared_task
def generate_text_task(prompt_id):
    """
    Асинхронная задача для генерации текста
    через OpenAI. Меняет статус Prompt на PROCESSING,
    затем на COMPLETED/FAILED.
    """
    try:
        prompt = Prompt.objects.get(id=prompt_id)
        prompt.status = Prompt.STATUS_PROCESSING
        prompt.save()

        client = OpenAI()

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt.input_text
                }
            ]
        )
        generated_text = completion.choices[0].message.content

        PromptContent.objects.create(
            prompt=prompt,
            output_text=generated_text
        )

        prompt.status = Prompt.STATUS_COMPLETED
        prompt.save()

    except Exception as e:
        print(f"Error in generate_text_task for Prompt ID={prompt_id}: {e}")
        if prompt_id:
            Prompt.objects.filter(id=prompt_id).update(status=Prompt.STATUS_FAILED)
