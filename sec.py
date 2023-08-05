import requests
import hashlib
import os
import subprocess
import time
import random

swfdump_path = "path/to/swfdump"
lokal_as_dosya_yolu = "test.as"
internet_url = "URL_TO_REMOTE_CHECK_AS_FILE"
swf_exe_yolu = "path/to/Badmice.exe"

def dosya_md5_hash_hesapla(dosya_yolu):
    hasher = hashlib.md5()
    with open(dosya_yolu, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def internetten_dosya_indir(url, hedef_dosya_yolu):
    response = requests.get(url)
    if response.status_code == 200:
        with open(hedef_dosya_yolu, "wb") as f:
            f.write(response.content)

while True:
    bekleme_suresi = random.randint(300, 900) 
    print(f"Kontrol yapılıyor. {bekleme_suresi} saniye sonra bir sonraki kontrol yapılacak.")
    time.sleep(bekleme_suresi)
    subprocess.run([swfdump_path, "badmice.swf", "-a", "-o", lokal_as_dosya_yolu])
    onceki_lokal_hash = dosya_md5_hash_hesapla(lokal_as_dosya_yolu)
    internetten_dosya_indir(internet_url, "check.as")
    suanki_lokal_hash = dosya_md5_hash_hesapla(lokal_as_dosya_yolu)
    if suanki_lokal_hash != onceki_lokal_hash:
        print("Dosya değiştirilmiş. Bağlantı kesiliyor.")
        subprocess.run(["taskkill", "/f", "/im", "Badmice.exe"])
    os.remove(lokal_as_dosya_yolu)
    os.remove("check.as")





