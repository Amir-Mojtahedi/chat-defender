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
  
  def detect_fallacy(self, messages: str):
    print(messages)
    """
    Detects any logical fallacies in the provided messages.

    Args:
        messages: The conversation messages in which to look for fallacies.

    Returns:
        str: A short description of the fallacies present.
    """
    completion = self.client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a logical fallacy detector. I provide you with text that includes information about the sender of the message, the content of the message, and the timestamp of the message. The text I provide you with might have many senders, different content and different timestamps. You have to be able to reconstruct the conversation and find logical fallacies in it while considering that some messages are commands or more than one conversation can be present and considering that new conversations can start seemingly randomly, so they should not be treated as a Red Herring fallacy. You should omit fallacies that are only potentially relevant. As an example, if I provide you with the following text: 'Sender: John, Content: I heard that eating organic food is better for your health, Timestamp: 12:00. Sender: Mary, Content: Really? I don't think so. I ate organic once and still got sick, Timestamp: 12:01.', you should be able to detect the Anecdotal Fallacy and the Confirmation Bias fallacy this conversation by saying \"Bob uses his personal experience of getting sick after eating organic food to refute the general claim that organic food is better for health. However, one person's experience is not enough to draw a general conclusion about the health benefits of organic food. This is an example of an anecdotal fallacy, where an individual's personal experience is given undue weight in an argument.. Both John and Mary may be exhibiting confirmation bias. Alice only considers information that supports her belief that organic food is better for health, while Bob only remembers the instance when he got sick after eating organic food, reinforcing his skepticism. Confirmation bias involves seeking out or interpreting information in a way that confirms one's preexisting beliefs or hypotheses, while ignoring or dismissing contradictory evidence\"."},
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
  
  def grammar_check(self, text: str):
    """
    Checks the grammar of the provided text.

    Args:
        text: The text to be checked.

    Returns:
        str: The corrected text.
    """
    completion = self.client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system",
         "content": "You are a grammar/vocabulary/spell checker. Please correct any grammar or vocabulary mistakes in the text. As an example, if the text is 'I is happy', you should correct it to 'I am happy'. Make sure to not change the meaning of the text. In case the text is already correct, you can reply with 'No grammar issue found'. Keep in mind that the text might be in different languages, so you should be able to correct grammar in different languages."},
        {"role": "user", "content": text}
      ]
    )
  
    return completion.choices[0].message.content