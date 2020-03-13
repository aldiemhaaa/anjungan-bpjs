from django.shortcuts import render
from datetime import date
import requests,hmac,hashlib,base64,time, tempfile , json ,random

diag, hasil, nokar, msg, noRujukan, fas, ppkPelayanan, poliRujukan, pelayanan, kelasRawat, comment, kodeSpesialisRujukan, dpjp = " "*13
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
    if 'diagnosa' in request.POST:
        try:
            diagnosa = request.POST['diagnosa']
            url = 'https://new-api.bpjs-kesehatan.go.id:8080/new-vclaim-rest/Rujukan/RS/%s' % diagnosa 
            global diag, noRujukan, poliRujukan, pelayanan, kelasRawat, kodeSpesialisRujukan
            noRujukan = diagnosa
            diag = getApi(url)

            # listNumber = open('list_number.txt',"w+")
            # for i in range(100):
            #     pin = ''.join(random.choice('0123456789') for _ in range(6))
            #     listNumber.write(pin)
            # listNumber.close()

            
            # print(pin + " ini random numbernya")

            poliRujukan = diag['response']['rujukan']['provPerujuk']['kode']
            pelayanan = diag['response']['rujukan']['pelayanan']['kode']
            kelasRawat = diag['response']['rujukan']['peserta']['hakKelas']['kode']
            kodeSpesialisRujukan = diag['response']['rujukan']['poliRujukan']['kode']
        except:
            return "none"

    elif 'nomorKartu' in request.POST:
        global nokar
        nokartu = request.POST['nomorKartu']
        url = 'https://new-api.bpjs-kesehatan.go.id:8080/new-vclaim-rest/Rujukan/RS/Peserta/%s' % nokartu
        
        nokar = getApi(url)
        print(nokar)

    elif 'faskes' in request.POST:
        try:
            global comment, fas, ppkPelayanan
            comment = request.POST['catatan']
            faskes = request.POST['faskes']
            url = 'https://new-api.bpjs-kesehatan.go.id:8080/new-vclaim-rest/referensi/faskes/%s/2' % faskes 
            fas = getApi(url)
            ppkPelayanan = fas['response']['faskes'][0]['kode']
        except:
            return "none"


    elif 'dpjp' in request.POST:
        try:
            global dpjp
            url = 'https://new-api.bpjs-kesehatan.go.id:8080/new-vclaim-rest/referensi/dokter/pelayanan/'+ pelayanan + '/tglPelayanan/'+ dateNow + '/Spesialis/' + kodeSpesialisRujukan
            dpjp = getApi(url)
        except:
            return "none"

    elif request.POST:
        noKartu = diag['response']['rujukan']['peserta']['noKartu']
        noMR = diag['response']['rujukan']['peserta']['mr']['noMR']
        tglrujukan = diag['response']['rujukan']['tglKunjungan']
        diagAwal = diag['response']['rujukan']['diagnosa']['kode']
        poliTujuan = diag['response']['rujukan']['poliRujukan']['kode']
        noDpjp = dpjp['response']['list'][0]['kode']
        url = 'https://new-api.bpjs-kesehatan.go.id:8080/new-vclaim-rest/SEP/1.1/insert'
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
        global hasil
        hasil = postApi(url,dataKey)
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