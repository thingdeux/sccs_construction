from django.test import TestCase
from quotes.models import Quote


class WebTemplateTests(TestCase):
    """Various Tests for the /thanks redirect page after posting
    a quote from the /quote/ page"""
    def test_thanks_with_string_value_less_than_limit(self):
        """Test with a proper string less than 254 characters"""
        response = self.client.get('/thanks/', {'r': 'Josh'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quotes/thanks.html')
        self.assertContains(response, 'Josh')

    def test_thanks_with_string_value_greater_than_limit(self):
        """Test with a proper string greater than 254 (300) characters
           -Had to remove all of the newline characters in order to create
           the long string and keep with PEP8"""
        string_to_pass = """1234567891123456789112345678911234567891
        123456789112345678911234567891123456789112345678911234567891
        123456789112345678911234567891123456789112345678911234567891
        123456789112345678911234567891123456789112345678911234567891
        123456789112345678911234567891123456789112345678911234567891
        12345678911234567891""".replace("\n", "").replace("        ", "")
        string_to_test = """1234567891123456789112345678911234567891
        123456789112345678911234567891123456789112345678911234567891
        123456789112345678911234567891123456789112345678911234567891
        123456789112345678911234567891123456789112345678911234567891
        1234567891123456789112345678911234""".replace("\n", "").replace("        ", "")  # noqa
        response = self.client.get('/thanks/', {'r': string_to_pass})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quotes/thanks.html')

        self.assertContains(response, string_to_test)

    def test_thanks_with_empty_string_value(self):
        """Test with an empty name value"""
        response = self.client.get('/thanks/', {'r': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quotes/thanks.html')

    def test_thanks_with_no_passed_string(self):
        """Test with no passed value - should return 404"""
        response = self.client.get('/thanks/')
        self.assertEqual(response.status_code, 404)

    """Tests for basic url-endpoints template renders"""
    def test_index_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('quotes/index.html')

    def test_services_view(self):
        response = self.client.get('/services/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quotes/services.html')

    def test_aboutus_view(self):
        response = self.client.get('/aboutus/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quotes/aboutus.html')


class QuoteSubmissiontests(TestCase):
    """Test Quote submission / URL interactions"""
    def test_quote_get_view(self):
        response = self.client.get('/quote/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quotes/submitQuote.html')

    def test_quote_post_with_succesful_values(self):
        response = self.client.post('/quote/', {
            'first_name': "Josh",
            'last_name': "Johnson",
            'email': "test@gmail.com",
            'phone': '123567',
            'comments': 'This is just a test comment'
            })
        # Test that the redirect happened and the status code 302 was received
        self.assertRedirects(response, '/thanks/?r=Josh',
                             status_code=302, target_status_code=200)
        # Make sure the e-mail templates are called
        self.assertTemplateUsed(response, 'quotes/email_html.html')
        self.assertTemplateUsed(response, 'quotes/email_text.html')
        new_record = Quote.objects.get(pk=1)

        # Test that the newly created DB record matches the post info
        self.assertEqual(new_record.first_name, 'Josh')
        self.assertEqual(new_record.last_name, 'Johnson')
        self.assertEqual(new_record.email, 'test@gmail.com')
        self.assertEqual(new_record.phone, '123567')
        self.assertEqual(new_record.comments, 'This is just a test comment')

    def test_quote_post_with_unsuccesful_values(self):
        """You should not be able to submit a request without values
        In first_name / last_name / email / comments"""
        response = self.client.post('/quote/', {
            'first_name': "",
            'last_name': "Johnson",
            'email': "test@gmail.com",
            'phone': '',
            'comments': 'This is just a test comment'
            })
        self.assertEqual(response.status_code, 200)
        # Should redirect back to the quote template with errors
        self.assertTemplateUsed(response, 'quotes/submitQuote.html')
        self.assertContains(response, "This field is required")
        new_record = Quote.objects.all()
        # No DB Record was created
        self.assertEqual(len(new_record), 0)

    def test_quote_post_without_all_required_values(self):
        # Missing email and phone (e-mail is required)
        response = self.client.post('/quote/', {
            'first_name': "Johnson",
            'last_name': "Johnson",
            'comments': 'This is just a test comment'
            })
        self.assertTemplateUsed(response, 'quotes/submitQuote.html')
        self.assertContains(response, "This field is required")

    def test_quote_post_without_one_value(self):
        # Missing email and phone (e-mail is required)
        response = self.client.post('/quote/', {
            'first_name': "Josh",
            'last_name': "Johnson",
            'email': 'test@gmail.com',
            'comments': 'This is just a test comment'
            })

        # Test that the redirect happened and the status code 302 was received
        self.assertRedirects(response, '/thanks/?r=Josh', status_code=302,
                             target_status_code=200)
        # Make sure the e-mail templates are called
        self.assertTemplateUsed(response, 'quotes/email_html.html')
        self.assertTemplateUsed(response, 'quotes/email_text.html')
        new_record = Quote.objects.get(pk=1)

        # Test that the newly created DB record matches the post info
        self.assertEqual(new_record.first_name, 'Josh')
        self.assertEqual(new_record.last_name, 'Johnson')
        self.assertEqual(new_record.email, 'test@gmail.com')
        self.assertEqual(new_record.comments, 'This is just a test comment')
