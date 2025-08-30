import yagmail
from smtplib import SMTPAuthenticationError


def send_mail(user_name, password, receiver_email, subject, html_msg):
    try:
        """Login to your gmail account"""
        yagmail.register(user_name, password)
        yag = yagmail.SMTP(user_name, password)
        """Send Email"""
        yag.send(receiver_email, subject, html_msg)
        msg = "Email sent to the recruiter successfully!"
    except SMTPAuthenticationError:
        msg = """Alert! Hi {}.As your google password is not set, the mail is by default sent by domain owner.
                It is recommended that you use gmail account and set google app password.
                Click on the Set google app password button on dashboard to set it up.""".format(
            "testaccount"
        )
    return msg
