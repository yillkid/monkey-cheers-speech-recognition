import random
import time
import speech_recognition as sr

def recognize_speech_from_mic(recognizer):
    # check that input file
    audio = ""
    with sr.AudioFile("media/monkey-cheers.wav") as source:
        audio = recognizer.record(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

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

    # TODO: 比對答案
    print("3/3: 我猜完了，一共花了 %s 秒！" % (time.time() - start_time))
    
    return response


if __name__ == "__main__":
    # TODO: 匯入答案庫

    # TODO: 檢查網路狀態
    recognizer = sr.Recognizer()

    print('1/3: 遊戲開始囉!')
    guess = recognize_speech_from_mic(recognizer)
    if not guess["success"]:
        print("I didn't catch that. What did you say?\n")

    # if there was an error, stop the game
    if guess["error"]:
        print("ERROR: {}".format(guess["error"]))

    # show the user the transcription
    print("你說: {}".format(guess["transcription"]))
