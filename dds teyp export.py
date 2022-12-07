#coding:utf-8
import os.path,sys,re

file=open('/media/DEPO/tape2/tape1offset.txt','rb')

def DosyaKlasorOlustur(kokdizin,klasor,st_size,st_nlink,tamyol,ilk_pos):
#buraya tape2.dd dosyasından boh konumuna göre st_size,st_nlink ve diğer parametreler parseedilecek. burayı fonksiyon olarak yaz ve
#aşağıdaki koşullara fonksiyon parametresi olarak geçir.
 
 try:
  if len(kokdizin)==1:
   if not os.path.exists(tamyol):
    os.mkdir(tamyol)
 except OSError:
  pass  

 try:
  if kokdizin.find(':')==-1:
#aşağıyı fonksiyon olarak tanımlanabilir. aşağıdaki koşullar dosya,klasor oluşturmaya yarayacak...lnk dosyalarını ignore eidoyruz. 
   if st_size==0 and st_nlink==1:
    if not os.path.exists(klasor):
     os.mkdir(klasor)
     f=open(tamyol,'w').close()
     print 'size=0 dosya konum............:',ilk_pos
     print 'size=0 klasor adı............:',tamyol
     print 'size=0 tamyol............:',tamyol    
    else:
     f=open(tamyol,'w').close() 
     print 'size=0 dosya konum............:',ilk_pos
     print 'size=0 tamyol............:',tamyol

   elif (st_size > 0 and st_nlink==1):
    if not os.path.exists(klasor):
     os.mkdir(klasor)
     print 'size=0 dosya konum............:',ilk_pos
     print 'size>0 st_nlink=1 tamyol............:',klasor
    else:
     tamyol=tamyol.replace('\x08\x08\x08\x08\x08\x08\x08\x03','recovered_'+str(ilk_pos))
     tamyol=tamyol.replace('?','questionmark_')
     tamyol=tamyol.replace('*','star')
     tamyol=tamyol.replace('\x01%','yuzde_isareti')
     tamyol=tamyol.replace('\x01\x93','recovered_'+str(ilk_pos))
     tamyol=tamyol.replace('\x02"','cift_tirnak_isareti')
     f=open(tamyol,'wb')
     fo.seek(int(ilk_pos)+1024)
     data=fo.read(int(st_size)).strip('\x00')
     f.write(data)
     f.close()
     print 'konum............:',ilk_pos
     print 'dosya adı............:',tamyol
     
   if (st_size >0 and st_nlink>1):
    if not os.path.exists(tamyol):
     os.mkdir(tamyol)
    else:
     print 'konum............:',ilk_pos
     print 'klasor..:',tamyol
 #print ': varrrrrrrrrrrrrrrrrrrrrrrr'
 except OSError:
  pass

for satir in file.readlines():
 #ilk boh konumu
	#ilk_pos=448574
	ilk_pos=int(satir)
       	fo=open("tape1.dd","r")
	#ilk boh konumuna git
	fo.seek(ilk_pos)
        katar=''
	#1024 byte katar degiskenine oku
	katar=fo.read(1024)
	print ilk_pos
        print 'katar boyutu..............:',len(katar)
        fo.seek(ilk_pos)
	#parametreler--BOH içindeki konum bilgileri
	kokdizin_pos=katar.find('/')
	st_size_pos=katar.find('st_size:')
	st_ino_pos=katar.find('st_ino:')
	st_nlink_pos=katar.find('st_nlink:')
        st_atime_pos=katar.find('st_atime:')
        
        #kokdizin adı
	kacbayt=st_size_pos-kokdizin_pos
	fo.seek(ilk_pos+kokdizin_pos)
	kokdizin=fo.read(kacbayt)
	kokdizin=kokdizin.strip('\x00')
        #st_size boyut
	kacbayt=st_ino_pos-st_size_pos-8
	fo.seek(ilk_pos+st_size_pos+8)
	st_size=fo.read(kacbayt)
	st_size=st_size.strip('\x00')
	int_st_size=int(st_size)
	      
        #link_to kontrol...link dosyalarını ihmal ediyorum..yoksa hata veriyor
        
        if katar.find('link_to:')==-1:
         kacbayt=st_atime_pos-st_nlink_pos-9
         fo.seek(ilk_pos+st_nlink_pos+9)
         st_nlink=fo.read(kacbayt)
         st_nlink=st_nlink.strip('\x00')
	 int_st_nlink=int(st_nlink)
        #aşağıda klasor bilgileri yer alıyor
	ana='/media/DEPO/teyp1'
	tamyol=ana+kokdizin
	(klasor,dosya)=os.path.split(tamyol)
	(dosyaad,uzanti)=os.path.splitext(tamyol)
         
        DosyaKlasorOlustur(kokdizin,klasor,int_st_size,int_st_nlink,tamyol,ilk_pos)

file.close()       



