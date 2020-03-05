from django.shortcuts import render
import requests
from datetime import date
import hmac,hashlib
import base64 
import time
import tempfile 
import json



diag = {}
hasil = {}
def index(request):
    if 'diagnosa' in request.POST:
        consID = '27952'
        # secretKey = 'rsm32h1'
        stamp = str(
                round(
                    time.time()
                )
                )
        data = consID + '&' + stamp
        resultdata = data.encode("utf-8")
        signature = hmac.new(b"rsm32h1", resultdata, digestmod=hashlib.sha256).digest()
        encodesignature = base64.b64encode(signature).decode()
        diagnosa = request.POST['diagnosa']
        url = 'https://new-api.bpjs-kesehatan.go.id:8080/new-vclaim-rest/Rujukan/RS/%s' % diagnosa 
        headers = {
            "Accept":"application/json", 
            "X-cons-id":consID,
            "X-timestamp":stamp,
            "X-signature":encodesignature
        }

        response = requests.get(url,headers = headers)
        global diag
        diag = response.json()
        print(diag)
    elif request.POST:
        consID = '27952'
        # secretKey = 'rsm32h1'
        stamp = str(
                round(
                    time.time()
                )
                )
        data = consID + '&' + stamp
        resultdata = data.encode("utf-8")
        signature = hmac.new(b"rsm32h1", resultdata, digestmod=hashlib.sha256).digest()
        encodesignature = base64.b64encode(signature).decode()
        noKartu = diag['response']['rujukan']['peserta']['noKartu']
        url = 'https://new-api.bpjs-kesehatan.go.id:8080/new-vclaim-rest/SEP/1.1/insert'
        headers = {
            "Accept":"application/json", 
            "X-cons-id":consID,
            "X-timestamp":stamp,
            "X-signature":encodesignature
        }
        dataKey = json.dumps({
           "request": {
              "t_sep": {
                #   "0001848267911"
                 "noKartu": noKartu,
                 "tglSep": "2020-03-03",
                 "ppkPelayanan": "0601R001",
                 "jnsPelayanan": "2",
                 "klsRawat": "2",
                 "noMR": "1120059",
                 "rujukan": {
                    "asalRujukan": "2",
                    "tglRujukan": "2020-01-03",
                    "noRujukan": "0609R0020120B000006",
                    "ppkRujukan": "0609R002"
                 },
                 "catatan": "TEST",
                 "diagAwal": "C55",
                 "poli": {
                    "tujuan": "018",
                    "eksekutif": "0"
                 },
                 "cob": {
                    "cob": "0"
                 },
                 "katarak": {
                    "katarak": "0"
                 },
                 "jaminan": {
                    "lakaLantas": "0",
                    "penjamin": {
                        "penjamin": "",
                        "tglKejadian": "",
                        "keterangan": "",
                        "suplesi": {
                            "suplesi": "0",
                            "noSepSuplesi": "",
                            "lokasiLaka": {
                                "kdPropinsi": "",
                                "kdKabupaten": "",
                                "kdKecamatan": ""
                                }
                        }
                    }
                 },
                 "skdp": {
                    "noSurat": "098908",
                    "kodeDPJP": "30468"
                 },
                 "noTelp": "09809809809",
                 "user": "XX"
              }
           }
        })               
                                 
                      
        response2 = requests.post(url,data = dataKey ,headers = headers)
        global hasil
        hasil = response2.json()
        # message = result['metaData']['message']
        # print(message)
    #     print(stamp)
    #     print(encodesignature)
        # print(int(noKartu))
        # print(noKartu)
        # print(response.json())
        # print(list(diag['response']))

    return render(request,'index.html', {
        'diagnosa':diag,
        'hasil': hasil,
        # 'stamp': stamp,
        # 'signature': encodesignature,
        # 'consID' : consID,
        # 'faskes' : faskes,
        # 'dateToday' : today
    })

# def index(request):
#     diag = {}
#     if request.method == request.GET:
#         diagnosa = request.GET['diagnosa']
#         url = 'https://new-api.bpjs-kesehatan.go.id:8080/Rujukan/%s' % diagnosa
#         headers = {
#             "Accept":"application/json", 
#             "X-cons-id":consID,
#             "X-timestamp":stamp,
#             "X-signature":encodesignature
#         }
#         response = requests.get(url,headers = headers)
#         diag = response.json()
        
#         print(diag)
#     return render(request,'index.html', {
#         'diagnosa':diag,
#     })


