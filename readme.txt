Celery-ni quyidagi ko‘rinishda ishga tushirish tavsiya etiladi:

celery -A movie worker -l info --pool=threads

Nima uchun threads?
threads rejimi minglab yoki millionlab email xabarlarni tezkor va samarali yuborish uchun juda mos keladi.

Celery standart holatda prefork (multi-processing) rejimidan foydalanadi.
Biroq, bu rejim joriy tasklar uchun ValueError xatoligiga olib kelishi mumkin.
Threads ishlatilganda, har bir task alohida jarayonda emas, balki yengil vaznli oqimlar (threads) orqali ishlaydi, bu esa resurslarni tejaydi va ishlash tezligini oshiradi.

Agar siz katta hajmli email jo‘natish operatsiyalarini bajarishni rejalashtirayotgan bo‘lsangiz, threads rejimi eng yaxshi tanlov bo‘ladi!