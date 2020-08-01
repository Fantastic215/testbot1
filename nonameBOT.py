from flask import Flask, request
from pymessenger.bot import Bot
import os

app = Flask(__name__)

ACCESS_TOKEN = 'EAAE8JlowHrsBAB781IgZBRhLf46XRJCoIdh2rGAZBv2nKcYrN7r5JKWAxuBDCfiQx1LaxblWYPihGf0oAotCujmgCF4eZCnI3DssfdWnIadHBOvhKFJC5zQiZBWk9ZAlfh798krKFNvcgzMKJ6bZAZBMcsgRHBFXUlZCHlAZALh05OIGVQNZAOvfuR'
VERIFY_TOKEN = 'Noname.ProG'

bot = Bot(ACCESS_TOKEN)

#Получать сообщения, посылаемые фейсбуком нашему боту мы будем в этом терминале вызова
@app.route('/', methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
    # до того как позволить людям отправлять что-либо боту, Facebook проверяет токен,
    # подтверждающий, что все запросы, получаемые ботом, приходят из Facebook
        token_sent = request.args['hub.verify_token']
        return verify_fb_token(token_sent)
    # если запрос не был GET, это был POST-запрос и мы обрабатываем запрос пользователя
    else:
        # получаем сообщение, отправленное пользователем для бота в Facebook
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    #определяем ID, чтобы знать куда отправлять ответ
                    recipient_id = message['sender']['id']
                    try:
                        message_text=message['message'].get('text')
                        if message_text.lower() == 'начать':
                            send_message(recipient_id, 'я и так работаю)')
                        elif message_text.lower() == 'инфо':
                            send_message(recipient_id, 'я ничего не скажу вам')
                        elif message_text.lower() == 'мой id':
                            send_message(recipient_id, 'ваш id:\n' + str(recipient_id))
                        elif message_text.lower() == 'возможности':
                            send_message(recipient_id, 'вот что я могу:\n+сообщить вам ваш id(напишите"мой id")\n'
                                                       '+"инфо" и "начать" почти ничего не делают пока что')
                        else:
                            send_message(recipient_id, 'напишите понятней')
                    except :
                        # если пользователь отправил GIF, фото, видео и любой не текстовый объект
                        if message['message'].get('attachments'):
                            send_message(recipient_id, "я пока что не понимаю вас, но в скором времени научусь(¬‿¬)")



        return "Message Processed"

def verify_fb_token(token_sent):
    '''Сверяет токен, отправленный фейсбуком, с имеющимся у вас.
    При соответствии позволяет осуществить запрос, в обратном случае выдает ошибку.'''
    if token_sent == VERIFY_TOKEN:
        return request.args['hub.challenge']
    else:
        return 'Invalid verification token'

def send_message(recipient_id, response):
    '''Отправляет пользователю текстовое сообщение в соответствии с параметром response.'''
    bot.send_text_message(recipient_id, response)
    return 'Success'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
