from tools.gmail_tool import send_email


def email_summary(recipient, summary):

    subject = "PilotOS AI Research Summary"

    send_email(
        recipient,
        subject,
        summary
    )

    return "Email sent successfully."