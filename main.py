"""
1. firebase 연동 및 회원 가입 로그인 기능
2. Manager, User UI 다르게 만들기.
3. Manager, User 기능 구현(문제를 풀때에는 마지막 정답:1 이 부분이 안나오게 제어하고, 만약 푼 문제가 틀렸으면 오답노트로 파일을 생성해준다.)
4. 패키징 하기.
5. 추가로 쓰레드 사용 하기.
"""
from random import random

"""
[클래스 관련 내용]
객체를 먼저 판단해서 나눌지 결정하기.
유저, 매니저, 문제,
"""

import pyrebase
import sys
import os
import random
import shutil

config = {
    "apiKey": "AIzaSyAcJdQ7H6f8RsYItDNK1FYGLNO-ViOGMR8",
    "authDomain": "pythonquiz-ded50.firebaseapp.com",
    "databaseURL": "https://pythonquiz-ded50.firebaseio.com",
    "projectId": "pythonquiz-ded50",
    "storageBucket": "pythonquiz-ded50.appspot.com",
    "messagingSenderId": "727076101887",
    "appId": "1:727076101887:web:1ea8d91ac5572464cb36ca",
    "measurementId": "G-9DEF4Z3P6P"
}

firebase = pyrebase.initialize_app(config)

# db = firebase.database()
# storage = firebase.storage()
auth = firebase.auth()

