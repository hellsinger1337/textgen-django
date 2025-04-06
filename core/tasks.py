import os
from openai import OpenAI
from celery import shared_task
from django.conf import settings
from .models import Prompt, PromptContent
from mailersend import emails

@shared_task
def generate_text_task(prompt_id):
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

        mailer = emails.NewEmail(os.getenv('MAILERSEND_API_KEY'))

        mail_body = {}

        mail_from = {
            "email": os.getenv('MAILERSEND_FROM_EMAIL'),
        }

        recipients = [
            {
                "email": os.getenv('MAILERSEND_TO_EMAIL'),
            }
        ]

        mailer.set_mail_from(mail_from, mail_body)
        mailer.set_mail_to(recipients, mail_body)
        mailer.set_subject("Hello!", mail_body)
        mailer.set_html_content(generated_text, mail_body)
        mailer.set_plaintext_content(generated_text, mail_body)

        mailer.send(mail_body)

    except Exception as e:
        print(f"Error in generate_text_task for Prompt ID={prompt_id}: {e}")
        if prompt_id:
            Prompt.objects.filter(id=prompt_id).update(status=Prompt.STATUS_FAILED)
