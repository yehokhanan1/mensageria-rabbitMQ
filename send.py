import pika
import os
import smtplib
from datetime import datetime, timezone
from email.message import EmailMessage

# conectando ao rabbitMQ
credentials = pika.PlainCredentials('******', '******')
parameters = pika.ConnectionParameters(host='**.***.***.**', port='****', credentials=credentials, heartbeat=0)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

def Email(info, error):
    with open("pass.txt", 'r') as Pass:
        password = Pass.read()
    # endereços de e-mails e assunto
    EmailAddress = '********10@gmail.com'
    msg = EmailMessage()
    msg['Subject'] = '[ ATLANTIC ] - PEDIDO DE ESTORNO'
    msg['From'] = EmailAddress
    msg['To'] = '**********@gmail.com'
    # formatação da data
    date = info["payment_date"]
    dateTimes = datetime.fromisoformat(date)
    data = '{}/{}/{}'.format(dateTimes.day,dateTimes.month,dateTimes.year)
    hora = '{}:{} UTC-03:00'.format(dateTimes.hour,dateTimes.minute)
    # corpo da mensagem
    msg.set_content(f'''

                        TOKEN: {info["client_token"]}
                        DATA DA VENDA: {data} Hora {hora}
                        VALOR DA VENDA: R${info["amount"]}
                        CODIGO DE AUTORIZAÇÃO: {info["authorization_code"]}
                        VALOR DO CANCELAMENTO: R${info["amount_charge_back"]}''')
    try:
        # conectando e enviando os e-mails
        with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
            smtp.login(EmailAddress, password)
            smtp.send_message(msg)
    except:
        # verificação de error
        Error(error)

def Error(errou):
    channel.basic_publish(exchange='', routing_key='QueuePaymentChargebackError', body=errou)