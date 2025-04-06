from rest_framework import serializers
from .models import Prompt, PromptContent

class PromptContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromptContent
        fields = ['id', 'output_text', 'created_at']


class PromptSerializer(serializers.ModelSerializer):
    content = PromptContentSerializer(read_only=True)

    class Meta:
        model = Prompt
        fields = [
            'id',
            'title',
            'input_text',
            'status',
            'created_at',
            'updated_at',
            'content',
        ]
        read_only_fields = ['status', 'created_at', 'updated_at', 'content']