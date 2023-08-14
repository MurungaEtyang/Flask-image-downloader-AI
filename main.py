import openai as openai
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client


openai.api_key = 'YOUR_OPENAI_API_KEY'
class ChatApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.text_input = TextInput(hint_text="Type your message here...")
        self.send_button = Button(text="Send", on_press=self.send_message)
        self.layout.add_widget(self.text_input)
        self.layout.add_widget(self.send_button)
        return self.layout

    def send_message(self, instance):
        user_message = self.text_input.text
        bot_response = self.process_message(user_message)
        self.send_whatsapp_response(user_message, bot_response)
        self.text_input.text = ""

    def process_message(self, message):
        response = openai.Completion.create(
            engine="davinci",  # Use the GPT-3 engine
            prompt=message,
            max_tokens=50  # Adjust as needed
        )
        bot_response = response.choices[0].text.strip()
        return bot_response

    def send_whatsapp_response(self, user_message, bot_response):
        # Twilio credentials
        account_sid = 'ACff4e37308ce6f12ea0ef818c0aefb0f7'
        auth_token = '2898c515a84dbe98f249c44cd8cde0b6'
        twilio_phone_number = '+14155238886'

        # Initialize Twilio client
        client = Client(account_sid, auth_token)

        response = MessagingResponse()
        response.message(f"You: {user_message}\nBot: {bot_response}")

        client.messages.create(
            to=twilio_phone_number,
            from_='whatsapp:' + twilio_phone_number,
            body=response.to_xml().decode('utf-8')
        )

if __name__ == '__main__':
    ChatApp().run()
