from .base import FunctionalTest
from .read_mail import find_email
from django.core import mail
from selenium.webdriver.common.keys import Keys
import os
import datetime
import re


SUBJECT = "Your login link for Superlists"


class LoginTest(FunctionalTest):

    def test_can_get_email_link_to_log_in(self):
        # Edith goes to the superlists site and notices a "Log in"
        # section in the navbar for the first time.
        # It's telling her to enter her email address, so she does
        if self.staging_server:
            test_email = "augusto.septimio.severo@gmail.com"
        else:
            test_email = "edith@example.com"

        self.browser.get(self.live_server_url)
        sent_time = datetime.datetime.now()
        sent_time = self.reduce_date_precision(sent_time)
        self.browser.find_element_by_name("email").send_keys(test_email)
        self.browser.find_element_by_name("email").send_keys(Keys.ENTER)

        # A message appears telling her that an email has been sent
        self.wait_for(lambda: self.assertIn(
            "Check your email",
            self.browser.find_element_by_tag_name("body").text
        ))

        # She checks her email and finds a message
        body = self.wait_for_email(test_email, SUBJECT, sent_time)

        # It has an url link in it
        self.assertIn("Use this link to log in", body)
        url_search = re.search(r"http://.+/.+$", body)
        if not url_search:
            self.fail(f"Could not find url in email body:\n{body}")
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # She clicks it
        self.browser.get(url)

        # She is logged in!
        self.wait_to_be_logged_in(email=test_email)

        # Now she logs out
        self.browser.find_element_by_link_text("Log out").click()

        # She is logged out
        self.wait_to_be_logged_out(email=test_email)

    @staticmethod
    def reduce_date_precision(date):
        return datetime.datetime(
            year=date.year,
            month=date.month,
            day=date.day,
            hour=date.hour,
            minute=date.minute,
            second=date.second,
        )

    def wait_for_email(self, test_email, subject, sent_time=None):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        creds = (test_email, os.environ["RCV_MAIL_PASS"])
        msg = find_email(creds,
                         "daniel.ibarrola.sanchez@gmail.com",
                         subject, sent_time)
        return msg.body
