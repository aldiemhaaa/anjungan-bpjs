from django.shortcuts import render
from datetime import date
import requests,hmac,hashlib,base64,time, tempfile , json ,random
from .models import generatekey,Sep
import re

diag, hasil, nokar, msg, noRujukan, fas, ppkPelayanan, poliRujukan, pelayanan, kelasRawat, comment, kodeSpesialisRujukan, dpjp,noSep = " "*14
dateNow = str(date.today())

# Header API BPJS
def generateHeader():
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
    headers = {
        "Accept":"application/json", 
        "X-cons-id":consID,
        "X-timestamp":stamp,
        "X-signature":encodesignature
    }
    return consID,stamp,encodesignature,headers

def getApi(endpoint):
    response = requests.get(endpoint,headers = generateHeader()[3])
    diag = response.json()
    return diag
    
def postApi(endpoint,dataKey):
    response = requests.post(endpoint,data = dataKey, headers = generateHeader()[3])
    hasil = response.json()
    return hasil

def index(request):
    global diag, hasil, nokar, msg, noRujukan, fas, ppkPelayanan, poliRujukan, pelayanan, kelasRawat, comment, kodeSpesialisRujukan, dpjp,noSep,hasil
    if 'nomorKartu' in request.POST:
        global nokar
        nokartu = request.POST['nomorKartu']
        url = 'https://new-api.bpjs-kesehatan.go.id:8080/new-vclaim-rest/Rujukan/RS/Peserta/%s' % nokartu
        
        nokar = getApi(url)
        diag = nokar
    #     global hasil
    #     hasil = postApi(url,dataKey)
    #     # print(hasil)
    #     # if hasil['response']['noSep'] == '':
    #     #     noSep = hasil['response']['noSep']
    #     #     print(noSep)
    #     # else:
    #     #     print(hasil)
    #     # try: 
    #     #     print(hasil['response']['noSep'])
    #     #     resultnoSep = hasil['response']['noSep']
    #     #     Sep.objects.create(key = resultnoSep)
    #     # except TypeError:
    #     #     # print(hasil)
    #     #     # listnoSep = Sep.objects.all()
    #     #     hasilnya = hasil['metaData']['message'] 
    #     #     result = hasilnya.rsplit(' ', 1)[1]
    #     #     filterSep = Sep.objects.filter(key = result)
    #     #     print(filterSep)
    #         # print(Sep.objects.all())
    #         # if result == filterSep:
    #         #     print(result +" ini sudah ada di dalam database, juga sudah dicetak")
    #         # else:
    #         #     Sep.objects.create(key = result)
    #         #     print(result+" ini ini ")
    #     # print(generateKey())
    return render(request,'index.html', {
        'diagnosa':diag,
        'hasil': hasil,
        'nokar': nokar,
        'field': msg,
        'noRujukan':noRujukan,
    })

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return random.randint(range_start, range_end)


def generateKey():  
    waktu = round(time.time())
    strWaktu = str(waktu)
    resultWaktu = strWaktu[4:10]
    lists = generatekey.objects.all()
    if strWaktu not in lists:
        generatekey.objects.create(key = resultWaktu)
        resultBaru = list(reversed(generatekey.objects.all()))
        hasil = resultBaru[0] 
        return hasil
    else:
        return False    

