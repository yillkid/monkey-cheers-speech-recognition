import random
import time
import speech_recognition as sr
from tty import write as serial_write 
from tty import read as serial_read
from line_bot import linebot_write
from network import get_ip_address, connect_time

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


    # Read from serial for listening
    content_from_serial = ""
    while True:
        content_from_serial = serial_read()
        if content_from_serial == "b":
            break
        elif content_from_serial == "a":
            continue

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        try:
            recognizer.adjust_for_ambient_noise(source)
            print("1/3: 我正在聽呢 ... ...")
            start_time = time.time()
            recognizer.dynamic_energy_threshold = False
            audio = recognizer.listen(source, timeout = 2.0, phrase_time_limit = 2.0)
            print("我聽完了，一共花了 %s 秒！" % (time.time() - start_time))

            #start_time = time.time()
            #with open("audio_file.wav", "wb") as file:
            #    file.write(audio.get_wav_data())
            #print("DEBUG: 存檔，一共花了 %s 秒！" % (time.time() - start_time))

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
        # Check networking
        try:
            ip = get_ip_address()
            duration = connect_time()
            if float(duration) > 0.02: 
                linebot_write("幫加油已經啟動完成！IP: " + str(ip) + "，網路品質稍慢！")
            else:    
                linebot_write("幫加油已經啟動完成！IP: " + str(ip) + "，網路品質良好！")
        except:
            pass

        # Write reset to serial
        serial_write("0")

        recognizer = sr.Recognizer()
        microphone = sr.Microphone(chunk_size=1024, sample_rate=48000)

        print('遊戲開始囉!')
        guess = recognize_speech_from_mic(recognizer, microphone)
        if not guess["success"]:
            print("I didn't catch that. What did you say?\n")


        # if there was an error, stop the game
        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))

        # show the user the transcription
        print("你說: {}".format(guess["transcription"]))
        linebot_write(guess["transcription"])

        # 比對答案
        if guess["transcription"] in list_answer:
            print("你猜對了!")
            serial_write("1")
        else:
            print("你猜錯了！")
            serial_write("2")
