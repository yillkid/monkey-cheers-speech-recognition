import random
import time
import speech_recognition as sr
from led import led_reset_all, led_listen, led_win, led_lose

def recognize_speech_from_mic(recognizer, microphone):
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        try:
            print("1/3: 我正在聽呢 ... ...")
            led_listen()
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=3)
        except Exception as e:
            response["success"] = False
            response["error"] = e
            return response

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    # update the response object accordingly
    start_time = time.time()

    try:
        print("2/3: 我正在思考您說的是什麼 ... ...")
        response["transcription"] = recognizer.recognize_google(audio, language='zh-TW')
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"

    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "我的 Google 語音辨識好像失效了！"

    print("3/3: 我猜完了，一共花了 %s 秒！" % (time.time() - start_time))
    
    return response


if __name__ == "__main__":
    # 匯入答案庫
    list_answer = []
    with open('answer/input.txt','r') as f:
            list_answer = f.read().splitlines() 

    while True:
        # TODO: 檢查網路狀態

        # Reset LED
        led_reset_all()

        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        print('遊戲開始囉!')
        guess = recognize_speech_from_mic(recognizer, microphone)
        if not guess["success"]:
            print("I didn't catch that. What did you say?\n")


        # if there was an error, stop the game
        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
            led_lose()

        # show the user the transcription
        print("你說: {}".format(guess["transcription"]))

        # 比對答案
        if guess["transcription"] in list_answer:
            print("你猜對了!")
            led_win()
        else:
            print("你猜錯了！")
            led_lose()

