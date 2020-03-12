from django.shortcuts import render
import requests
from datetime import date
import hmac,hashlib
import base64 
import time
import tempfile 
import json
import random

diag = "Data Peserta Kosong"
hasil = ""
nokar = "Data Peserta Kosong(2)"
msg = ""
noRujukan = ""
fas = ""
ppkPelayanan = ""
poliRujukan = ""
pelayanan = ""
kelasRawat = ""
comment = ""
kodeSpesialisRujukan = ""
dpjp = ""
dateNow = str(date.today())
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
        try:
            diagnosa = request.POST['diagnosa']
            global diag
            global noRujukan
            global poliRujukan
            global pelayanan
            global kelasRawat
            global kodeSpesialisRujukan
            noRujukan = diagnosa
            url = 'https://new-api.bpjs-kesehatan.go.id:8080/new-vclaim-rest/Rujukan/RS/%s' % diagnosa 
            headers = {
                "Accept":"application/json", 
                "X-cons-id":consID,
                "X-timestamp":stamp,
                "X-signature":encodesignature
            }

            response = requests.get(url,headers = headers)
            diag = response.json()

            # for i in range(100):
            #     pin = ''.join(random.choice('0123456789') for _ in range(6))
            #     print(i)
            
            print(diag)
            # print(pin + " ini random numbernya")

            poliRujukan = diag['response']['rujukan']['provPerujuk']['kode']
            pelayanan = diag['response']['rujukan']['pelayanan']['kode']
            kelasRawat = diag['response']['rujukan']['peserta']['hakKelas']['kode']
            kodeSpesialisRujukan = diag['response']['rujukan']['poliRujukan']['kode']
            # print(kodeSpesialisRujukan)
            # print(kelasRawat)
            # print(pelayanan)

            # print(consID)
            print(stamp)
            print(encodesignature)
        except:
            return "none"

    elif 'nomorKartu' in request.POST:
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
        nokartu = request.POST['nomorKartu']
        global nokar
        url = 'https://new-api.bpjs-kesehatan.go.id:8080/new-vclaim-rest/Rujukan/RS/Peserta/%s' % nokartu
        headers = {
            "Accept":"application/json", 
            "X-cons-id":consID,
            "X-timestamp":stamp,
            "X-signature":encodesignature
        }

        response = requests.get(url,headers = headers)
        nokar = response.json()
        print(nokar)

    elif 'faskes' in request.POST:

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
        try:
            global comment
            comment = request.POST['catatan']
            faskes = request.POST['faskes']
            global fas
            url = 'https://new-api.bpjs-kesehatan.go.id:8080/new-vclaim-rest/referensi/faskes/%s/2' % faskes 
            headers = {
                "Accept":"application/json", 
                "X-cons-id":consID,
                "X-timestamp":stamp,
                "X-signature":encodesignature
            }

            response = requests.get(url,headers = headers)
            fas = response.json()
            global ppkPelayanan
            ppkPelayanan = fas['response']['faskes'][0]['kode']
            print(ppkPelayanan)
            print(comment)
            # print(consID)
            # print(stamp)
            # print(encodesignature)
        except:
            return "none"


    elif 'dpjp' in request.POST:

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
        try:
            url = 'https://new-api.bpjs-kesehatan.go.id:8080/new-vclaim-rest/referensi/dokter/pelayanan/'+ pelayanan + '/tglPelayanan/'+ dateNow + '/Spesialis/' + kodeSpesialisRujukan
            headers = {
                "Accept":"application/json", 
                "X-cons-id":consID,
                "X-timestamp":stamp,
                "X-signature":encodesignature
            }

            global dpjp
            response = requests.get(url,headers = headers)
            dpjp = response.json()
            # dp = fas['response']['faskes'][0]['kode']
            # print()
            # print(comment)
            # print(consID)
            # print(stamp)
            # print(encodesignature)
        except:
            return "none"



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
        noMR = diag['response']['rujukan']['peserta']['mr']['noMR']
        tglrujukan = diag['response']['rujukan']['tglKunjungan']
        diagAwal = diag['response']['rujukan']['diagnosa']['kode']
        poliTujuan = diag['response']['rujukan']['poliRujukan']['kode']
        noDpjp = dpjp['response']['list'][0]['kode']
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
                 "noKartu": noKartu,
                 "tglSep": dateNow,
                 "ppkPelayanan": ppkPelayanan, # ini diambil di fasilitas kesehatan
                 "jnsPelayanan": pelayanan, # rawat jalan pasti
                 "klsRawat": kelasRawat, # kelas rawat diambil dari kelas bpjs
                 "noMR": noMR, 
                 "rujukan": {
                    "asalRujukan": "2", # faskes 1 , faskes 2 RS
                    "tglRujukan": tglrujukan, #diambil dari tgl kunjungan
                    "noRujukan": noRujukan, 
                    "ppkRujukan": poliRujukan #diambil dari kode faskes
                 },
                 "catatan": comment, #diambil dari client
                 "diagAwal": diagAwal, 
                 "poli": {
                    "tujuan": poliTujuan,
                    "eksekutif": "0" #diambil dari client
                 },
                 "cob": {
                    "cob": "0" # null
                 },
                 "katarak": {
                    "katarak": "0" #null
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
                    "noSurat": "098908", #diambil di client mau dokter dpjp
                    "kodeDPJP": noDpjp # ^^ referensinya di dokter dpjp
                 },
                 "noTelp": "09809809809", #isi dengan no hp client
                 "user": "XX" # null
              }
           }
        })               
                                 
                      
        response2 = requests.post(url,data = dataKey ,headers = headers) #ngirim ke server BPJS untuk insert SEP

        # clientresponse = requests.post('api server client', data = 'data clientnya apa', headers = 'headersnya apa') # ini untuk ke client
        global hasil
        hasil = response2.json()
        print(hasil)
   
    return render(request,'index.html', {
        'diagnosa':diag,
        'hasil': hasil,
        'nokar': nokar,
        'field': msg,
        'noRujukan':noRujukan,
    })



def table(request):
    return render(request,'table.html')

def printsep(request):
    data = request.POST.get('sep')
    print(data)
    return render(request,'printsep.html',{
        'data':data
    })