!pip install SpeechRecognition
!pip show pyaudio # pyaudio 설치 확인
!pip install pyaudio # 없으면 설치

import speech_recognition as sr

# 마이크로 auido source를 생성 -> 마이크에 입력
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

# 구글 웹 음성 API로 인식하기 (하루에 제한 50회)
try:
    print("Google Speech Recognition thinks you said : " + r.recognize_google(audio, language='ko'))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio") # 음성인식 실패
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))