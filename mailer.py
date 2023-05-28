import smtplib
import json
import csv
from email.message import EmailMessage


def main():
    # Load email credentials from JSON file
    with open("config.json") as f:
        credentials = json.load(f)

    # Read email template file
    with open('template.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        sender = lines[0].replace('FROM: ', '').strip()
        subject = lines[1].replace('SUBJECT: ', '').strip()
        body = ''.join(lines[3:]).strip()

    # Startup smtp server and send email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(credentials['username'], credentials['app_password'])

        with open('mailing_list.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            print(f"Sending mail: {subject}")
            for row in reader:
                msg = EmailMessage()
                msg['From'] = sender
                msg['To'] = row['email']
                msg['Subject'] = subject
                msg.set_content(body.replace(
                    '{firstname}', row['firstname']), charset='utf-8')

                try:
                    server.sendmail(
                        credentials['username'], row['email'], msg.as_string())
                    print("Email sent successfully to", row['email'])
                except smtplib.SMTPException as e:
                    print("Failed to send email to ",
                          row['email'], " due to ", str(e))

    print("Complete!")


if __name__ == '__main__':
    main()
