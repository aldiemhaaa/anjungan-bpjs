from django.shortcuts import render
from datetime import date
import requests,hmac,hashlib,base64,time, tempfile , json ,random
from .models import generatekey,Sep
import re

diag, hasil, nokar, msg, noRujukan, fas, ppkPelayanan, poliRujukan, pelayanan, kelasRawat, comment, kodeSpesialisRujukan, dpjp,noSep,diagnosa = " "*15
noKartu, noMR, tglrujukan, diagAwal, poliTujuan, noDpjp,resultsep,aksiSep = " "*8
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
    # response = requests.get(endpoint,headers = generateHeader()[3])
    response = requests.get(endpoint)
    diag = response.json()
    return diag

def getApiHeader(endpoint):
    response = requests.get(endpoint,headers = generateHeader()[3])
    diag = response.json()
    return diag
    
def postApi(endpoint,dataKey):
    response = requests.post(endpoint,data = dataKey)
    hasil = response.json()
    return hasil

def postApiHeader(endpoint,dataKey):
    response = requests.post(endpoint,data = dataKey,headers = generateHeader()[3])
    hasil = response.json()
    return hasil

def index(request):
    global diag, hasil, nokar, msg, noRujukan, fas, ppkPelayanan, poliRujukan, pelayanan, kelasRawat, comment, kodeSpesialisRujukan, dpjp,noSep,hasil
    # if 'nomorKartu' in request.POST:
    #     global nokar
    #     nokartu = request.POST['nomorKartu']
    #     url = 'https://new-api.bpjs-kesehatan.go.id:8080/new-vclaim-rest/Rujukan/RS/Peserta/%s' % nokartu
        
    #     nokar = getApi(url)
    #     diag = nokar
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


def pilihDokter(request):
    try: 
        # get variable global
        global diagnosa, diag, hasil, nokar, msg, noRujukan, fas, ppkPelayanan, poliRujukan, pelayanan, kelasRawat, comment, kodeSpesialisRujukan, dpjp,noSep,hasil,noDpjp,noKartu, noMR, tglrujukan, diagAwal, poliTujuan, noDpjp
        # get input from user
        if 'rujuk' in request.POST:
            diagnosa = request.POST.get('rujuk')
            url = 'http://10.1.0.6/rest-anjungan/api/bpjs/rujukan/%s' % diagnosa # get peserta via no rujukan
            diag = getApi(url) 
        elif 'nomorKartu' in request.POST:
            getnomorKartu = request.POST.get('nomorKartu')
            url = 'http://10.1.0.6/rest-anjungan/api/bpjs/rujukan/peserta/%s' % getnomorKartu
            nokar = getApi(url)
            diag = nokar
            # diagnosa = cariberdasarkartu
        # faskes
        # urlfaskes = 'https://new-api.bpjs-kesehatan.go.id:8080/new-vclaim-rest/referensi/faskes/Hoesin/2' # get kode RS Hoesin Palembang
        noRujukan = diagnosa
        #get api rujukan
        #get api faskes
        # fas = getApi(urlfaskes)

        # retrieve data
        poliRujukan = diag['response']['rujukan']['provPerujuk']['kode']
        pelayanan = diag['response']['rujukan']['pelayanan']['kode']
        kelasRawat = diag['response']['rujukan']['peserta']['hakKelas']['kode']
        kodeSpesialisRujukan = diag['response']['rujukan']['poliRujukan']['kode']
        ppkPelayanan = '0601R001'

        #url api dpjp
        urldpjp = 'https://new-api.bpjs-kesehatan.go.id:8080/new-vclaim-rest/referensi/dokter/pelayanan/'+ pelayanan + '/tglPelayanan/'+ dateNow + '/Spesialis/' + kodeSpesialisRujukan
        # get api dpjp
        dpjp = getApiHeader(urldpjp)
        print(dpjp)
        # retrieve data 
        noKartu = diag['response']['rujukan']['peserta']['noKartu']
        noMR = diag['response']['rujukan']['peserta']['mr']['noMR']
        tglrujukan = diag['response']['rujukan']['tglKunjungan']
        diagAwal = diag['response']['rujukan']['diagnosa']['kode']
        poliTujuan = diag['response']['rujukan']['poliRujukan']['kode']
        print(generateHeader())
       
    except:
        return False

    return render(request,'pilihdokter.html',{
        'rujukan':diag,
        'dpjp':dpjp,
        # 'hasil':hasil
    })

def cetakSep(request):
    global diag, hasil, nokar, msg, noRujukan, fas, ppkPelayanan, poliRujukan, pelayanan, kelasRawat, comment, kodeSpesialisRujukan, dpjp,noSep,hasil,noDpjp,noKartu, noMR, tglrujukan, diagAwal, poliTujuan, noDpjp
    noDokterDpjp = request.POST.get('kode')
    
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
                "kodeDPJP": noDokterDpjp # ^^ referensinya di dokter dpjp
                },
                "noTelp": "09809809809", #isi dengan no hp client
                "user": "ANJUNGAN" # null
            }
        }
    })
    hasil = postApiHeader(urlInsertSep,dataKey)
    # global resultsep
    if hasil['metaData']['message'] == "Sukses":
        global resultsep
        resultsep = hasil['response']['sep']['noSep']
        Sep.objects.create(nomorsep = resultsep,nomorsuratkontrol = noSurat)
        print(hasil)
    else:
        # global resultsep
        global aksiSep
        # print(generateHeader())
        # print(noSurat)
        # print(hasil['metaData']['message'])
        hasilnya = hasil['metaData']['message']
        hasilSep = hasilnya.rsplit(' ', 1)[1]
        urlgetSep = 'https://new-api.bpjs-kesehatan.go.id:8080/new-vclaim-rest/SEP/'+ hasilSep
        aksiSep = getApiHeader(urlgetSep)
        print(aksiSep)
        resultsep = aksiSep
        print(resultsep)    
        # print('sep sudah ada')

    return render(request,'cetaksep.html',{
        'hasil':hasil,
        'result':resultsep,
        # 'sep' : aksiSep,
    })