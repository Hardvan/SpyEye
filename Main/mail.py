import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Mail sent to : treemusketeers32@gmail.com
# Password : Dhootkilillyput
# Mail sent from : spyeyemusk42@gmail.com
# Password : Dhootkilillyput


# Setup port number and server name
smtp_port = 587                 # Standard secure SMTP port
smtp_server = "smtp.gmail.com"  # Google SMTP Server

# Set up the email lists
email_from = "spyeyemusk42@gmail.com"


# Define the password (better to reference externally)
# As shown in the video this password is now dead, left in as example only
pswd = "dosi juxf dbjx mgeb"


# name the email subject
subject = "Test Mail: Intruder Detected"


# Define the email function (dont call it email!)
def send_emails(filename):

    group_mail = "treemusketeers32@gmail.com"
    hardik_mail = "hardikhpawar.cs21@rvce.edu.in"
    abhishek_mail = "abhishekyadav.cs21@rvce.edu.in"
    harshit_mail = "harshitdhoot.cs21@rvce.edu.in"
    karan_mail = "karansathish.cs21@rvce.edu.in"

    email_list = [hardik_mail]

    for person in email_list:

        # Make the body of the email
        body = """
        Dear Team,

        We have detected a recent intrusion, and we wanted to inform you immediately.
        Attached to this email is a picture of the intruder for your reference.

        If you have any concerns or need further information, please don't hesitate to reach out.
        
        PS: This is a test email. No action is required from your side.

        Best regards,
        SpyEye Team
        """

        # make a MIME object to define parts of the email
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = person
        msg['Subject'] = subject

        # Attach the body of the message
        msg.attach(MIMEText(body, 'plain'))

        # Open the file in python as a binary
        attachment = open(filename, 'rb')  # r for read and b for binary

        # Encode as base 64
        attachment_package = MIMEBase('application', 'octet-stream')
        attachment_package.set_payload((attachment).read())
        encoders.encode_base64(attachment_package)
        attachment_package.add_header(
            'Content-Disposition', "attachment; filename= " + filename)
        msg.attach(attachment_package)

        # Cast as string
        text = msg.as_string()

        # Connect with the server
        print("Connecting to server...")
        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        TIE_server.starttls()
        TIE_server.login(email_from, pswd)
        print("Succesfully connected to server")
        print()

        # Send emails to "person" as list is iterated
        print(f"Sending email to: {person}...")
        TIE_server.sendmail(email_from, person, text)
        print(f"✅ Email sent to: {person}")
        print()

    # Close the port
    TIE_server.quit()
