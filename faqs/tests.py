from django.test import TestCase
from django.urls import reverse
from .models import FAQ

class FAQModelTest(TestCase):
    def setUp(self):
        self.faq = FAQ.objects.create(
            question="What is your name?",
            answer="<p>My name is Django FAQ.</p>"
        )

    def test_translation_auto_populated(self):
        # Check if auto-translation fields are populated (or fallback to English)
        self.assertTrue(self.faq.question_hi)
        self.assertTrue(self.faq.question_bn)

    def test_get_translated_question(self):
        # For English, should return original question
        self.assertEqual(self.faq.get_translated_question('en'), self.faq.question)
        # For other languages, should return translated text (or fallback to english)
        translated_hi = self.faq.get_translated_question('hi')
        self.assertIsInstance(translated_hi, str)
        translated_bn = self.faq.get_translated_question('bn')
        self.assertIsInstance(translated_bn, str)

class FAQAPITest(TestCase):
    def setUp(self):
        FAQ.objects.create(
            question="How are you?",
            answer="<p>I'm fine, thanks!</p>"
        )

    def test_api_default_language(self):
        url = reverse('faq-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Expect default language to be English (original question)
        self.assertEqual(response.data[0]['translated_question'], "How are you?")

    def test_api_hindi_language(self):
        url = reverse('faq-list') + '?lang=hi'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # The translated question should be a string (translated via googletrans)
        self.assertIsInstance(response.data[0]['translated_question'], str)
