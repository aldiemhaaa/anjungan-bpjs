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
        global noRujukan
        noRujukan = diagnosa
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
        noMR = diag['response']['rujukan']['peserta']['mr']['noMR']
        tglrujukan = diag['response']['rujukan']['tglKunjungan']
        diagAwal = diag['response']['rujukan']['diagnosa']['kode']
        poliTujuan = diag['response']['rujukan']['poliRujukan']['kode']
        # noRujukan = request.POST['diagnosa']
        dateNow = str(date.today())
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
                 "tglSep": dateNow,
                 "ppkPelayanan": "0601R001", # ini diambil di fasilitas kesehatan
                 "jnsPelayanan": "2", # rawat jalan pasti
                 "klsRawat": "2", # kelas rawat diambil dari kelas bpjs
                 "noMR": noMR, 
                 "rujukan": {
                    "asalRujukan": "2", # faskes 1 , faskes 2 RS
                    "tglRujukan": tglrujukan, #diambil dari tgl kunjungan
                    "noRujukan": noRujukan, 
                    "ppkRujukan": "0609R002" #diambil dari kode faskes
                 },
                 "catatan": "TEST", #diambil dari client
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
                    "kodeDPJP": "30468" # ^^ referensinya di dokter dpjp
                 },
                 "noTelp": "09809809809", #isi dengan no hp client
                 "user": "XX" # null
              }
           }
        })               
                                 
                      
        response2 = requests.post(url,data = dataKey ,headers = headers)
        global hasil
        hasil = response2.json()
        print(hasil)


    return render(request,'index.html', {
        'diagnosa':diag,
        'hasil': hasil,
    })

