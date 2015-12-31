import smtplib    




def Send_Textbook_Email(buyer, seller):
    try:
        body = '''%s is contacting contacting you about the textbook %s. 
Below is their message:\n-----------------\n%s\n-----------------\n
If you'd like to contact %s further, their email is %s. From all of us at NDreviews.com, have a great day!!
''' %( buyer["name"], seller['title'], buyer['message'],buyer["name"], buyer['email'])
        
        message = 'Subject: %s \n\n %s' %("New Textbook Offer", body)
        mail = smtplib.SMTP('smtp.gmail.com',587)
	    
        receivers = [seller['email'], 'pcunneen@nd.edu']
        FROM = 'ndreviews1842@gmail.com'
        password = '5BrnH+5BrnH+'
        mail.ehlo()
        mail.starttls()
        mail.login(FROM,password)
        for recepiant in receivers:
            mail.sendmail(FROM,recepiant,message)
        mail.quit
        return "Successfully sent email"
    except smtplib.SMTPException,error:
        print str(error)
        return "Error: unable to send email"