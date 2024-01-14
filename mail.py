import smtplib
from email.mime.text import MIMEText
from socket import gaierror

import exception


class Mail:
    def __init__(self, domain: str, port: int, acc: str, pwd: str):
        self.mail_server = self.init_smtp_server(domain, port, acc, pwd)

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.mail_server.quit()

    def init_smtp_server(
        self, domain: str, port: int, account: str, password: str
    ) -> smtplib.SMTP:
        server = self.__check_domain_alive(domain, port)
        server.starttls()
        server = self.__check_acc_pwd_valid(server, account, password)
        return server

    def __check_domain_alive(self, domain: str, port: int) -> smtplib.SMTP:
        try:
            server = smtplib.SMTP(domain, port, timeout=3)
        except gaierror:
            raise exception.DomainError(
                f"Domain: {domain} is incorrect, please check again.", 404
            )
        except TimeoutError:
            raise exception.DomainError(
                f"Domain: {domain} with port: {port} is not alive, please check again.",
                404,
            )
        return server

    def __check_acc_pwd_valid(
        self, server: smtplib.SMTP, account: str, password: str
    ) -> smtplib.SMTP:
        try:
            server.login(account, password)
        except smtplib.AccountPasswordError as e:
            raise exception.AccountPasswordError(
                f"Account: {account} with password: {password} is incorrect, for more info, please read the error message {e}.",
                404,
            )
        return server

    def send(
        self, receiver: str, title: str, message: str, content_type: str = "text/plain"
    ) -> None:
        if content_type == "text/plain":
            self.send_mail_with_text(receiver, title, message)

    def send_mail_with_text(self, receiver: str, title: str, message: str) -> None:
        sender = self.mail_server.user
        text = MIMEText(message, "plain", "utf-8")
        text["Subject"] = title
        text["From"] = sender
        text["To"] = receiver
        self.mail_server.sendmail(sender, receiver, text.as_string())
