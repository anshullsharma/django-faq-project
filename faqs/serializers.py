from rest_framework import serializers
from .models import FAQ

class FAQSerializer(serializers.ModelSerializer):
    translated_question = serializers.SerializerMethodField()

    class Meta:
        model = FAQ
        fields = ['id', 'translated_question', 'answer']

    def get_translated_question(self, obj):
        # Get language from serializer context (passed from the view)
        lang = self.context.get('lang', 'en')
        # For English, return the original question
        if lang == 'en':
            return obj.question
        return obj.get_translated_question(lang)
