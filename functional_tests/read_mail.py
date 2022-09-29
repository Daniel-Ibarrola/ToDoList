import imaplib
import email
import datetime
import time


class Message:

    def __init__(self, date, subject, body=""):
        self.date = date
        self.subject = subject
        self.body = body

    def __str__(self):
        return f"Date: {self.date}\n"\
               f"Subject: {self.subject}\n"\
               f"Body: {self.body}\n"


months = {
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}


def email_date_to_datetime(date_str):
    """ Transforms a string to a datetime object. """
    date_parts = date_str.split()
    day = int(date_parts[1])
    month = months[date_parts[2].lower()]
    year = int(date_parts[3])
    full_hour = date_parts[4].split(":")
    hour = int(full_hour[0])
    min = int(full_hour[1])
    second = int(full_hour[2])

    return datetime.datetime(year, month, day, hour, min, second)


def find_email(credentials, sender, subject, sent_time):
    """ Find emails of the given sender, with the given subject, that
        arrived at least at sent time.
    """

    user, password = credentials

    host = 'imap.gmail.com'
    email_data = []
    start_time = time.time()
    while time.time() - start_time < 80:

        mail = imaplib.IMAP4_SSL(host)
        mail.login(user, password)
        mail.select("INBOX")
        _, selected_mails = mail.search(None, f'FROM "{sender}"')
        selected_mails = selected_mails[0].split()
        for num in selected_mails:
            _, data = mail.fetch(num, '(RFC822)')
            _, bytes_data = data[0]
            # convert the byte data to message
            email_message = email.message_from_bytes(bytes_data)

            if subject in email_message["subject"]:

                date = email_date_to_datetime(email_message["date"])
                if date >= sent_time:

                    msg = Message(date=date,
                                  subject=email_message["subject"])
                    for part in email_message.walk():
                        if part.get_content_type() == "text/plain" or part.get_content_type() == "text/html":
                            body = part.get_payload(decode=True)
                            msg.body = body.decode()
                            break

                    email_data.append(msg)
        if len(email_data) > 0:
            break
        time.sleep(5)

    if len(email_data) == 0:
        return

    email_data.sort(key=lambda x: x.date)
    return email_data[-1]
