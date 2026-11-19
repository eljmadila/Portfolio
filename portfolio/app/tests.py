from smtplib import SMTPException

from django.core import mail
from django.core.mail.backends.base import BaseEmailBackend
from django.template.loader import render_to_string
from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse

from .models import ContactMessage, Service


class ContactFormComponentTests(SimpleTestCase):
    def test_renders_complete_project_inquiry_form_and_home_anchor(self):
        rendered = render_to_string(
            "components/forms/contact_form.html",
            {
                "form_action": "/",
                "form_anchor": "contact",
                "form_title": "Send a Project Brief or Inquiry",
                "submit_label": "Send Message",
            },
        )

        self.assertIn('action="/#contact"', rendered)
        self.assertIn('id="id_company" name="company"', rendered)
        self.assertIn('id="id_service" name="service"', rendered)
        self.assertIn('id="id_budget" name="budget"', rendered)
        self.assertIn('id="id_timeline" name="timeline"', rendered)
        self.assertIn('id="id_message" name="message"', rendered)
        self.assertIn("<span>Send Message</span>", rendered)

    def test_renders_contact_page_action_without_an_anchor(self):
        rendered = render_to_string(
            "components/forms/contact_form.html",
            {
                "form_action": "/contact",
                "form_title": "Send a Project Brief or Inquiry",
                "submit_label": "Send Inquiry",
            },
        )

        self.assertIn('action="/contact"', rendered)
        self.assertNotIn('action="/contact#', rendered)
        self.assertIn("<span>Send Inquiry</span>", rendered)


class FailingEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        raise SMTPException("Test email failure")


@override_settings(
    MAILERS={
        "default": {
            "BACKEND": "django.core.mail.backends.locmem.EmailBackend",
        }
    }
)
class ContactSubmissionTests(TestCase):
    def setUp(self):
        mail.outbox = []
        self.service = Service.objects.create(
            title="Full-Stack Web Development",
            description="Build web applications",
        )
        self.payload = {
            "name": "Test Sender",
            "email": "sender@example.com",
            "company": "Example Co",
            "service": str(self.service.pk),
            "budget": "150-500",
            "timeline": "immediate",
            "message": "Please contact me about a project.",
        }

    def test_contact_submission_saves_message_and_sends_email(self):
        response = self.client.post(reverse("contact"), self.payload)

        self.assertRedirects(response, reverse("contact"), fetch_redirect_response=False)
        saved_message = ContactMessage.objects.get(email=self.payload["email"])
        self.assertEqual(saved_message.company, "Example Co")
        self.assertEqual(saved_message.service, self.service)
        self.assertEqual(saved_message.budget, "150-500")
        self.assertEqual(saved_message.timeline, "immediate")

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["madilaelyamine@gmail.com"])
        self.assertEqual(mail.outbox[0].reply_to, [self.payload["email"]])
        self.assertIn(self.service.title, mail.outbox[0].body)
        self.assertIn(self.payload["message"], mail.outbox[0].body)

    def test_home_submission_saves_and_sends_email(self):
        response = self.client.post(reverse("home"), self.payload)

        self.assertRedirects(response, "/#contact", fetch_redirect_response=False)
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)

    @override_settings(
        MAILERS={
            "default": {
                "BACKEND": "app.tests.FailingEmailBackend",
            }
        }
    )
    def test_email_failure_is_logged_and_reported_after_saving_message(self):
        with self.assertLogs("app.views", level="ERROR"):
            response = self.client.post(reverse("contact"), self.payload)

        self.assertRedirects(response, reverse("contact"), fetch_redirect_response=False)
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 0)
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any("email notification could not be sent" in str(message) for message in messages))