def cetakSep(request):
    try: 
        # get variable global
        global diag, hasil, nokar, msg, noRujukan, fas, ppkPelayanan, poliRujukan, pelayanan, kelasRawat, comment, kodeSpesialisRujukan, dpjp,noSep,hasil
        # get input from user
        diagnosa = request.POST.get('rujuk')
        # faskes
        url = 'https://new-api.bpjs-kesehatan.go.id:8080/new-vclaim-rest/Rujukan/RS/%s' % diagnosa # get peserta via no rujukan
        urlfaskes = 'https://new-api.bpjs-kesehatan.go.id:8080/new-vclaim-rest/referensi/faskes/Hoesin/2' # get kode RS Hoesin Palembang
        noRujukan = diagnosa
        #get api rujukan
        diag = getApi(url) 
        #get api faskes
        fas = getApi(urlfaskes)

        # retrieve data
        poliRujukan = diag['response']['rujukan']['provPerujuk']['kode']
        pelayanan = diag['response']['rujukan']['pelayanan']['kode']
        kelasRawat = diag['response']['rujukan']['peserta']['hakKelas']['kode']
        kodeSpesialisRujukan = diag['response']['rujukan']['poliRujukan']['kode']
        ppkPelayanan = fas['response']['faskes'][0]['kode']

        #url api dpjp
        urldpjp = 'https://new-api.bpjs-kesehatan.go.id:8080/new-vclaim-rest/referensi/dokter/pelayanan/'+ pelayanan + '/tglPelayanan/'+ dateNow + '/Spesialis/' + kodeSpesialisRujukan
        # get api dpjp
        dpjp = getApi(urldpjp)
        
        # retrieve data 
        noDpjp = dpjp['response']['list'][0]['kode']
        noKartu = diag['response']['rujukan']['peserta']['noKartu']
        noMR = diag['response']['rujukan']['peserta']['mr']['noMR']
        tglrujukan = diag['response']['rujukan']['tglKunjungan']
        diagAwal = diag['response']['rujukan']['diagnosa']['kode']
        poliTujuan = diag['response']['rujukan']['poliRujukan']['kode']
        noDpjp = dpjp['response']['list'][0]['kode']

        # generate key from function generateKey()
        noSurat = str(generateKey())

        # api url to insert sep
        urlInsertSep = 'https://new-api.bpjs-kesehatan.go.id:8080/new-vclaim-rest/SEP/1.1/insert'

        # data to post Insert Sep
        dataKey = json.dumps({
           "request": {
              "t_sep": {
                 "noKartu": noKartu, #no kartu from peserta
                 "tglSep": dateNow, #generate time now
                 "ppkPelayanan": ppkPelayanan, # ini diambil di fasilitas kesehatan
                 "jnsPelayanan": pelayanan, # rawat jalan pasti
                 "klsRawat": kelasRawat, # kelas rawat diambil dari kelas bpjs
                 "noMR": noMR, # retrieve from no rujukan or no kartu
                 "rujukan": {
                    "asalRujukan": "2", # faskes 1 , faskes 2 RS
                    "tglRujukan": tglrujukan, #diambil dari tgl kunjungan
                    "noRujukan": noRujukan, #get from user input no rujukan
                    "ppkRujukan": poliRujukan #diambil dari kode faskes
                 },
                 "catatan": comment, #diambil dari client
                 "diagAwal": diagAwal, #diambil di diagnosa awal noRujukan/NoKartu
                 "poli": {
                    "tujuan": poliTujuan, #diambil dari poliRujukan
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
                    "noSurat": noSurat, # generate from stamp 
                    "kodeDPJP": noDpjp # ^^ referensinya di dokter dpjp
                 },
                 "noTelp": "09809809809", #isi dengan no hp client
                 "user": "ANJUNGAN" # null
              }
           }
        })
        hasil = postApi(urlInsertSep,dataKey)
        # print(type(hasil['metaData']['message']))
        # print(hasil)
        # print(hasil['response']['noSep'])
        # print(type(hasil['response']['noSep']))
        # print(type(str(hasil['response']['noSep'])))

        if hasil['metaData']['message'] == "Sukses":
            print(hasil)
            result = hasil['response']['sep']['noSep']
            Sep.objects.create(nomorsep = result,nomorsuratkontrol = noSurat)
            # print(result)
        else:
            # print(generateHeader())
            print(noSurat)
            print(hasil['metaData']['message'])
            # print(hasil)
        # generate nomor surat dan post ke database berbarengan post noSep ke database            
        # try: 
        # result = hasil['response']['noSep']
        #     # resultnoSep = hasil['response']['noSep']
        #     # Sep.objects.create(nomorsep = resultnoSep, nomorsuratkontrol = generatekey())
        # except TypeError:
        #     result = "NO SEP SUDAH ADA"
        #     return result
            # print(hasil)
            # listnoSep = Sep.objects.all()
            # hasilnya = hasil['metaData']['message'] 
            # result = hasilnya.rsplit(' ', 1)[1]
            # filterSep = Sep.objects.filter(key = result)
            # print(filterSep)
            # print(Sep.objects.all())
            # if result == filterSep:
            #     print(result +" ini sudah ada di dalam database, juga sudah dicetak")
            # else:
            #     Sep.objects.create(key = result)
            #     print(result+" ini ini ")
        # print(generateKey())
    except:
        return False

    return render(request,'cetaksep.html',{
        'rujukan':diag,
        # 'hasil':hasil
    })