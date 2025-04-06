from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .tasks import generate_text_task

from .models import Prompt
from .serializers import PromptSerializer

class PromptViewSet(viewsets.ModelViewSet):
    queryset = Prompt.objects.all().select_related('content')
    serializer_class = PromptSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        prompt = serializer.save()  

        generate_text_task.delay(prompt.id)
        
        return Response(
            self.get_serializer(prompt).data,
            status=status.HTTP_201_CREATED
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        prompt = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = self.get_serializer(prompt)
        return Response(serializer.data)