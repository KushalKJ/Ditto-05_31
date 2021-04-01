import win32com.client as win32


class Emailer:
    def __init__(self, subject: str, recipient: str, text: str):
        self.subject = subject
        self.recipient = recipient
        self.text = text

    def send_message(self):
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.To = self.recipient
        mail.Subject = self.subject
        mail.HtmlBody = self.text  # (fin_df.head(50)).to_html()
        mail.Display(True)
        mail.send()

    def send_mail_via_com(self, profilename="Outlook2003"):
        import win32com
        s = win32com.client.Dispatch("Mapi.Session")
        o = win32com.client.Dispatch("Outlook.Application")
        s.Logon(profilename)

        Msg = o.CreateItem(0)
        Msg.To = self.recipient

        Msg.CC = "moreaddresses here"
        Msg.BCC = "address"

        Msg.Subject = self.subject
        Msg.Body = self.text

        """
        attachment1 = "Path to attachment no. 1"
        attachment2 = "Path to attachment no. 2"
        Msg.Attachments.Add(attachment1)
        Msg.Attachments.Add(attachment2)
        """
        Msg.Send()