prompt = """
\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n
\t\t\t$$$#$$$$#$$$$$$$#$$$$$$$$$#$$$#$$$$$$$$$$$$#$$$$$#$$$$$$$$$$$$#$$$$$$$#$$$$#$$$#$$$$$$##$#$$$$$$$$$~..:#$$#$$$$$#$$#$$$..~$$$#$$$#$$$$#$$$#$$$$$#$$#$...#$$#$$$$$$$$#$$$#...!$$#$#$$$#$
\t\t\t$$$$#$$#$#$$$##$~..:$#$$$$#$$#$$$$$$$$$##$##$$$$#$$$#$$$$...$#$$$#$#$$$$$$$$$-..!$$$#$#$$$$$#$$#$#$~..~$###$$$$$$$##$##..~$#$$$#$$###$#~...........#$...$$$$#####$$$$$$$$...!$$#$$$$#$$
\t\t\t$$$==***==***=#$~..~$##$#=*=$$##$##$=**$$$$#$*::::::#$$$#...$$$$$$$$$$$$$$$$$-..!$$$$$.........,$$$~..:$#$$$#$..-###$$$..~$$$$$#$$-..$$~...........$$...###$.........:$$$...!$$...$$#$$
\t\t\t$#*...........#$~..:$$$$$..;$#$$#$#$:..$$$$$$;......$$$$$...$$#$.........:##$-..!$$$#$.........,##$~..:$$#$$$#..-$$$##$..~$$$$$$$!..,$$$===========$$...$##$.........:$$$...!$$!..,#$$$
\t\t\t$$*...........$$~..~#$$##..;$$$#$$$$:..#$$$$$;......$$$$$...$$$#.........:$$#-..!#$$$$*******..,##$~..:$$#$$$$..,#$$#$#..~$$$$$$$...$$#$#~~;#$~~~$$#$...$$#$*******..:$#$...!#$$...*#$$
\t\t\t$$$$$$$...$$$$$$~..:$#$$#..;$$$$$$$$:..$#$##$$$#$$##$$$$#...$$$#=======..:$$$-..!$$$$$$$$###*..,$$$~..:#$$#$$$...$$$$$#..~#$$#$$;..-$$$$$..~$$,..$$$$...#$$$$$$#$$;..:$$$...!$$$=...$$$
\t\t\t$$$$##$...$#$;~~,..:$$$#$..............$$$$:,,,,,,,,,,;$$...$$$$#$$$$$$..:###-..!$$$$$$#$$$$;..=$$$~..:#$$$$$#...$$#$$$..~#$$$$$...!$$#$#..~$$,..$$$$...$$$#$$$$$$~..$$$#...!$$#$...*$#
\t\t\t##$$$$-...~$$~.....:$#$$$..............$#$$~..........;#$...$$$$$$$$#$$..:$$$-..!$$$$$$$#$$$~..$$#$~..:$$$$$$*...$$$$$$..~#$#$$*...#$$$$$~.~$$,.-$$$$...###$$$$$$$,.,$$$$...!$$$$....$$
\t\t\t#$$#$;.....!$*;;-..:$$#$$..;$$$$$$$#:..$$#$!;;;~..;;;;*$$...$$$$;;;;;;;..:$##-..!$$$$$$$$#$=..-$##$~..:$$#$$$:...-$#$$$......$$:..,#$#$**:.-:,.....:$...$$$$$$$$$*..;$#$$...!$$$$=...$$
\t\t\t$#$$!...$...!$$$~..:$$$$$..;$$$$$$$$:..$#$$$$$$,..$$$$$$#...#$$$.........:$$$-..!$$$$#$$#$$~..$$$##~..:$#$$$$.....#$$$$......#$~..~$$$#............:$...$$$$$$$$$...$$$$$...!$#$$$...*$
\t\t\t$$$!...*$*....$$~..:$$$$$..;$$#$$$$$:..$$$$#$$#....#$:......$$##..,~~~~~~!$#$-..!$$$$$#$$$~..~$$#$$~..:$$#$$~..,..,$$$$..~$$$$$...~$$$$,,,,,,,:$$$$$$,,,#$$$$#$#...!$$$$#...!$$#$$...!#
\t\t\t##,...=#$$*-.,$#~..:$$$#$..............##$$$$$$....$#:......$$#$..-$#$$$#$$#$-..!$$$$#$$$;...$$$$$$~..:$$##$...$...$$$$..~$$$$$...~$#$$$$$$$$$$$$$$$$$$$$$$$$$$,...$$$$$$...!#$#$=...!$
\t\t\t$$$.,=$$$$#$=$#$~..:$#$$$..............$$$$$$$!....*$$#$$...$#$$..-#$$$$$$$$$-..!$$#$$$$~...$$$$$$$~..:$$$$,..!$$...=$$..~$$$$$...~$#$$$$$..............$$$$$$-...$$$$$$$...!$$$#=...!$
\t\t\t#$#$$$$$$$$$$$$#~..:#$$$$$$$$$,..*$$$$$#$$$#$#..-...$$$#$...##$$..-$#$$$$$$$$-..!$$$#$$~...:$$$$##$~..:$#$,..:$$$!...~$..~$#$$$...~$$$##$$..............$$$#$-...=###$$$#...!$$#$$...!$
\t\t\t$$$$$#$:,......,-=$$#$$#$$$$$$...=$$$$$$#$$$$,..==..,$$$#...#$$$..-$#$$$$$!~$-..!$$$$*....!$$$$$$$$~..:$$...:$$$#$!..!$..~$$$$$...~$$$$$$$$$$$$$$$$$$...#$$;...,=$$$$#$$$...!$$$$=...!$
\t\t\t$$$$#$,...........!##$#$$$#$$$,..=$$$$###$$$,..~#$*..,!$#...$#$$...........-$-..!$$$$:...=#$$$$$$#$~..:$$$,:$$#$$$$*;#$..~$$$$$:..~$#$$$$$..............$$$-..,$$$$$$$$$$...!$$$$=...=$
\t\t\t$#$$$,..~*$#$$#!...*##$$$$$$$$,..=$$$$$$$#;...-#$$$!...*#...##$$...........~$-..!$$$$$~:$$$$$#$$$$$~..:$$$#$$$#$$$$$$$$..~$$$$$:...$$$$$$$..............$#$$-;$#$$$$$$$$$...!$$$$!...$$
\t\t\t$$$$$...$$#$$$#$!..~$$;;;;;;;;...:;;;;;;;$$-.~$$$$$$!.;$$...$$#$;;;;!=#$$$$$$-..!$$$$$#$$$$$#$#$$$$~..:$#$$#$$$$$$$$##$..~$#$$#;...$$##$$$..-$$$$$###$$$#$$$#$$$$#$#$$$$$...!$$$$...-$#
\t\t\t$$$$$...$$$$$$$$:..:$$...................$$;*$$$$$$#$$$$#...$$$$###$$#$$$$$$$-..!$$$$#$##$$$#$#$$#$~..:$$$#$$$$$#$$$$#$..~$$$$$$,..-$$#$$$..,~::::::~:::$$$#$##$$$$$$$$$$...!$$$$...*$$
\t\t\t$$$$$~...******-...$$#~~~~~~~~~~~~~~~~~~~$$$$$$#$$$##$$$#...$$$$#$$$$#$$$$$##-..!$$####$$##$$#$$###~..:$$$$$#####$#$$#$..~#$$#$#;..-$$$#$$..............=#$$##$$$$$$$#$$$...!$$$=...$$$
\t\t\t$##$$$~..........,;$$#$$$$$$$$$#$$#$$$$$$$$$#$$$$$$$$$$$$...$$$$$$$$$$$#$#$#$-..!$$####$$$$$$$$####~..:#$#$$#$#$$$$$$$#..~$$#$$$$...$$$$$#..............=$$#$$##$$#$$$$$#...!$$#...=$$$
\t\t\t#$$$$##$,.......*#$$$$$$$$$##$$$$$$$$$$$##$$#$$##$$##$##$...$#$$$$$##$$$$$$$$-..!$$$$$$$$#$##$$$#$$$$$$$$$$$$$$$##$$#$$$$$##$$$$$!..,$$$$$$#$$$#$$$#$$#$$$$$#$$$#$$$$$$$$#$$$$$*...$$$$
\t\t\t#$#$$$#$#$#$$$$$$$$$$$#$$$$#$$$$$$$$$$$$$$$$#$$$#$##$$$#$=$=##$$##$$#$$#$$$#$$$=$$##$$$#$$$##$$$$$$$#$$$$$$$$$$$$#$$#$$$$$$$$$$$$#!!!$#$$$$##$$$$$$#$$$$#$$#$$$$$$$$$$$$$$$$$$$**!$$$$$


\n\n
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t1. 로그인
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t2. 회원가입
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t3. 종료
\n\n\n\n\n
"""

userPrompt = """
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t1. 문제풀기
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t2. 오답노트
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t3. 로그아웃
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t4. 종료
\n\n\n\n\n
"""

managerPrompt = """\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t1. 문제 추가
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t2. 문제 검색 및 수정
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t3. 문제 삭제
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t4. 문제 전체 삭제
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t5. 로그 아웃
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t6. 시스템 종료
\n\n\n\n\n
"""


