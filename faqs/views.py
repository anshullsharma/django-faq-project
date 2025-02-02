from rest_framework import generics
from .models import FAQ
from .serializers import FAQSerializer

class FAQListAPIView(generics.ListAPIView):
    serializer_class = FAQSerializer
    queryset = FAQ.objects.all()

    def get_serializer_context(self):
        # Pass the language code from the query parameter to the serializer
        context = super().get_serializer_context()
        context['lang'] = self.request.query_params.get('lang', 'en')
        return context
