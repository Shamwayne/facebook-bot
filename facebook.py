"""
This bot listens for incoming connections from Facebook. It takes
in any messages that the bot receives and uses the chat.
"""
from flask import Flask, request
from pymessenger.bot import Bot
from bot import bot_response

# get the Facebook tokens
ACCESS_TOKEN = ""
VERIFY_TOKEN = ""

app = Flask(__name__)

bot = Bot(ACCESS_TOKEN)


@app.route("/handler", methods=['GET', 'POST'])
def handler():
	# This deals with getting the verify token to start bot messaging
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        else:
            return 'Invalid verification token'

    # This actually handles Webhook Updates
    if request.method == 'POST':
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for msg in messaging:
                if msg.get('message'):
                    recipient_id = msg['sender']['id']

                    if msg['message'].get('text'):
                        message = msg['message']['text']
                        # generate response and send it
                        #
                        # *** ALL YOUR LOGIC GOES HERE ***
                        #
                        response = "Your message here"
                        bot.send_text_message(recipient_id, response)

                    if msg['message'].get('attachments'):
                        for att in msg['message'].get('attachments'):
                            bot.send_attachment_url(recipient_id, att['type'], att['payload']['url'])
                else:
                    pass
        return "Ok"

if __name__ == "__main__":
    app.run()