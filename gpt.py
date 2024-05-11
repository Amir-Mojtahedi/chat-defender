from openai import OpenAI
client = OpenAI()

def is_hate_speech(text):
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a hate speech detector, for everything i say to you, please reply \"True\" if you would consider what i am saying hate speech or reply \"False\" in any other case. Ensure to take into consideration the overall feeling of the message. As an example, \"I love you my dumb little cutie\" is not hate speech even though the word dumb is used in it since the overall feeling is positive."},
        {"role": "user", "content": text}
      ]
    )
    if completion.choices[0].message.content == "True":
        return True
    else:
        return False