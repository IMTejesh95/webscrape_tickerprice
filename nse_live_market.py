import requests
from bs4 import BeautifulSoup

# Emailing imports
import email
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage



watchlist = {
    'BAJFINANCE': 'https://www.tickertape.in/stocks/bajaj-finance-BJFN',
    'INFY': 'https://www.tickertape.in/stocks/infosys-INFY'
}


def get_tickerinfo(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    ticker = soup.find(class_="jsx-2256451 sidebar desktop--only")
    name = ticker.select('.ticker')[0].get_text()
    current_price = ticker.select('.current-price')[0].get_text()
    change = ticker.select('.change')[0].get_text()
    per_change = ticker.select(
        '.percentage-value')[0].get_text()[1:-1].replace('(', '')

    tickerinfo = {"symbol": name, "current_price": current_price,
                  "change": change, "percent_change": per_change}
    return tickerinfo


tickertapelist = []
for ticker in watchlist:
    tickertapelist.append(get_tickerinfo(watchlist[ticker]))


print(tickertapelist)


def notify_via_email():
    # Email configuration
    sender_email = 'tejaschauragade7@gmail.com'
    receiver_email = 'chauragade.tejesh@gmail.com'
    password = '9545223055'

    message = MIMEMultipart("alternative")
    message["Subject"] = "Ticker price updates for your watchlist!"
    message["From"] = sender_email
    message["To"] = receiver_email

    ul = """<ul class="SG">"""
    for ticker in tickertapelist:
        li = """
        <li class="sgLi">
            <div class="box">
            <h3>{0}</h3>
            <ul class="df">
            <li>Current Price : {1}</li>
            <li>Change : {2} ( {3} )</li>
            </ul>
            </div>
        </li>"""
        li.format(ticker['symbol'], ticker['current_price'],
                  ticker['change'], ticker['percent_change'])
    ul = ul + """</ul>"""


    html = """
    <html>
    <body>
        <h3>Dear Sir,</h3>
        <p style="font-size:16px;">
        We hope you are doing great!<br>
    """

    html = html + ul

    html = html + """
    </body>
    </html>
    """

    body = MIMEText(html, "html")

    try:
        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server: 
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
    except Exception as e:
        print(e)


notify_via_email()

