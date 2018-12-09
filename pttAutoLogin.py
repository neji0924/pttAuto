import telnetlib
import sys
import time
import json
import os

def login(account, password):
    global telnet
    telnet = telnetlib.Telnet('ptt.cc')
    time.sleep(1)
    content = telnet.read_very_eager().decode('big5','ignore')
    
    if u'系統過載' in content:
        sys.exit()

    if u"請輸入代號" in content:
        telnet.write((account + "\r\n").encode('big5'))
        time.sleep(1)
        content = telnet.read_very_eager().decode('big5','ignore')

        if u"請輸入您的密碼" in content:
            telnet.write((password + "\r\n").encode('big5'))
            time.sleep(2)
            content = telnet.read_very_eager().decode('big5','ignore')

            if u"密碼不對或無此帳號" in content:
                return
            
            if u"您想刪除其他重複登入的連線嗎" in content:               
                telnet.write(("n\r\n").encode('big5'))
                time.sleep(1)
                content = telnet.read_very_eager().decode('big5','ignore')

            if u"您要刪除以上錯誤嘗試的記錄嗎" in content:
                telnet.write(("Y\r\n").encode('big5'))
                
            if u"請按任意鍵繼續" in content:
                telnet.write(("\r\n").encode('big5'))
                time.sleep(2)
                content = telnet.read_very_eager().decode('big5','ignore')

def logout():
    telnet.write(b'qqqqqqg\r\ny\r\n')
    time.sleep(1)
    telnet.close()
        
def main():
    users = json.loads(os.environ.get('users', None))

    for user in users:
        login(user[0], user[1])
        time.sleep(3)
        logout()

if __name__ == '__main__' :
    main()