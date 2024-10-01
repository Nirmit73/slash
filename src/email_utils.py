"""
This file is responsible for sending emails to the user if
they choose to have an email sent. The email contains all
of the results from their SLASH search.
"""

import tempfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename
from email.mime.text import MIMEText
from email.utils import formatdate
import csv


def send_html_email(email_from=None,
                    email_to=None,
                    email_cc=None,
                    email_bcc=None,
                    email_subject=None,
                    text_body=None,
                    attachments=None):
    """
        function will send mail in html format

        :param email_from: Sender email id
        :param email_to: email id of person in To
        :param email_cc: email id of person in Cc
        :param email_bcc: email id of person in Bcc
        :param email_subject: subject of email
        :param text_body: Body of mail (in html)
        :param attachments: file path of attachment
        :return: None
    """

    msg = MIMEMultipart()
    msg['Subject'] = email_subject
    msg.add_header('From', email_from)
    msg.add_header('To', email_to)
    msg.add_header('cc', email_cc)
    msg.add_header('bcc', email_bcc)
    msg.attach(MIMEText(text_body, 'html'))

    if attachments is not None:
        for f in attachments:
            with open(f, "rb") as fil:
                part = MIMEApplication(fil.read(), Name=basename(f))
            # After the file is closed
            part[
                'Content-Disposition'] = 'attachment; filename="%s"' % basename(
                    f)
            msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(email_from, 'phxszsraydbwhqek')

    email_combiner = list()

    if email_to and ',' in email_to:
        email_combiner.append(email_to.split(','))
    elif email_to:
        email_combiner.append(email_to)

    if email_cc and ',' in email_cc:
        email_combiner.append(email_cc.split(','))
    elif email_cc:
        email_combiner.append(email_cc)

    if email_bcc and ',' in email_bcc:
        email_combiner.append(email_bcc.split(','))
    elif email_bcc:
        email_combiner.append(email_bcc)
    server.sendmail(email_from, email_combiner[0], msg.as_string())
    server.close()


def text_table_to_html(file, header):
    """
        function will convert text table to html table

        :param file: input data
        :param header: header name (list)
        :return: html table
    """
    style = """
                <head>
                <style>
                #customers {
                font-family: Verdana, Helvetica, sans-serif;
                border-collapse: collapse;
                width: 100%;
                }

                #customers td, #customers th {
                border: 2px solid #000;
                padding: 8px;
                }

                #customers tr:nth-child(even){background-color: #f2f2f2;}

                #customers tr:hover {background-color: #ddd;}

                #customers th {
                padding-top: 12px;
                padding-bottom: 12px;
                text-align: left;
                background-color: #04AA6D;
                color: white;
                }
                </style>
                </head>
            """
    body = """
            <body>
            <pre id="customers">
Hi There,

    Here is a preview of the your query results from slash. Please find more details in the attached csv file.
            <pre>
            """
    table_head = style + body + "<table id='customers'><tr>"
    for head in header:
        table_head += "<th>{}</th>".format(head.title())
    table_head += "</tr>"

    table_body = ""

    csv_file = open(file, 'r')
    reader = csv.reader(csv_file, delimiter='\t')
    for idx, row in enumerate(reader):
        if idx == 0:
            continue
        if idx == 15:
            break
        table_body += '\n\n' + "<tr>"

        for col in row:
            table_body += "<td>{}</td>".format(col.title())

        table_body += "</tr>"

    table_foot = "</table>"
    body_end = """
            <pre id="customers">
Thanks,
Team Slash.
            </pre>
            </body>
            """

    return table_head + table_body + table_foot + body_end


def alternateMerge(listToMerge):
    """
    Alternate merging the list of products.
    :param listToMerge: list of lists for different websites.
    return: merged list
    """
    maxLength = len(listToMerge[0])
    mergedList = []
    for each in listToMerge[1:]:
        maxLength = max(maxLength, len(each))
    idx = 0
    while idx < maxLength:
        for each in listToMerge:
            if idx < len(each):
                mergedList.append(each[idx])
        idx += 1
    return mergedList


def write_data(results, linkFlag, receiver_emails):
    """
    Write data and publish it.
    :param results: results data from the search queries.
    :param receiver_emails: list of comma separated emails.
    return: None
    """
    if len(results) == 0:
        print("No results found for the search query. Hence no email on it")
        return
    if len(receiver_emails) == 0:
        print("No email to send data. Hence not sending the email")
        return
    fieldnames = [
        'title', 'website', 'price', 'rating', 'ratingCount', 'timestamp',
        'link'
    ] if linkFlag else [
        'timestamp', 'title', 'price', 'website', 'rating', 'ratingCount'
    ]
    tempFile = tempfile.NamedTemporaryFile(delete=False)
    try:
        with open(tempFile.name, "w+t") as f:
            writer = csv.DictWriter(f, delimiter='\t', fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        f.close()
        email_text = text_table_to_html(tempFile.name, fieldnames)
        send_html_email(email_from="vishnuchalla47@gmail.com",
                        email_to=receiver_emails,
                        email_subject="Slash execution results",
                        text_body=email_text,
                        attachments=[tempFile.name])
    except Exception as e:
        raise Exception("Error while sending the email. Error:- " + str(e))
    finally:
        tempFile.close()
