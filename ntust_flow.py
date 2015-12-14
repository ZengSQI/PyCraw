import re
import sys
import requests


class NtustFlow:

    _url = "http://web.ntust.edu.tw/~B10315030/flow.php"

    def __init__(self):
        self._ip = NtustFlow.get_ip()
        self.fresh()

    def set_ip(self, ip):
        self._ip = ip
        self.fresh()

    @staticmethod
    def get_ip():
        content = requests.get("http://orange.tw")
        ip = re.search(r'(\d+\.\d+\.\d+\.\d+)', content.text).group(1)
        return ip
    
    def fresh(self):
        response = requests.post(NtustFlow._url, data={"ip": self._ip})
        content = response.text
        pattern = re.compile('<div.*?texttotal">.*?<h2>.*?(\d+).*?</h2>.*?(\d+).*?(\d+).*?</div>', re.S)

        items = re.split(pattern, content)

        self._total = items[1]
        self._download = items[2]
        self._upload = items[3]

    def get_total(self):
        return self._total

    def get_download(self):
        return self._download

    def get_upload(self):
        return self._upload
    
    def main():
        data = NtustFlow()
        try:
            ip = sys.argv[1]
        except:
            ip = NtustFlow.get_ip()
            if re.match(r'140\.118.*?', ip, re.S):
                pass
            else:
                ip = "140.118.127.30"
        data.set_ip(ip)
        print ("IP : " + ip)
        print ("Total used : " + data.get_total() + " Mb")
        print ("Download : " + data.get_download() + " Mb")
        print ("Upload : " + data.get_upload() + " Mb")


if __name__ == '__main__':
    NtustFlow.main()
