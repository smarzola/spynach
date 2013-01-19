import sys, cgitb
import email, mimetools, cStringIO
import smtplib

__all__ = ['create_mail', 'send_mail', 'send_traceback']

def create_mail(sender, recipient, subject, html, text):
    out = cStringIO.StringIO()
    htmlin = cStringIO.StringIO(html)
    txtin = cStringIO.StringIO(text)

    writer = MimeWriter.MimeWriter(out)
    writer.addheader("From", sender)
    writer.addheader("To", recipient)
    writer.addheader("Subject", subject)
    writer.addheader("MIME-Version", "1.0")
    writer.startmultipartbody("alternative")
    writer.flushheaders()

    subpart = writer.nextpart()
    subpart.addheader("Content-Transfer-Encoding", "quoted-printable")
    pout = subpart.startbody("text/plain", [("charset", 'us-ascii')])
    mimetools.encode(txtin, pout, 'quoted-printable')
    txtin.close()

    subpart = writer.nextpart()
    subpart.addheader("Content-Transfer-Encoding", "quoted-printable")

    pout = subpart.startbody("text/html", [("charset", 'us-ascii')])
    mimetools.encode(htmlin, pout, 'quoted-printable')
    htmlin.close()
    writer.lastpart()
    msg = out.getvalue()
    out.close()
    return msg

def send_mail(sender, recipient, subject, html, text):
    message = create_mail(sender, recipient, subject, html, text)
    server = smtplib.SMTP("localhost")
    server.sendmail(sender, recipient, message)
    server.quit()

def format_traceback():
    return cgitb.html(sys.exc_info())

def send_traceback(mail_from, mail_to):
    try:
        send_mail(mail_from, mail_to, 'Artichoke Exception',
                  format_traceback(), cgitb.text(sys.exc_info()))
    except:
        print 'Failed to connect to SMTP'
