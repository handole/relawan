# Relawan

*Test to try on master*

django fixtures untuk pemodelan id pada data awal agar menggenerate id custom dengan json
`https://docs.djangoproject.com/id/2.1/howto/initial-data/`

custom sesuai UI/UX agar menu terlihat rapih
Relawan -> Add Relawan
Target -> Add Target

### Fixtures initial data
- pertama siapkan folder fixtures di app yang terkait
- buat file initial_data.json atau apapun sesuai table di model
- untuk mengambil data dump di terminal > python manage.py dumpdata <nama_fixtures>.json
- untuk memberikan data ke database, bisa dibuat file json sesuai format modelnya
  dengan membuat ke terminal > python manage.py loaddata nama_fixtures.json
  

### Dashboard views
- summary relawan dengan jumlah realisasi target pemilih

### DAPIL 12
- fitur pencarian TPS dengan filter dapil dari kab -> kecamatan -> kelurahan -> jumlah tps
- fitur data calon pemilih dari target

- Relawan membawahi perwilayah 
- DAPIL perwilayah, kelurahan dipecah per RW dan per RT
- validasi duplikasi calon pemilih tiap wilayah. ada peringatan nik yang sdh diinput sdh punya relawan siapa.
- untuk penambahan target, langsung ke nama relawan
- relawan(korcam, kordes, kor tps) ada asisten,-> untuk struktural 
- dalam page relawan detail, terrdapat menu add target, area cakupan wilayah target
- penambahan tabel asisten yang terkait dengan relawan 
- perbedaan harga antara korcam dengan asisten(kordes, kor tps)
- 

- Detail relawan(Korcam) struktural/ non struktural(meliputi relawan umum bukan dari partai)
	- wilayah cakupanya
	- asisten 
		- wilayah asisten(kordes hingga kor RW RT)
	- masih dalam tabel relawan, terdapat pilihan tipe KORCAM, KORDES dan KOR RTRW

	
