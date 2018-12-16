#! /usr/bin/env python 

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Email(object):
    def __init__(self, santa=False, child=False, to_address=False, debug=False,
                 from_address='alittlegnome@gmail.com'):

        self.subject = 'You\'re a Secret Santa {0}!!'.format(santa)
        self.from_address = from_address 
        self.to_address = to_address
        self.santa = santa
        self.child = child
        self.price_limit = '25' 
        self.debug = debug

        self.debug_text = '' \
            '********************************************\n' \
    		'**** THIS IS JUST A TEST, PLEASE DELETE! ****\n' \
    		'*********************************************\n'
    
        self.debug_html = '' \
            '<p>*********************************************<br>' \
    		'**** THIS IS JUST A TEST, PLEASE DELETE! ****<br>' \
    		'*********************************************<br><br>'
    
        self.text = 'Hello my little Elf,\n\nCongratulations {0}! You are ' \
                'Secret Santa for: {1}.\n\nThe price limit is: ${2}\n\n' \
                ' - Kris Kringle\n'.format(self.santa, self.child, 
                                           self.price_limit)
        
        self.html1 = '<html><head></head><body><font face="courier"><p>Hello' \
                ' my little Elf,<br></p>'
        
        self.html2 = 'Congratulations {0}! You are Secret Santa for: ' \
                '<b> {1}</b>'.format(self.santa, self.child)
        
        self.html3 = '<br>The price limit is: ${0}<br><br>  - Kris Kringle' \
                '<br></body></html>'.format(self.price_limit)
        
        self.html = '{0}{1}{2}'.format(self.html1, self.html2, self.html3)


    def send(self):

        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.subject
        msg['From'] = self.from_address
        msg['To'] = self.to_address
        
        part1 = MIMEText(self.text, 'plain')
        part2 = MIMEText(self.html, 'html')
        
        msg.attach(part1)
        msg.attach(part2)
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login('alittlegnome@gmail.com','f4Pimz9GgUQ8KeUWa4vmw9kBtaFDzG')
        server.sendmail(self.from_address, self.to_address, msg.as_string())
        server.quit()

