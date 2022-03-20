from bs4 import BeautifulSoup
import requests
import os


class App:

    def __init__(self):
        self.userlist = []     
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
        self.cookie = self.GetCookies()
        self.page = 1
        self.reportedList = []
        os.system("title "+"THT IHBAR OTOMASYONU")
        os.system("color F")
        try:
            self.hashUser=self.cookie[0].strip()
            self.hashTfaTrust =self.cookie[1].strip()
            self.cookies = {
                'xf_user':f'{self.hashUser}',
                'xf_tfa_trust':f'{self.hashTfaTrust}'
            }
        except:
            print("Hatalı Cookies Verisi Lütfen Kontrol Ediniz !")
            input()
            exit()
        self.Transactions()


    def GetCookies(self):
        try:
            file = open("cookies.txt", "r")
            cookies = file.readlines()
            file.close()
            return cookies
        except:
            print("Cookies.txt Dosyası Bulunamadı. Uygulamayı kapatmak için lütfen bir tuşa basınız.")
            input()
            exit()


    def ControlAccount(self):
        request = requests.get("https://www.turkhackteam.org/uye/kaptantr.744109/", cookies=self.cookies, headers = self.headers)
        controltext = "Giriş yap"
        html = request.text
        if controltext in html:
            return "Giris Yapılmadı"
        else:
            return"Giriş Yapıldı"

    
    def Scarping(self):
        request = requests.get("https://www.turkhackteam.org/reports/closed?page="+ str(self.page), cookies=self.cookies, headers=self.headers).text
        parser = BeautifulSoup(request, 'html.parser')
        urls = parser.findAll("a", {"class": "structItem-title"},href=True)
        for url in urls:
            file = open("rapor.txt","a",encoding='utf-8')
            file.write("*"*40)
            file.write("\n")
            reportedLink = "https://www.turkhackteam.org"+url["href"]
            request = requests.get(reportedLink, cookies=self.cookies, headers=self.headers).text
            contentParser = BeautifulSoup(request, 'html.parser')
            content = contentParser.find_all("header",{"class":"message-attribution message-attribution--plain"})

            for item in content:
                userLink = item.find('a')["href"]
                userLink = "https://www.turkhackteam.org"+userLink
                userSituation = item.find("span", {"class": "label label--accent"})
                userSituation = userSituation is None
                userName = item.find('h4',{"class":"attribution"}).text

                userSituation ={True: "İhbar Yapan", False: "İhbar Eden"} [userSituation]
                text = f"{userLink} // {userName} // ({userSituation})"
                file.write(reportedLink)
                file.write("\n")
                file.write(text)
                file.write("\n")
                file.write("-"*20) 
                file.write("\n")
                
        file.close()


    def Transactions(self):
        print(""" 
        ///////////////////////////////////////////
        //                                       //
        //          THT Ihbar  Otomasyonu        //
        //                  1.0                  //
        //                                       //
        //              Created By               //
        //              Ar-Ge Team               //
        /////////////////////////////////////////// 
        
        """)

        if self.ControlAccount() == "Giris Yapılmadı":
            print("Giriş Yapılamadı. Çıkış yapmak için lütfen bir tuşa basınız.")
            input()
            exit()
        else:
            print(f"Login Control: {self.ControlAccount()}")
            print("İşlem Başladı, Lütfen Bekleyiniz")
            self.Scarping()
            print("İşlem Tamamlandı, Çıkış Yapmak İçin Bir tuşa Basınız.")
            input()
               

if __name__ == '__main__':
    main = App()