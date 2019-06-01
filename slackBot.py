import requests
import slack
import os
import datetime


def getClient():
    client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])
    return client


def getNames(nick):
    headers = {
        'if-none-match': 'W/^\\^59f1ed700e57ec224ccd83d64fe559bf^\\^',
        'accept-encoding': 'gzip, deflate, br',
        'x-csrf-token': 'Vb+iFxZVsbFyKBYvObdbZRzj4tY9Q0PT+0j83VkxSVm3nu83JIRLqiTsXrONDzB37y8AC6Yp8sSHKiDyfuUGPw==',
        'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'content-type': 'application/json',
        'accept': 'application/json',
        'referer': 'https://www.hackerrank.com/{}?hr_r=1'.format(nick),
        'authority': 'www.hackerrank.com',
        'cookie': 'hackerrank_mixpanel_token=e695ac82-3f9d-4341-a38e-68665def55d7; hrc_l_i=F; _hrank_session=54fbfa3190957eea842e210e8974b9ca063ffb399c4784dc2abbddf2f7afaeecc8f90ce610526fc86b5560ae006a0cfb500b3b2d7ca81cc98d73bf8ba11d73d9; user_type=hacker',
    }
    return headers


def getBilgiler(nick):
    headers = {
        'accept-encoding': 'gzip, deflate, br',
        'x-csrf-token': 'Lvwx1oa2kFwjhQvOuOw+I5D7l1KE90azRDtVaUJqRe25/iJMh5WImyd0AU6trHkHOd0WsPppQRRP/TAcPwFYUA==',
        'accept-language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'content-type': 'application/json',
        'accept': 'application/json',
        'referer': 'https://www.hackerrank.com/{}?hr_r=1'.format(nick),
        'authority': 'www.hackerrank.com',
        'cookie': '_hrank_session=36682c1cb39a2f46a3d512b2ee148a0076ad0d57af06121d00789f6c0aab65a2ba1e4b30d87f0619a7db2fd06fe25f0f1db5ec3f53564a139df9fc8151285b43; user_type=hacker; h_r=login; h_l=body_middle_left_button; hackerrank_mixpanel_token=7a7db36a-8c0d-426d-9212-01eecce3b65f; react_var=true__trm2; react_var2=true__trm2; hrc_l_i=T; metrics_user_identifier=48ade0-1ffa99bc0caffb98b286bd899c3c23a77c27e981',
    }
    return headers


def main():
    client = getClient()
    toplam = 0
    icerik = {}
    nickler = ["fuatbeser",
               "aby_baran"]

    for nick in nickler:
        bilgiler = {}
        r = requests.get(
            'https://www.hackerrank.com/rest/hackers/{}/badges'.format(nick), headers=getBilgiler(nick))
        isimler = requests.get(
            'https://www.hackerrank.com/rest/contests/master/hackers/{}/profile'.format(nick), headers=getNames(nick))

        for bilgi in r.json()["models"]:
            if bilgi["url"] == "/domains/python":

                print("{} Yildiz Sayisi: ".format(nick), bilgi["stars"])
                bilgiler["Yildiz_Sayisi"] = ":star:"*bilgi["stars"]
                if bilgi["stars"] == 0:
                    bilgiler["Yildiz_Sayisi"] = ":face_with_rolling_eyes:"
                toplam += bilgi["stars"]

                print("{} Toplam Puan: ".format(nick), bilgi["current_points"])
                bilgiler["Toplam_Puan"] = bilgi["current_points"]

                print("{} Siralama: ".format(nick), bilgi["hacker_rank"])
                bilgiler["Siralama"] = bilgi["hacker_rank"]

                print("{} Cozulen Soru: ".format(nick), bilgi["solved"])
                bilgiler["Cozulen_Soru"] = bilgi["solved"]

                print("{} Link: www.hackerrank.com/{}".format(nick, nick))
                bilgiler["Link"] = "www.hackerrank.com/{}".format(nick)

                icerik[isimler.json()["model"]["name"]] = bilgiler

    for key, value in icerik.items():
        text = "*-- {} --* \n".format(key)
        for k, v in value.items():
            text += "{} --> {}\n".format(k.replace("_", " "), v)
        client.chat_postMessage(channel='#testing', text=text)
        client.chat_postMessage(channel='#testing', text="-"*50)

    client.chat_postMessage(channel='#testing', text="*Toplam Yildiz Sayisi --> {} x {}*".format(toplam, ":star:"))
    now = datetime.datetime.now()
    
    tarih = "*Tarih: {}/{}/{}*".format(now.day, now.month, now.year)
    client.chat_postMessage(channel='#testing', text=tarih)


if __name__ == "__main__":
    main()
    #TODO nickler yamldan alinacak 
    #TODO chanel yaml dan alinacak
    #TODO siralama yapilacak
    #TODO ay gun ayaralancak
	#TODO komuta tepki verme eklenecek