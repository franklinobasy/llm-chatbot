from typing import Annotated, Any, List

import pandas as pd
import win32com.client


def get_outlook_emails(
    sender_email: Annotated[str, "The sender's email"]
) -> List:
    outlook = win32com.client.Dispatch("Outlook.Application")\
        .GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)

    # Access the items (emails) in the inbox
    items = inbox.Items

    filtered_items = []

    # Loop through the items and filter by sender email
    for item in items:
        if item.SenderEmailAddress == sender_email:
            filtered_items.append(item)

    return filtered_items


def export_sender_email(
    emails: Annotated[List[Any], "List of all emails from sender"],
    file_path: Annotated[str, "Path to export file"] = None,
    format: Annotated[str, "Format of export file"] = "csv"
) -> None:
    supported_filetypes = {
        'txt': 'txt',
        'csv': 'csv',
        'xlxs': 'excel'
    }
    if format not in supported_filetypes.keys():
        message = f"The specified format type: {format}, is not supported." + \
            f"Only supports - {supported_filetypes.keys()}"
        raise ValueError(
            message
        )

    if not file_path:
        file_path = str(emails[0].SenderEmailAddress).split("@")[0]

    if file_path.split(".")[-1] not in supported_filetypes.keys():
        file_path = f"{file_path}.{format}"

    if format == 'txt':
        output = f"Emails from {emails[0].SenderEmailAddress}\n"
        for email in emails:
            output += f"Subject: {email.Subject}\n"
            output += f"Received Time: {email.ReceivedTime}\n"
            output += f"Sender Email: {email.SenderEmailAddress}\n"
            output += f"Body: {email.Body}\n"
            output += "" * 50

        with open(file_path, "w") as file_object:
            file_object.write(output)

    else:
        data = {
            'Subject': [],
            'Time Received': [],
            'Content': []
        }

        for email in emails:
            data['Subject'].append(email.Subject)
            data['Time Received']\
                .append(email.ReceivedTime.strftime(r'%Y-%m-%d %H:%M:%S'))
            data["Content"].append(email.Body)

        data = pd.DataFrame(data)
        # Export
        code = f"data.to_{supported_filetypes[format]}(\"{file_path}\")"
        eval(code)
