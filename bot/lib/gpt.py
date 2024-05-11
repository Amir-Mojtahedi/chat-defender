from openai import OpenAI

class Gpt:
  
  def __init__(self):
    
    self.client = OpenAI()

  def is_hate_speech(self, text: str):
    """
    Determines if the given text is considered hate speech.

    Args:
        text: The text to be evaluated.

    Returns:
        bool: True if the text is considered hate speech, False otherwise.
    """
    completion = self.client.chat.completions.create(
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
      
  def summerize_converstaion(self, messages: str):
    """
    Summarizes a conversation based on the provided messages.

    Args:
        messages: The conversation messages to be summarized.

    Returns:
        str: The summarized conversation.
    """
    completion = self.client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a conversation summarizer. I provide you with text that includes information about the sender of the message, the content of the message, and the timestamp of the message. The text I provide you with might have many senders, different content and different timestamps. You have to be able to write a summary for this conversation. As an example, if I provide you with the following text: 'Sender: John, Content: Hello, Timestamp: 12:00. Sender: Mary, Content: Hi, Timestamp: 12:01. Sender: John, Content: How are you?, Timestamp: 12:02.', you should be able to summarize this conversation by saying \"John and Mary had a conversation where John greeted Mary and asked her how she was doing.\"."},
        {"role": "user", "content": messages}
      ]
    )
  
    return completion.choices[0].message.content
  
  def ask_gpt(self, user_input: str, system_input: str = "You are a helpful assistant."):
    """
    Asks GPT-3.5 a question and returns the response.

    Args:
        user_input: The prompt to be sent to ChatGPT.
        system_input (optional): The system message helps set the behavior of the assistant. For example, you can modify the personality of the assistant or provide specific instructions about how it should behave throughout the conversation. However note that the system message is optional and the model's behavior without a system message is likely to be similar to using a generic message such as "You are a helpful assistant.".

    Returns:
        str: The response from GPT-3.5
    """
    completion = self.client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": system_input},
        {"role": "user", "content": user_input}
      ]
    )
  
    return completion.choices[0].message.content