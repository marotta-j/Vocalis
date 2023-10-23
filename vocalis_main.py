import speech_recognition as sr
import openai
from gtts import gTTS
import wikipedia
import pyjokes

class Vocalis:
    def __init__(self):
        openai.api_key = "YOUR API KEY HERE"  # secret API key for OpenAI
        self.r = sr.Recognizer() # init the speech recognition module

    def speak(self, text): # save the response as an mp3
        speech = gTTS(text)
        speech.save('audio.mp3')
        return text

    def listen_and_decode(self):
        with sr.Microphone() as source: # listen through the microphone
            audio = self.r.listen(source)
        try:
            request = self.r.recognize_google(audio) # speech recognition using Google speech to text
            print('Heard: "' + request + '".')
            print('------------------------')
            return request
        except sr.UnknownValueError: # when you say gibberish
            print("Could not understand audio")
            return "Could not understand audio"
        except sr.RequestError as e:
            print("Error; {0}".format(e))
            return "Error"

    def create_response(self, request): # determine the response
        # ------ Begin Pre-made Responses ---------------------
      
        if request.lower() == 'who are you':
            return self.speak('Hi! I am your virtual assistant named Vocalis. Ask me anything!')
        elif request.lower() == 'what is your function':
            return self.speak('My function is to help you and get as smart as possible!')

        # ------ End Pre-made Responses --------------------

        # ---- Error handling responses -----
        elif request == 'Could not understand audio':
            return self.speak("Sorry, I couldn't understand that.")

        elif request == 'Error':
            return self.speak("Sorry, try again later.")
        # ---- Error handling responses -----

        elif "joke" in request.lower(): # If you ask a joke
            return self.speak(pyjokes.get_joke()) # get a progamming joke from PyJoke
        else: # If no pre-made response, search Wikipedia or use ChatGPT
            return self.generate_internet_content(request)

    def generate_internet_content(self, request):
        try:
            # Try and search Wikipedia
            print(wikipedia.summary(request, sentences=2, auto_suggest=False))
            return self.speak(wikipedia.summary(request, sentences=2, auto_suggest=False))
        except Exception: # If no Wikipedia article exists with that name, use OpenAI
            print('--- Using ChatGPT to answer ---')
            completion = openai.Completion.create( # completion request to OpenAI
                model="text-davinci-003",
                prompt=f"{request}",
                max_tokens=100, # only 100 tokens so it doesn't go on forever
                temperature=0
            )
            print(completion.choices[0].text)
            return self.speak(completion.choices[0].text)

if __name__ == "__main__":  # for testing purposes -- - - - - -
    v = Vocalis()
    text = v.create_response(v.listen_and_decode())
    print(text)
