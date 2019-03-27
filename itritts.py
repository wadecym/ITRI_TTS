from zeep import Client
import time

#ITRI TTS Web Services API Url : http://tts.itri.org.tw/development/web_service_api.php

#itri SOAP 連接網址
itri_tts_soap_url = 'http://tts.itri.org.tw/TTSService/Soap_1_3.php?wsdl'
soapclient = Client(itri_tts_soap_url)

#itri 申請帳號/密碼
account = '帳號'
password = '密碼'

#要語音合成的文字
text = '鳳凰臺上鳳凰遊，鳳去臺空江自流。吳宮花草埋幽徑，晉代衣冠成古丘。三山半茖青天外，二水中分白鷺洲。總為浮雲能蔽日，長安不見使人愁。'

def get_tts(username,password,text):
    #ConvertSimple 是使用官網預設好的語音參數,如果需要調整人聲或其他參數可以使用 ConvertText 或 ConvertAdvancedText, 詳細情況請參考官網說明
    result = soapclient.service.ConvertSimple(username,password,text)
    resultcode=result.split('&')[0]
    print('預合成狀態 : ',result)
    #resultcode不為0表示有其他錯誤,錯誤代碼請參閱官網說明
    if resultcode == '0':
        #成功後可以拿到號碼牌
        convertid=result.split('&')[-1]
        print('號碼牌 :',convertid)
        #等待一段時間後再拿convertid這個號碼牌去查詢網站是否已經轉好檔案
        #直接去查詢的結果通常都是在排隊中
        time.sleep(15)
        data = get_ttsurl(username,password,convertid)
        return data

def get_ttsurl(username,password,convertid):
    tts_resule=soapclient.service.GetConvertStatus(username,password,convertid)
    print('查詢結果 : ',tts_resule)
    statuscode = tts_resule.split('&')[-2]

    # 如果查詢結果是0表示還在排隊中,如果是1表示網站正在處理中,不管哪種都還是要等
    if statuscode == '0' or statuscode == '1':
        time.sleep(10)
        data = get_ttsurl(username, password, convertid)
        return data

    # 如果查詢結果出現completed表示已經轉檔完成
    if statuscode=='completed':
        # 拿到語音網址後依個人需求看是要下載檔案或是撥放
        tts_url = tts_resule.split('&')[-1]
        print('語音合成網址:',tts_url)
        return tts_url
    else:
        print('語音合成錯誤')
        return 'error'
get_tts(account,password,text)