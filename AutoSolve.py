import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import random
import os

abcd = time.time()
webloc = r'C:\Users\hojun\Downloads\chromedriver_win32\chromedriver.exe'
webblof = r'C:\Users\hojun\Desktop\geckodriver-v0.23.0-win64\geckodriver.exe'

userids = 'kaspee'
userpwd = 'BLOCK'

driver = webdriver.Chrome(executable_path=webloc)


def login():
    # 자원을 로딩한다
    driver.implicitly_wait(10)

    driver.get('https://www.acmicpc.net/login')

    # ID를 입력한다
    id = driver.find_element_by_name('login_user_id')
    id.send_keys(userids)

    # PWD를 입력 한다
    id = driver.find_element_by_name('login_password')
    id.send_keys(userpwd)

    # 준 사이트 로그인 버튼 클릭
    driver.find_element_by_xpath("//*[@class='btn-u pull-right']").click()


def findsolve():
    count = 0
    temp = []
    # 백준 아이디를 이용하여, id로 로그인
    driver.get("https://www.acmicpc.net/status?user_id=" + userids)
    time.sleep(4)
    # 파싱하여, 모든 로그를 저장한다.
    # 로그는 다음과 같은 형식으로 저장되었다.
    # 11151808 kaspee 5988 맞았습니다!! 117592 120 PyPy3 / 수정 138 7시간 전
    SolveLogs = driver.find_element_by_xpath('//*[@id="status-table"]/tbody').find_elements_by_tag_name('tr')
    for i in range(len(SolveLogs)):
        # 로그를 알아볼 수 있는 텍스트 형식으로 바꾼다.

        SolveLogs[i] = str(SolveLogs[i].text)

    for log in SolveLogs:
        # 현재 시간과 푼 시간을 매치시키고, 아니면 False를 출력한다.

        temptime = mach(
            driver.find_element_by_xpath('//*[@id="solution-' + (str(log).split())[0] + '"]/td[9]/a').get_attribute(
                "data-original-title"))
        if ((log.split())[3] == '맞았습니다!!') and (temptime == True) and ((log.split())[2] not in temp):
            count += 1
            temp += [(log.split())[2]]

    # 풀 문제가 있으면 True, 아니면 Else를 반환합니다.
    return False if count > 1 else True


def mach(strSolve):
    # 날짜를 매치하는 함수이다.

    # 날짜를 변환시킵니다.
    temp = ''
    # strSolve = (strSolve.split()[0])[:-1] + (strSolve.split()[1])[:-1] + (strSolve.split()[2])[:-1]
    temp += (strSolve.split()[0])[:-1]
    if len((strSolve.split()[1])[:-1]) == 1:
        temp += '0' + (strSolve.split()[1])[:-1]
    else:
        temp += (strSolve.split()[1])[:-1]

    if len((strSolve.split()[2])[:-1]) == 1:
        temp += '0' + (strSolve.split()[2])[:-1]
    else:
        temp += (strSolve.split()[1])[:-1]

    nowtime = (str(datetime.datetime.now()).split()[0].replace('-', ''))
    if temp == nowtime:
        return True
    else:
        return False


def findnum():
    numlist = []
    driver.get('https://www.acmicpc.net/vs/boobot/' + userids)
    ids = driver.find_elements_by_xpath('/html/body/div[3]/div[2]/div/div[4]/div/div[2]/span')
    for i in ids:
        if i.text != '':
            numlist += [i.text]
    a = numlist[random.randrange(1, len(numlist))]

    return a


def beforesolving(SolveNum):
    driver.implicitly_wait(10)

    driver.get('https://www.acmicpc.net/login')

    # ID를 입력한다
    id = driver.find_element_by_name('login_user_id')
    id.send_keys('boobot')

    # PWD를 입력 한다
    id = driver.find_element_by_name('login_password')
    id.send_keys('BLOCK')

    # 백준 사이트 로그인 버튼 클릭
    driver.find_element_by_xpath("//*[@class='btn-u pull-right']").click()

    driver.get('https://www.acmicpc.net/status?from_mine=1&problem_id=' + str(SolveNum) + '&user_id=boobot')
    aaa = (driver.find_element_by_xpath('//*[@id="status-table"]/tbody/tr[1]').text)
    driver.get('https://www.acmicpc.net/submit/1316/' + (str(aaa).split())[0])
    inputblank = driver.find_element_by_xpath('//*[@id="code_open_open"]')
    inputblank.send_keys(Keys.TAB, Keys.CONTROL, 'a', 'c')
    driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[1]/div/ul/li[7]/a').click()


def solve(num):
    driver.get('https://www.acmicpc.net/submit/' + num)
    time.sleep(2)

    driver.find_element_by_xpath('//*[@id="language_chosen"]/a').click()
    solves = driver.find_element_by_xpath('//*[@id="language_chosen"]/div/div/input')
    solves.send_keys('python')
    solves.send_keys(Keys.ENTER)

    inputblank = driver.find_element_by_xpath('//*[@id="code_open_open"]')
    inputblank.send_keys(Keys.TAB, Keys.CONTROL, 'v')
    #driver.find_element_by_xpath('//*[@id="submit_button"]').click()
    print("completed")
    driver.close()

if __name__ == '__main__':
    aa = findnum()
    beforesolving(aa)
    login()
    solve(aa)
    print(aa)
    print(time.time()-abcd)
