import json

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from app.config.secure import access_key_id, access_secret


def send_verification_sms(phone, code):
    client = AcsClient(access_key_id, access_secret, 'cn-hangzhou')

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', phone)
    request.add_query_param('SignName', "创想实验室")
    request.add_query_param('TemplateCode', "SMS_132535024")
    request.add_query_param('TemplateParam', json.dumps({'code': code}))

    try:
        response = client.do_action_with_exception(request)
        return json.loads(response.decode('utf8')).get('Message')
    except:
        return 'request error'


if __name__ == '__main__':
    print(send_verification_sms('18768153531', '123456'))
