import boto3
from config.settings import settings


class SES_CLIENT:
    def __init__(self):
        self.access_key = settings.AWS_ACCESS_KEY
        self.secret_key = settings.AWS_SECRET_KEY
        self.region = settings.AWS_REGION
        self.ses_client = boto3.client(
            "ses",  region_name='eu-central-1', aws_access_key_id =self.access_key,aws_secret_access_key = self.secret_key
        )

    async def send_email(self, subject, to_addresses, text_data):
        body = {
            'Text': {
                'Data': text_data,
                'Charset': "UTF-8"
            }
        }
        
        try:
            response = self.ses_client.send_email(
                Source='temirlan.kazhigerey@gmail.com',
                Destination={
                    'ToAddresses': [to_addresses,],
                    'CcAddresses': [],  
                    'BccAddresses': []  
                },
                Message={
                    'Subject': {
                        'Data': subject,
                        'Charset': "UTF-8"
                    },
                    'Body': body  
                }
            )
            print("Email sent successfully! Message ID:", response['MessageId'])
        except Exception as e:
            print("Email sending failed:", str(e))
