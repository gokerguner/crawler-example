# README

Hepsiburada Crawler

## Paket Kurulumları
Linux Ubuntu v18.04 ortamında root kullanıcısıyla aşağıdaki adımlarla microk8s ve Docker kurulmaldır. 

**Komut Satırında: snap install microk8s --classic**

**Docker kurulumu için https://docs.docker.com/engine/install/ubuntu/ linkindeki adımlar takip edilebilir.**

## Docker ile Pullanması Gereken İmajlar
-- python:3.6.9

-- mongo:4.0.4

--------------------------------

**Komut Satırında Sırasıyla:** 

**microk8s.start**

**microk8s enable dns**

**microk8s enable registry**

--------------------------------

Komutları çalıştırılmalıdır. Bu komutlar, microk8s servisini başlattıktan sonra backend ve mongo podlarının haberleşmesi için dns eklentisinin ve backend imajının eklenmesi için registry eklentisinin aktive edilmesini sağlar.

## Backend İmajının Lokal Registry'e Eklenmesi

**Sırasıyla aşağıdaki adımlar uygulanır:**

Kaynak kodun açık olduğu ***dev ortamı*** imajı için: 

----------------------------------------------
**docker build -t backend-service:latest -f Dockerfile ./src**

----------------------------------------------

Bazen, kubernetes cluster'ımızı onprem ortamlarda ayağa kaldırmak, bundan dolayı da kaynak kodumuzu derleyerek gizlemek isteyebiliriz. Bunun için de aşağıdaki komutu çalıştırmamız gerekir:

----------------------------------------------
**docker build -t backend-service-prod:latest -f Dockerfile_prod ./src**

----------------------------------------------

Ardından, aşağıdaki komutla imajımızı tar'lamamız gerekir:

**docker image save -o image.tar backend-service:latest**

Eğer derlenmiş imaj kullanılacaksa bu kod uygun şekilde değiştirilmelidir. Sonrasında aşağıdaki komutla imaj, lokal registry'e eklenmelidir.

**microk8s.ctr image import image.tar**

# Yaml Dosyalarının Apply Edilmesi

Deployment klasörü altındaki yaml dosyaları haricindeki dosyalarla apply etmeye başlıyoruz. Klasör içindeki tüm dosyaları apply etmek için örnek olarak

**microk8s.kubectl apply -f service/**

Komutu kullanılabilir. Sırasıyla *service* klasörü yerine diğer klasörler yazılarak yaml dosyaları apply edilir.

### Yaml Notları

1) pv klasörü apply edilmeden önce MongoDB için /home/mongo klasörü oluşturulmalıdır.

2) Deployment klasörü altında önce mongo-deployment dosyası apply edilmelidir. Pod ayağa kalktıktan sonra önce poda, sonrasında da pod içerisinde mongo servisine bağlanılıp sırasıyla:

**use admin**

**db.createUser({user: "local-admin", pwd: "2023code", roles: [ {role:"readWriteAnyDatabase", db:"admin"},{role:"userAdminAnyDatabase",db:"admin"}, {role:"dbAdminAnyDatabase",db:"admin"}]})**

Komutları çalıştırılmalıdır. Böylelikle admin db'si altında backend servisimizin mongo'ya bağlanırken kullanacağı kullanıcıyı oluşturmuş oluruz.

Sonrasında deployment klasörü altındaki backend deployment dosyalarından uygun olanını (kodun açık veya derlenmiş halini kullanma isteğimize göre) apply ederek uygulamayı ayağa kaldırabiliriz.

Backend podu ayağa kalktıktan sonra yine mongo poduna bağlanıp:

**show dbs**

Komutuyla secret dosyası içinde bilgisini verdiğimiz *localdb* database'inin ve *params.json* dosyasında isimlendirdiğimiz collection'ların backend servisi tarafından oluşturulduğunu görebiliriz.

# Notlar

1) Mevcut pozisyonumda kullandığım yapıya yakın bir yapı olmasını, böylelikle bildiklerimi ve rutin çalışma düzenimin bir bölümünü göstermeyi hedefledim. Bundan dolayı *helm* chart kullanmadım.

2) Crawler yalnızca Türkiye'de yer alan bir serverda çalışır. Almanya'da yer alan bir serverda denediğimde request boş döndü, muhtemelen Türkiye dışı her lokasyonda boş gelecektir.

3) Hedefim, Kubernetes yeteneklerimi göstermekti. Dolayısıyla codebase çok düzgün, her corner case'i cover edecek şekilde çalışmıyor olabilir.

4) Burada kullandığım k8S komponentleri dışında Azure AKS, Openshift ortamları ve ingress, route komponentleri de kullandığım MLOps tech stack'inin bir bölümünü oluşturuyor.



