from django.db import models
from ckeditor.fields import RichTextField
from django.core.cache import cache
from googletrans import Translator

translator = Translator()  # Initialize the translator

class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()
    # Optional language-specific translations for the question
    question_hi = models.TextField(blank=True, null=True)
    question_bn = models.TextField(blank=True, null=True)
    
    def get_translated_question(self, lang_code):
        """
        Returns the question in the specified language.
        It first checks if a manual translation exists,
        then caches and returns the result (automatically translating if needed).
        """
        cache_key = f'faq_{self.pk}_question_{lang_code}'
        translated = cache.get(cache_key)
        if translated:
            return translated

        # If manual translation exists, use it
        if lang_code == 'hi' and self.question_hi:
            translated = self.question_hi
        elif lang_code == 'bn' and self.question_bn:
            translated = self.question_bn
        else:
            # Use Google Translate API to translate the English question
            try:
                translation = translator.translate(self.question, dest=lang_code)
                translated = translation.text
            except Exception:
                # Fallback to English if translation fails
                translated = self.question

        # Cache the translated text for 1 hour (3600 seconds)
        cache.set(cache_key, translated, timeout=3600)
        return translated

    def save(self, *args, **kwargs):
        """
        Override save() to auto-populate translation fields if they are empty.
        """
        # Auto-translate to Hindi if not provided
        if not self.question_hi:
            try:
                self.question_hi = translator.translate(self.question, dest='hi').text
            except Exception:
                self.question_hi = self.question  # Fallback to English

        # Auto-translate to Bengali if not provided
        if not self.question_bn:
            try:
                self.question_bn = translator.translate(self.question, dest='bn').text
            except Exception:
                self.question_bn = self.question  # Fallback to English

        super().save(*args, **kwargs)

    def __str__(self):
        return self.question