def loginUser():
    global email
    global password
    Login = False
    while True:
        print(prompt)
        try:
            number = int(input("\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t숫자를 입력주세요 :"))
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            # 로그인
        except ValueError:
            return

        if number == 1:
            print(
                "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
                "\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\"뒤로가기\"를 입력하면 이전 페이지로 이동합니다.\n")
            # Login
            while True:
                email = input("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t이메일 :")
                if email == "뒤로가기":
                    print(
                        "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                    break
                password = input("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t비밀번호 :")
                if password == "뒤로가기":
                    print(
                        "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                    break

                # tryLogin = 0
                # if tryLogin >= 3:
                #     Check = input("뒤로 돌아가시겠습니까? (1. 네, 2. 아니오) :")
                #     if tryLogin == 1:
                #         break
                try:
                    auth.sign_in_with_email_and_password(email, password)
                    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
                          "\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t로그인 되었습니다.")

                    if not os.path.isdir("../회원파일/{}".format(email)):
                        os.mkdir("../회원파일/{}".format(email))
                    return email


                except:
                    # tryLogin += 1
                    print("\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t이메일 또는 비밀번호를 다시 입력해주세요.\n")

        # 회원가입
        elif number == 2:
            print(
                "\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\"뒤로가기\"를 입력하면 이전 페이지로 이동합니다.\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t이메일 형식에 맞게 입력해주세요. (Ex: Playdata@naver.com)\n")
            email = input("\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t이메일 :")
            if email == "뒤로가기":
                print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                break
            password = input("\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t비밀번호 :")
            if password == "뒤로가기":
                print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                break
            passwordCheck = input("\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t비밀번호 확인 :")
            if password == "뒤로가기":
                print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                break
            while password == passwordCheck:
                auth.create_user_with_email_and_password(email, password)
                print("\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t회원가입이 되었습니다.")
                if not os.path.isdir("../회원파일/{}".format(email)):
                    os.mkdir("../회원파일/{}".format(email))
                break
            else:
                print("\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t비밀번호를 다시 입력해주세요.")

        # 종료
        elif number == 3:
            sys.exit(0)
        else:
            print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t숫자를 다시 입력해주세요.")


class Dao:
    def __init__(self):
        self.ch = 0
        self.prod = []
        self.examAnswer = []
        self.userAnswer = []
        self.testNumber = []
        self.incorrectNumber = []

    def addQ(self):
        arr = []
        file_name = input(
            "\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\"뒤로가기\"를 입력하면 메뉴창으로 이동합니다\" \n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t문제 번호 :")
        if os.path.isfile(file_name):
            print(
                "\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t같은 파일명을 갖고 있는 파일이 존재합니다.\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t파일명을 바꿔주세요.\n")
            return
        elif file_name == "뒤로가기":
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            return

        print(
            """\n\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t마지막에 \"정답:1\"과 같은식으로 정답을 기입해주세요.\n\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t(작성을 완료 하려면 "/끝"을 입력하세요!!)\n""")
        while True:
            string = input()
            if string == "/끝":
                break
            arr.append(string + '\n')

        file = open(file_name, "w")
        file.writelines(arr)
        file.close()

    def editQ(self):
        # 수정 로직 = 파일을 불러와서 위에서 보여준다 > 수정 하시겠냐고 물어보면 (수정 , 뒤로가기)를 입력해서
        # 각 입력받은 내용을 전달 받아 if else 제어문으로 UI 조종한다.
        # 수정을 입력하면 새 파일을 만들때 처럼, UI를 만들어 줘서 저장시킨다. 저장할 때는 추가 할때 방법과 같지만 파일이 새로 생기는것이 아닌, 같은 파일에서 새로 저장이 될 수 있도록 구현한다.
        global Q
        msg = """\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t수정 하시겠습니까? (\"네\" 또는 \"아니오\"를 기입해주세요) :"""
        while True:
            # 셔플하는 방법 알아보기.
            # print(os.listdir(os.getcwd()))
            for i in os.listdir(os.getcwd()):
                print(i)
                # for j in random(5):

            mode = "r"
            file_name = input("\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t(\"뒤로가기\"를 입력하면 메뉴창으로 이동합니다.)"
                              "\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t어떤 파일을 수정 하시겠습니까? :")
            if os.path.isfile(file_name):
                while True:
                    file = open(file_name, mode)
                    print("--------------------------------")
                    print("\n", file.read())
                    print("--------------------------------")
                    try:
                        Q = input(msg)
                    except ValueError:
                        print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t다시 입력해주세요.")
                    if Q == "네":
                        # 해당 파일 삭제
                        os.remove(file_name)
                        # 새로운 파일 작성
                        arr = []

                        if os.path.isfile(file_name):
                            print(
                                "\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t같은 파일명을 갖고 있는 파일이 존재합니다.\n\t파일명을 바꿔주세요.\n")
                            return
                        print("""\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t(작성을 완료 하려면 "/끝"을 입력하세요!!)\n""")
                        while True:
                            string = input()
                            if string == "/끝":
                                break
                            arr.append(string + '\n')

                        file = open(file_name, "w")
                        file.writelines(arr)
                        file.close()
                    elif Q == "아니오":
                        break
                    else:
                        print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t다시 입력해주세요.")
                    file.close()
            elif file_name == "뒤로가기":
                print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                break
            else:
                print('\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t파일명을 다시 확인해주세요!!\n')

    def removeQ(self):

        while True:
            print(os.listdir(os.getcwd()))
            file_name = input(
                "\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t(\"뒤로가기\"를 입력하면 메뉴창으로 이동합니다.)\n어떤 파일을 삭제 하시겠습니까? :")
            if os.path.isfile(file_name):
                os.remove(file_name)
                print('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t', "\"", file_name, "\"파일이 삭제 되엇습니다!\n")
                break
            elif file_name == "뒤로가기":
                print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                break
            else:
                print('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t파일명을 다시 확인해주세요!!\n')

    def removeAllQ(self):

        msg1 = """\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t정말 파일을 전체 삭제 하시겠습니까? (\"네 맞습니다.\" 또는 \"아니오\"를 기입해주세요) :"""
        msgEmail = """\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t이메일 :"""
        msgPassword = """\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t비밀번호 :"""
        check = input(msg1)
        if check == "네 맞습니다.":
            print("\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t이메일과 비밀번호를 입력해주세요.\n")

            # 이메일과 비밀번호 체크
            checkEmail = input(msgEmail)
            checkPW = input(msgPassword)
            if checkEmail == "Manager@naver.com" and checkPW == "123123":
                for i in os.listdir(os.getcwd()):
                    os.remove(i)
                    print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t전체 삭제 되었습니다.")
            else:
                print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t다시 입력하세요.")
                return
        else:
            return

    def answerList(self, path, num):
        answer = []

        f = open(path + '/{}번.txt'.format(num), 'rb')
        f.seek(-1, 2)
        ch = str(f.read(1)).split("\'")[1]  # b값 바이너리 값을 없애기 위해서 split 사용
        answer.append(int(ch))
        # print("문제의 정답 : {}".format(answer))
        self.examAnswer.append(int(ch))
        # print("문제의 정답 : {}".format(self.examAnswer))
        # print("유저의 정답 : {}".format(self.userAnswer))

        f.close()

    def solve_test(self, path):
        check = [False] * 20
        userAnswerList = []

        for i in range(0, 20):
            while True:
                # 20개 랜덤으로 돌려서 num에 저장
                num = random.randrange(0, 20)
                if check[num] == False:
                    check[num] = True
                    break
                # TODO : [문제] : 중복된 문제가 나온다. - 해결
                """
                [생각] : 불린으로 20개의 리스트를 다 false 로 넣고 불러와서 중복 안되게 구현.
                """
            # 문제 출제 하고 답 받는 코드
            # -------------
            Mode = 'r'
            u = open(path + '/{}번.txt'.format(num), Mode, encoding='utf-8')
            self.answerList(path, num)
            self.testNumber.append(num)

            # 5번째줄까지만 보여줌
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            for i in range(5):
                line = u.readline()
                print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t", line)
            print("\n\n\n\n\n\n\n\n\n\n")
            while True:
                try:
                    userAnswer = int(input("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tanswer:"))

                    if 1 > userAnswer or userAnswer > 4:
                        print("다시 입력해주세요.")
                    else:
                        userAnswerList.append(userAnswer)
                        self.userAnswer.append(userAnswer)
                        break
                except ValueError:
                    print("다시 입력해주세요.")

            # -------------

            # TODO : [문제] : 사용자가 입력한 정답과 문제의 실제 정답이 같은지 아닌지 판독하는 구문 만들기.
            """
            생각 : 먼저, 문제들의 정답 부분만 가져와서 (문제정답 리스트)에 넣고
            사용자가 입력한 답을 (사용자 답 리스트)에 넣어서
            두개의 값들을 불러와 두 리스트의 값이 일치 = 정답, 아닌경우 = 오답으로 처리한다.

            오답으로 처리 될 경우, 해당 번호의 문제를
            회원의 오답노트로 복사한다.
            """

            u.close()
            # print("유저가 입력한 정답 : {}".format(userAnswerList))

        self.calculator()

        # 파일 복사하는 코드
        os.chdir("./exam{}".format(self.ch))

        for i in range(len(self.incorrectNumber)):
            # print('{}번.txt'.format(self.incorrectNumber[i]))
            shutil.copyfile('{}번.txt'.format(self.incorrectNumber[i]),
                            "../../오답노트/{}번".format(self.incorrectNumber[i]))
        os.chdir("../")

    def exam(self):

        global f

        if not os.path.isdir("./문제파일"):
            os.mkdir("./문제파일")
        os.chdir("./문제파일")

        number = 1

        testAnswerList = []
        while True:
            if os.path.isdir("./exam{}".format(number)):  # 만약 해당 폴더가 있으면 숫자 1을 더해서 폴더를 생성한다.
                number += 1
            else:
                shutil.copytree("../../../문제파일", "./exam{}".format(number))

                self.ch = number
                break

        self.solve_test('./exam' + str(number))

        os.chdir("../")

        # 정답의 마지막 번호만 저장하는 코드

        # TODO: 점수 알려주기.
        # TODO: 틀린 문제는 오답노트로 이동.

    # 오,정답 판단하는 함수.
    # 틀렸을 경우 틀린 파일을 오답노트 파일로 넘겨준다
    def calculator(self):
        ExamAnswer = self.examAnswer
        UserAnswer = self.userAnswer
        correctTestNumber = []

        QNumber = self.testNumber

        score = 0
        for i in range(20):
            if ExamAnswer[i] == UserAnswer[i]:
                correctTestNumber.append(QNumber[i])
                score += 5
            else:
                self.incorrectNumber.append(QNumber[i])

        # 틀린문제 모임

        # print(score)
        # print("맞은 갯수", score // 5)

        # print(QNumber)
        # print(ExamAnswer)
        # print(UserAnswer)

        # print("맞은 문제 :", correctTestNumber)
        # print("틀린 문제 :", self.incorrectNumber)

        if score < 60:
            print("""

\t\t\t\t\t\t\t\t\t\t$$$#$#$$$$#$$#$##$$###$$$$$$##$##$$#$#$$$$$$$$$$$$$#$##$$$$$$;;;=$$#$#$$$$$$$$#$$$$$$$$$$$#$$=;;$$$$
\t\t\t\t\t\t\t\t\t\t$$$##=...:$$#$$$#$####$...,$#$$$#$$#$###$$$#!........;$$$$$##...*$$#$#$$$$#####$$$$$$##$$$###*..#$$$
\t\t\t\t\t\t\t\t\t\t#$$$$=...:$$##$$#$$$#$$...,$$$$$$$$$##$$$$$$!........;#$$$$$$...*$$$$#####$$$$$$$$$####$####$*..$$$#
\t\t\t\t\t\t\t\t\t\t#$$$$=....................,#$$$$$$$$$$$#$$$#*::::::::*$#$$$$$...*$$$$$$$!.............~$$$$$$*..$$$$
\t\t\t\t\t\t\t\t\t\t#$#$#=....................,$$#$#$$$$$$$#$$$$$$$##$$$$$$$$$$$$...*##$$$$$!.............~#$##$$*..#$##
\t\t\t\t\t\t\t\t\t\t$$$##=....................,#$$$#$$$$#$$$::::::::::::::::::$##...*#$#$$$$$$$##$$$$$$!..~$#####*..$$$$
\t\t\t\t\t\t\t\t\t\t$$$$$=...:#$$$#$$$$$$$#...,$$$$$$$$$###$..................$$$...*#$$#$#$$$$$$$$$#$$:..#,........$$$#
\t\t\t\t\t\t\t\t\t\t$$$$$=...:$##$#$#$$$$$$...,####$$$$$$$$$,,,,,,,,,,,,,,,,,,$$$...*#$$$$$$$$$$$$$$$$$,..$,........$$$$
\t\t\t\t\t\t\t\t\t\t#$$$$=...-!!!;!!!!!!!!;...,##$$$#$$$$$$$$#$##$$$=*$$$$$$$$$#$...*$$$$$$$$$$#$#$$#$;..*$;:::::~..$$$$
\t\t\t\t\t\t\t\t\t\t#$$$$=....................,$$$#$#$$$$$$$$#$$$,.......$$$$$$#$.......,$$$$$$###$$$$..-$$$$$###*..$$#$
\t\t\t\t\t\t\t\t\t\t$#$$$=....................,#$#$###$$$##$$$$;..........:$$$$#$.......,#$$$$$$$$###-..*$$#$$$$$*..$$#$
\t\t\t\t\t\t\t\t\t\t$#$$$$~~~~~~~~~~~~~~~~~~~~~#$$#$$$$##$$##$*...~$$$#*~..;#$$#$...-~~~~$$$$$$#$$#$,..-$#$$$$$$$*..$$$#
\t\t\t\t\t\t\t\t\t\t##$$$$#$$$$$$$$$$#$$$$##$$$$$$$$$$$$$$$$$$,..=$#$$$$$:..$$$$$...*$$$$$##$$$$$$#,...$$$*------,..#$$#
\t\t\t\t\t\t\t\t\t\t##;;;;;;;;;;;;;;;;;;;;;;;;;;;;*$$$$$$#$$$$..:#$$$$$$$;..!$$$$...*$$$$$$$$$$$$$-..-$$$#*.........$$$$
\t\t\t\t\t\t\t\t\t\t$$............................:#$$$$$###$$..~$$$$$$$$;..$$##$...*$$$$#$$#$#$:...,#$$$$*,,,,,,,..$$$$
\t\t\t\t\t\t\t\t\t\t$$............................:#$$$$$$$$$$;..~$#$$$$$-..$#$$$...*$#$$#$$$$~....*$##$$#$$#$$#$*..$$#$
\t\t\t\t\t\t\t\t\t\t$$~~~~~~~~~~~~....-~~~~~~~~~~~!#$$$$$#$#$$=,...****:...*$$$$$...*$$#$$$*.....~=$$$$$$$$$$#$$$*..$$$$
\t\t\t\t\t\t\t\t\t\t$###$$$$$#$$$$....;$$$$#$#$$$$$$$#$$$$##$$$$..........$$$$$$$...*$$$#$$$-..,$##$$$$$$#$$$$$$$*..$$$$
\t\t\t\t\t\t\t\t\t\t$##$$=;;;;;;;;....~;;;;;;;;$$$$$$#$#$$$$$#$$$;;;;:;;;$$$$$#$$;;;=$$#$$$$=;#$$$$$$$$$$$##$$#$$*..$$$$
\t\t\t\t\t\t\t\t\t\t$$$$#=....................,$$$$$$$$$$$$$#$$$$==$$$$$$$#$$$$$$===$$$$$$#$$$$$$##$$$$$$$##$$$$$$#$$$$$
\t\t\t\t\t\t\t\t\t\t$$#$$=....................,$$$#$$$$$$$#$$$$$!..$$$$$$$#$$$$$$...*$$#$$$##$$$~~~~~~~~~~~~~~~~~~~~$$$$
\t\t\t\t\t\t\t\t\t\t#$$$$=::~::::::~:::::~:...,$#$$$$#$$$$$$$$$$!..$$#$$$$$$$$#$#...*$$$$$$$$$#$....................$$$$
\t\t\t\t\t\t\t\t\t\t$$#$$##$#$#$#$$$$##$$#$...,$$$$$$#$$$$$$#$$$!..$$#$$$$$$$$#$$...*##$$$$$$#$$....................$#$#
\t\t\t\t\t\t\t\t\t\t$$$$$$:::::::::::::::::...,$#$$##$#$$#$$$$$$!..::::::::::::::...*$$#$##$$$$$$$##$$$$$##$$#$$$*..$$$$
\t\t\t\t\t\t\t\t\t\t#$$#$=....................,$$#$$$$$#$$$$$$##!...................*$$#$$$$$$#$$$#$#$$$$$$$$$#$$*..$$$$
\t\t\t\t\t\t\t\t\t\t$$##$=....................,$#$$$$$$####$$$$$!..==============...*$$$$$#$$$$$#$$$#$$$$$#$$####*..#$$$
\t\t\t\t\t\t\t\t\t\t#$$$$=...-::::::::::::::::;$#$#$#$$$##$$$$$$!..$#$$$##$$$$$$$...*$$$$#####$$$$$$$$$$###$##$$$*..$$$$
\t\t\t\t\t\t\t\t\t\t$$##$=...:$$$$$$$$$$$$$$$$$$$$$#$#$#$$$$$#$#!..$$#$$$#$$$###$...*#$$$#$$$###$$$$$$$$$$$$$#$#$*..$$$$
\t\t\t\t\t\t\t\t\t\t$$$$#=.....................;$$$#$$$#$$$#$$$$!..##$$#$$$#$$$#$...*$$#$$$$$$$#$$$##$$$$$$#$####*..$$$$
\t\t\t\t\t\t\t\t\t\t$$$$#=.....................;$$$$$$$$$$$$$$##!...................*#$#$##$$####$$$$$$$$$$$#####*..$$$$
\t\t\t\t\t\t\t\t\t\t$#$$$=.....................;$$$$$$$$$$#$$$$$!...................*$#$$##$$$$#$$$$#$$#$#$$$$$$$*..#$##
\t\t\t\t\t\t\t\t\t\t$$$$$$;;;;;;;;;;;;;;;;;;;;;*#$#$#$$$$$$$$$$#$$$$#$$$$$$#$$$$$#$$$#$$$$$#$$$$$##$$$$$$$$#$$$$$=;;$$$$
\t\t\t\t\t\t\t\t\t\t#$$$$$$$$#$##$$$$#$$$$$$$#$##$#$##$$$$##$#$##$#$#$$$$$$$$$$#$$$$#$$#$$$$$$$#$#$##$$##$$#$$$#$#$$$$$#
\t\t\t\t\t\t\t\t\t\t$#$$$$$$$$#$$$$$##$$$$#$#$#$$$$$##$$#$#$#$$$$$$$$$$$$$#$#$$$$#$#$$$$$$#$#$#$$##$$##$$$$$#$$$##$$$##$
""")
            print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t점수 : {}".format(score))
        else:
            print("""
\t\t\t\t\t\t\t\t\t\t$$$$$$$$#$##$$$$##$$$$$$$$$$$$$$#$$$$$$$$$#$$$$$$$$$$$#$#$$$$$$$$$$$$$$$$$$#$$$$$$$$#$$$$$$$$#$$$$$$
\t\t\t\t\t\t\t\t\t\t$$$$#$$#$$$#$::::::::::::::$$$$$$#$$#$$....*$$$$$#$#$$$$$$#$$$$$$$$##$$$$$#$$$#$#$$$$$$#$$....;$#$#$
\t\t\t\t\t\t\t\t\t\t$$$#$$#$$$$$#..............$$$$$$$#$$#$....*$$#$$#$$$$$$$$$$$$$$$$#$$$#$$$$$$$$$#$$##$$#$$....;$$$$$
\t\t\t\t\t\t\t\t\t\t$$$$$$$$$#$#$..............$#$$$$$$#$$$....*$$$$$##$$#$$$$$$#$$$$$$$$$$$$$$#$$##$$$$$$$#$$....;$$$#$
\t\t\t\t\t\t\t\t\t\t$$$$$$##$#$$$..............##$$#$$#$$$$....*$###$$$$$$$$$......................~$$$#$#$$$#....;$$$$$
\t\t\t\t\t\t\t\t\t\t$$#$#$$$$$$$$#$$#$$$$$$$$$$$$$$$$$$$$$$....*$$$$$$$$$##$#......................;#$$$$$$$$$....;$$$#$
\t\t\t\t\t\t\t\t\t\t$$$$$$$$$$$##$$$$#$$$$$$$$$$$$$#$$$$$$$....*$$$$$$$$$$$$#......................$#$$$$$$$$$....;$$$#$
\t\t\t\t\t\t\t\t\t\t$$#$#$#$$$$$$#$$#$$$$$$#$$#$$$$$#$$$$#$....*$$$$#$$#$$#$$......................$$$$$$$#$$#....;#$$$$
\t\t\t\t\t\t\t\t\t\t$$$$$!~~~~~~~~~~~~~~~~~~~~~~~~~~~~$$$$$....*$$$##$$$$$$$$$$$$##$#$$$$#$#$$$....$$$$$$$#$$$....;$$$$$
\t\t\t\t\t\t\t\t\t\t$$$$#:............................$$$$$....*$$$$#$$$#$$$$$$$$$$$$$$$$$$$$$:...-$**********....;$$$$$
\t\t\t\t\t\t\t\t\t\t$$$$#:............................$$$$#....*$$$$#$$#$$$$$$$#$$$$#$$#$$$$$#....$$..............;$$$$$
\t\t\t\t\t\t\t\t\t\t#$$#$:............................#$$$$....*$$$$$#$#$$#$#$$$$$###$#$$$#$$$....$$..............;#$$$$
\t\t\t\t\t\t\t\t\t\t$$$$$$$$$#$#$$$$$$$$$$#$$$$$#$$$$$$$$$$....*$$$$$$$$$$$$$$$$#$$$#$$$$$$$$....-$$..............;$$$$$
\t\t\t\t\t\t\t\t\t\t$$#$#$##$##$#$#$$$#$#$#$$$$#$$$$$$$$$#$....*$###$$$$$$$$$$#$#$#$$#$#$$#$$....$$$$$$###$$#$....;$$$$$
\t\t\t\t\t\t\t\t\t\t$$$$$$$$$$$$$$=.........-$$$$$$$$$$$$$$....;=======$$$$$$$$$#$$$$$$$$$$$....,$$$$$$$$$$$$$....;$$$$$
\t\t\t\t\t\t\t\t\t\t$$$$#$$$$$$$...............=$$$#$$$$$$$............$$$$$#$#$#$$$$$$$$#$~....$$$$$#$$$$$$$$....;$$$$$
\t\t\t\t\t\t\t\t\t\t$$#$$$##$$$.................,$$###$$$$#............$$#$$##$$#$$$$$$$$#=....:$$##$$$$$$$$$#....;#$$$$
\t\t\t\t\t\t\t\t\t\t$$$$$$$$$$......,:$#$$-......,$$$$$#$$$............#$$$$$#$$$$$$$$$$$$.....$#$$$$$$$$$#$##....;$$$$$
\t\t\t\t\t\t\t\t\t\t$$$$$#$$$.....,$$$$$$$$$$.....=#$$#$##$....*$$$$$$$$$$$$$#$$$#$##$$#$.....$$$$$$$$$$$#$$$$....;$$$##
\t\t\t\t\t\t\t\t\t\t$$$$#$#$$....~$$$$##$$$$$$.....$$$$$$$$....*#$$$$$#$$$$$$#$$$$$$$#$$.....=$$$$$$=$====$===....;#$$$$
\t\t\t\t\t\t\t\t\t\t#$$$$$#$;....#$#$###$##$##!....#$$$$$#$....*#$$$$$$#$$##$$$$$$$#$$~.....!$$$#$$~..............;$$$$$
\t\t\t\t\t\t\t\t\t\t$$$$##$$.....#$$$$$$$$$$#$$....#$$#$#$$....*$$$$$$$$$$$$$$$$$$#;......$$$$$$$$$:..............;$$$$$
\t\t\t\t\t\t\t\t\t\t$$$$$#$$=....#$$$$$$#$$$#$~....$$$$$$$$....*$$$#$$$##$$$$#$$$$.......$###$$#$$$$$#$$$#$$##....;$$$$$
\t\t\t\t\t\t\t\t\t\t#$$$$###$.....#$##$$$$$$#;....-$#$$$###....*#$$$$$$$$$##$#$~.......,#$$$$$$$##$$$$##$$$$$$....;$$$$$
\t\t\t\t\t\t\t\t\t\t$#$$$$#$$!.....,###$$$$$......$$#$$#$$$....*##$$$$#$$$$#~.........$#$##$$$$#$$$$#$$#$$$$$$....;$$$$$
\t\t\t\t\t\t\t\t\t\t$$$$#$$#$$...................$$$#$$$#$$....*$#$#$#$$$$#=........$$#$#$$$#$#$$$$##$$#$#$#$#....;$#$#$
\t\t\t\t\t\t\t\t\t\t$$$#$##$#$$!................$$$$$$#$$#$....*#$#$$$#$#$$$......$#$$#$$$$$$$$#$$$#$$#$#$$$#$....;$$$$$
\t\t\t\t\t\t\t\t\t\t$$$$$$$$$$$#$,............$$#$$$$$$#$$$....*$$$$$#$$$#$$$..,#$$$$$$$$$$$$$##$$$##$$$$#$#$$....;$$$#$
\t\t\t\t\t\t\t\t\t\t#$$$$$####$$$#$$$-....!$$$$##$$#$##$$$$$##$$$#$#$$$#$$$$#$#$$#$#$$#$$#$##$$$$$$#$$$#$#$$$#....;$$$$#
\t\t\t\t\t\t\t\t\t\t$$#$#$$$$$#$$$###$#$$$$$$$$#$#$$$$$$#$$$#$#$$#$$$$$$$##$#$$$$##$$$$#$$$$$$$$$##$#$$$$$$$$$$$#$#$$$$$
\t\t\t\t\t\t\t\t\t\t$$$$$$$$$$$#=~~~~#$$$$$$$$$$$$#$$$$$$#$,,,,*$$$$$$#$$$$$#$$$$$$$$#$##$$$$#$##$$$#$$$$$$$$$$$$$$$$$#$
\t\t\t\t\t\t\t\t\t\t$$$$#$##$$$$*....$$$$$$##$$$$$$$$$$$$$$....*$$$$#$$$$$#$$##$$$-,,,,,,,,,,,,,,,,-,,,,,,,,,,,,,,~#$$$$
\t\t\t\t\t\t\t\t\t\t$$$$$$$#$$$$*....$$$$$$$$$$$$#$$$$$$$$$....*$$$$$$$$$#$$$$$$$$................................-$$$$$
\t\t\t\t\t\t\t\t\t\t$#$$##$$#$$$*....$$$$#$$$$#$$#$$#$$$$$$....*$$$$$$$$$$#$$$$#$$................................-#$$$$
\t\t\t\t\t\t\t\t\t\t$$$$$#$$$$$$*....#$$$$$$$$$$$$$$$$$$$$$....*$$$$$$$$$$$$#$$$$$................................-$$$$$
\t\t\t\t\t\t\t\t\t\t$$$$###$$$$$*....##$$$$$$$#$$#$#$$$$#$$....*$$$$$$$$$$$##$$#$$$$$$$#$$$$$$$$$$#$$$$$$$$$$$,...-$$$$$
\t\t\t\t\t\t\t\t\t\t$$#$$$$####$=..............................*$$###$##$$#$$$$$$#$$$#$$$$####$$$$$$$$$#$#$$$$,...-$$$#$
\t\t\t\t\t\t\t\t\t\t$$$$###$$##$*..............................*#$$#$$$$$$$$$##$#$$$$$$$$$#$$$$###$$$$$$##$$$#,...-#$$$$
\t\t\t\t\t\t\t\t\t\t$$$$#$#$$$#$*..............................*$$$$#$$$$$$$$$$#$$$$$$$$#$$$$#$$#$$#$#$$$$$$$$,...-$$$$$
\t\t\t\t\t\t\t\t\t\t#$$$$$$$$$$$*....##$$$$##$###$$$$$$$#$$....*$$$$$$$#$#$$#$$$$$#$#$#$$$$$$$$$#$#$$$$$$$#$$$,...-#$$$$
\t\t\t\t\t\t\t\t\t\t#$#$$$$$$$$$*....$$$$$$#$$$#$$$#$$$$$$$....*$$$$#$$$$$$$$$$$$#$$#$$$$$$$$$$$#$$$$$#$$$#$$$,...-$$$$#
\t\t\t\t\t\t\t\t\t\t$$$$#$#$$$$$*....$#$$$$$$$$$$##$$$$$$#$....*$$$$$$$$#$#$$$$$$$$$$$$#$$$$$$$$$$$$$$#$$$$$#$,...-$$$$$
\t\t\t\t\t\t\t\t\t\t$$$$$$$$$$#$*....$$$$$$$$$$$$$$$#$$$$$$....*$$$$$$$$$$$$$$##$$$$$$$$$$$$$#$$$$$$$$$$$$#$$$,...-$$$$$
\t\t\t\t\t\t\t\t\t\t#$$$###$$$$$*....$$$#$$$$#$$$$$#$$$$$$$....*$$$$$$$$$$$$$$###$$$$$$$##$$$$$$#$$$##$$$#$$#$,...-$$$$$
\t\t\t\t\t\t\t\t\t\t$$$$#$$$$$$#*....$$$$$$#$$$$$$$$$#$$$$$....*$$$$$$#$$$#$$$$$$#$#$$$##$#$$$$#$$##$$$$$$$##$,...-$#$$$
\t\t\t\t\t\t\t\t\t\t$$$$$$$$$$#$*..............................*$$$$#$$#$$$$$$$$##$$#$$$#$#$$$$$$$$$$#$$$##$#$,...-$$$#$
\t\t\t\t\t\t\t\t\t\t$$$$$#$$$$#$*..............................*$$$$#$#$$$#$$$$$#$$$#$$$$$$$$#$###$$$$$$$$$$$#,...-$$$$$
\t\t\t\t\t\t\t\t\t\t#$$$##$$$$#$*..............................*$$$$$$$$$$#$$$$$#$#$$$$$$#$$$$$$#$$#$$$$#$$$$$,...-$$$$$
\t\t\t\t\t\t\t\t\t\t#$$$$$$$$$#$$#$$$#$$$$$##$##$$$$$$$#$$$#$$$$$$$$#$$#$$$$##$$$#$####$$#$$$$$$#$$$$$#$###$$#~---:$$$$$

""")
            print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t점수 : {}".format(score))

    # 오답노트 파일을 열어보는 함수
    def myNote(self):
        if not os.path.isdir("./오답노트"):
            os.mkdir("./오답노트")
        os.chdir("./오답노트")

        global Q
        msg = """\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t삭제 하시겠습니까? (\"네\" 또는 \"아니오\"를 기입해주세요) :"""

        while True:
            # 셔플하는 방법 알아보기.

            print(
                "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            print(
                "\t\t\t\t\t\t\t\t\t\t\t\t\t\t-----------------------------------------------오답노트-----------------------------------------------\n")
            for i in os.listdir(os.getcwd()):
                print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t", i)

                # for j in random(5):
            print(
                "\n\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t---------------------------------------------------------------------------------------------------")
            mode = "r"
            file_name = input("\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t(\"뒤로가기\"를 입력하면 메뉴창으로 이동합니다.)"
                              "\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t몇번 문제를 보시겠습니까? :")
            print(file_name)

            if os.path.isfile(file_name):
                while True:
                    file = open(file_name, mode)
                    print(
                        "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                    print(
                        "-----------------------------------------------오답노트-----------------------------------------------\n")
                    print("\n" + file.read())
                    print(
                        "\n\n---------------------------------------------------------------------------------------------------")
                    print("\n\n\n\n\n\n")
                    try:
                        Q = input(msg)
                    except ValueError:
                        print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t다시 입력해주세요.")
                    if Q == "네":

                        os.remove(file_name)
                        break
                        # 해당 파일 삭제

                    elif Q == "아니오":
                        break
                    else:
                        print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t다시 입력해주세요.")
                    file.close()
            elif file_name == "뒤로가기":
                os.chdir("../")
                print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                break
            else:
                print('\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t파일명을 다시 확인해주세요!!\n')


def Manager():
    dao = Dao()
    while True:
        print(managerPrompt)
        number = int(input("\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t숫자를 입력해주세요 :"))
        if number == 1:
            dao.addQ()
        elif number == 2:
            dao.editQ()
        elif number == 3:
            dao.removeQ()
        elif number == 4:
            dao.removeAllQ()
        elif number == 5:
            break
        elif number == 6:
            sys.exit(0)
        else:
            print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t숫자를 다시 입력해주세요.")


def User():
    if not os.path.isdir("../회원파일/{}".format(email)):
        os.mkdir("../회원파일/{}".format(email))
    os.chdir("../회원파일/{}".format(email))

    dao = Dao()
    while True:
        print(userPrompt)
        try:
            number = int(input("\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t숫자를 입력해주세요 :"))
            if number == 1:
                dao.exam()
            elif number == 2:
                dao.myNote()
            elif number == 3:
                break
            elif number == 4:
                sys.exit(0)
            else:
                print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t숫자를 다시 입력해주세요.")
        except ValueError:
            print("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n숫자를 기입해주세요.")


def main():
    if not os.path.isdir("/Users/joe/Documents/Python_PlayData/processingLicense/문제파일"):
        os.mkdir("/Users/joe/Documents/Python_PlayData/processingLicense/문제파일")
    os.chdir("/Users/joe/Documents/Python_PlayData/processingLicense/문제파일")

    while True:
        loginUser()
        try:
            if email == "Manager@naver.com":
                Manager()
            else:
                User()
        except NameError:
            print('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t다시입력하세요')


main()
