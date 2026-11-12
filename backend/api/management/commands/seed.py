"""Fake, lekin real ko'rinishdagi ma'lumotlar: python manage.py seed [--clear]"""
import io, random
from datetime import timedelta
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils import timezone
from PIL import Image, ImageDraw
from api.models import *

CATS = [("ayollar", "Ayollar kiyimlari", "Женская одежда", "Women's clothing"),
        ("erkaklar", "Erkaklar kiyimlari", "Мужская одежда", "Men's clothing"),
        ("bolalar", "Bolalar kiyimlari", "Детская одежда", "Kids' clothing"),
        ("bosh", "Bosh kiyimlar", "Головные уборы", "Headwear"),
        ("poyabzal", "Poyabzal", "Обувь", "Footwear")]
# (kategoriya, uz, ru, en, narx, eski narx, rang)
PRODUCTS = [
 ("ayollar", "Oltin atlas ko'ylak", "Платье из золотого атласа", "Golden satin dress", 195, None, "#c9a24a"),
 ("ayollar", "Milliy shoyi ko'ylak", "Национальное платье из шёлка", "Traditional silk dress", 155, 180, "#3b6ea5"),
 ("ayollar", "Ikat ko'ylak 'Gulnoza'", "Платье икат «Гулноза»", "Ikat dress 'Gulnoza'", 210, None, "#a8324f"),
 ("ayollar", "Zardo'zi nimcha", "Жилет с золотым шитьём", "Gold-embroidered vest", 175, None, "#8a1c2b"),
 ("ayollar", "Bekasam adras ko'ylak", "Платье из бекасама", "Bekasam adras dress", 140, 160, "#6b3fa0"),
 ("ayollar", "Kelin libosi", "Свадебный наряд невесты", "Bridal outfit", 890, 990, "#e8d9b5"),
 ("erkaklar", "Milliy adras to'n", "Национальный халат из адраса", "Traditional adras robe", 120, None, "#d4a017"),
 ("erkaklar", "Zarbof chopon", "Чапан из парчи", "Brocade chapan", 260, None, "#2f4f2f"),
 ("erkaklar", "Oq milliy ko'ylak", "Белая национальная рубашка", "White national shirt", 85, None, "#d8d3c8"),
 ("erkaklar", "Belbog' (kamar)", "Пояс-белбог", "Belbog sash", 35, None, "#b5651d"),
 ("bolalar", "Qizlar uchun atlas ko'ylak", "Атласное платье для девочки", "Girls' satin dress", 95, 110, "#d9778f"),
 ("bolalar", "O'g'il bola chopon to'plami", "Комплект чапан для мальчика", "Boys' chapan set", 110, None, "#1f5f5b"),
 ("bolalar", "Bolalar do'ppisi", "Детская тюбетейка", "Kids' skullcap", 25, None, "#c0392b"),
 ("bosh", "Chust do'ppisi", "Чустская тюбетейка", "Chust skullcap", 45, None, "#1b1b1b"),
 ("bosh", "Marg'ilon do'ppisi", "Ферганская тюбетейка", "Fergana skullcap", 60, None, "#2e6f40"),
 ("bosh", "Ro'mol (zarbof)", "Платок из парчи", "Brocade scarf", 70, 85, "#9c5b99"),
 ("poyabzal", "Mahsi (charm poyabzal)", "Махси (кожаная обувь)", "Mahsi leather shoes", 130, None, "#5c3a21"),
 ("poyabzal", "Kavush", "Кавуш", "Kavush slippers", 75, None, "#3a2a1a")]
DESC = {"uz": "Qo'l mehnati bilan tikilgan, yuqori sifatli materiallardan. Hunarmandlarimiz an'anaviy naqshlarni zamonaviy bichim bilan uyg'unlashtirgan. O'lchamlar: S, M, L, XL. Buyurtma asosida individual tikish mumkin.",
        "ru": "Изготовлено вручную из качественных материалов. Мастера сочетают традиционные узоры с современным кроем. Размеры: S, M, L, XL. Возможен индивидуальный пошив.",
        "en": "Handmade from high-quality materials. Our artisans blend traditional patterns with a modern cut. Sizes: S, M, L, XL. Custom tailoring available on request."}
POSTS = [
 ("Zamonaviy O'zbek milliy modasi: an'ana va modernlik uyg'unligi", "Современная узбекская мода: гармония традиций и современности", "Modern Uzbek fashion: tradition meets modernity"),
 ("Adras — qadimiy san'at va zamonaviy moda", "Адрас — древнее искусство и современная мода", "Adras: an ancient craft in modern fashion"),
 ("O'zbek milliy naqshlari va ularning ma'nosi", "Узбекские национальные узоры и их значение", "Uzbek national patterns and their meaning"),
 ("Do'ppi tanlash bo'yicha maslahatlar", "Советы по выбору тюбетейки", "How to choose a doppi"),
 ("Kelin libosi: to'y uchun qanday tanlash kerak", "Свадебный наряд: как выбрать для торжества", "The bridal outfit: how to choose for your wedding")]
BODY = ("O'zbekiston hunarmandchiligi asrlar davomida shakllangan. Har bir naqsh, har bir chok o'z ma'nosiga ega.\n\n"
        "Margilon adrasi ipakdan to'qiladi va ikat usulida bo'yaladi. Bu jarayon bir necha bosqichdan iborat bo'lib, ustalardan katta mahorat talab qiladi.\n\n"
        "Bugungi kunda dizaynerlar milliy matolardan zamonaviy kundalik va tantanali kiyimlar yaratmoqda.")
NAMES = ["Dilnoza Karimova", "Aziz Yusupov", "Madina Rahimova", "Jasur Toshmatov", "Sevara Aliyeva", "Bobur Ergashev", "Nigora Sattorova",
         "Sardor Mirzayev", "Malika Qodirova", "Otabek Nazarov", "Zarina Abdullayeva", "Rustam Xolmatov"]
ADDR = ["Toshkent sh., Chilonzor tumani, 9-kvartal, 47-uy", "Toshkent sh., Yunusobod tumani, 4-mavze, 12-uy", "Samarqand sh., Registon ko'chasi, 23-uy",
        "Farg'ona sh., Mustaqillik ko'chasi, 8-uy", "Buxoro sh., Navoiy ko'chasi, 15-uy", "Andijon sh., Bobur shoh ko'chasi, 31-uy", "Namangan sh., Uychi ko'chasi, 5-uy"]
MSGS = ["Assalomu alaykum, kelin libosini buyurtma asosida tikib berasizlarmi? Muddati qancha?", "Mahsulotlar Samarqandga yetkazib berilarmikan?",
        "Ko'ylakning XL o'lchami bormi? Narxi qancha bo'ladi?", "Ulgurji narxda do'ppi olmoqchiman, 50 dona. Qanday shartlar bor?",
        "Buyurtmam 3 kundan beri kelmadi, tekshirib bera olasizlarmi?", "Sizlar bilan hamkorlik qilmoqchimiz, do'konimizga mahsulot yetkazib bera olasizlarmi?"]

def img(color, text, size=(600, 800)):
    im = Image.new("RGB", size, color); d = ImageDraw.Draw(im)
    for i in range(0, size[1], 40):  # yengil naqsh
        d.line([(0, i), (size[0], i + 120)], fill=tuple(min(255, c + 25) for c in im.getpixel((5, 5))), width=3)
    d.rectangle([30, 30, size[0] - 30, size[1] - 30], outline="white", width=3)
    d.text((size[0] // 2 - len(text) * 3, size[1] // 2), text, fill="white")
    b = io.BytesIO(); im.save(b, "JPEG", quality=85); return ContentFile(b.getvalue())

class Command(BaseCommand):
    help = "Barcha jadvallarga fake ma'lumot qo'shadi"
    def add_arguments(self, p): p.add_argument("--clear", action="store_true", help="Avval eski ma'lumotlarni o'chiradi")
    def handle(self, *a, **o):
        random.seed(7)
        if o["clear"]:
            for m in (OrderItem, Order, ProductImage, Product, Category, Post, ContactMessage): m.objects.all().delete()
        SiteSettings.objects.update_or_create(pk=1, defaults=dict(
            phone="+998 90 123 45 67", email="info@gulidesign.uz", work_hours="Dushanba - Shanba: 9:00 - 18:00",
            address_uz="Toshkent sh., Chilonzor tumani, Chilonzor-9, 47-uy", address_ru="г. Ташкент, Чиланзарский р-н, Чиланзар-9, д. 47",
            address_en="47 Chilonzor-9, Chilonzor district, Tashkent", instagram="https://instagram.com/gulidesign", telegram="https://t.me/gulidesign",
            hero_title_uz="Gul dizayn", hero_title_ru="Гули дизайн", hero_title_en="Guli Design",
            hero_sub_uz="O'zbek an'anaviy kiyimlari va hunarmandchilik san'ati", hero_sub_ru="Узбекская традиционная одежда и искусство ремесла",
            hero_sub_en="Uzbek traditional clothing and the art of craftsmanship", stat_products=500, stat_clients=1200, stat_masters=50))
        cats = {s: Category.objects.update_or_create(slug=s, defaults=dict(name_uz=u, name_ru=r, name_en=e))[0] for s, u, r, e in CATS}
        n = 0
        for i, (c, uz, ru, en, price, old, color) in enumerate(PRODUCTS):
            if Product.objects.filter(name_uz=uz).exists(): continue
            p = Product(category=cats[c], name_uz=uz, name_ru=ru, name_en=en, description_uz=DESC["uz"], description_ru=DESC["ru"], description_en=DESC["en"],
                        price=price, old_price=old, in_stock=random.random() > 0.12, is_featured=i % 3 == 0, badge="CHEGIRMA" if old else ("YANGI" if i % 5 == 1 else ""))
            p.image.save(f"p{i}.jpg", img(color, uz[:24]), save=False); p.save()
            for k in range(2): ProductImage(product=p).image.save(f"p{i}_{k}.jpg", img(color, f"{uz[:18]} #{k+2}"), save=True)
            Product.objects.filter(pk=p.pk).update(created=timezone.now() - timedelta(days=random.randint(0, 90))); n += 1
        for i, (uz, ru, en) in enumerate(POSTS):
            if Post.objects.filter(title_uz=uz).exists(): continue
            p = Post(title_uz=uz, title_ru=ru, title_en=en, body_uz=BODY, body_ru=BODY, body_en=BODY); p.cover.save(f"b{i}.jpg", img("#c9a96e", uz[:22], (900, 500)), save=True)
            Post.objects.filter(pk=p.pk).update(created=timezone.now() - timedelta(days=7 * i + 3))
        for i, nm in enumerate(NAMES):
            ContactMessage.objects.create(name=nm, email=f"{nm.split()[0].lower()}{i}@mail.uz", phone=f"+99890{random.randint(1000000, 9999999)}",
                                          message=random.choice(MSGS), is_read=i % 3 == 0)
        users = [User.objects.get_or_create(username=f"{nm.split()[0].lower()}@mail.uz", defaults=dict(email=f"{nm.split()[0].lower()}@mail.uz", first_name=nm.split()[0]))[0] for nm in NAMES[:6]]
        for u in users: u.set_password("test12345"); u.save()
        prods = list(Product.objects.filter(in_stock=True))
        for i in range(25):
            nm = random.choice(NAMES); o_ = Order.objects.create(user=random.choice(users + [None]), name=nm, phone=f"+99890{random.randint(1000000, 9999999)}",
                address=random.choice(ADDR), note=random.choice(["", "", "Soat 18:00 dan keyin yetkazing", "Qo'ng'iroq qilib keling"]),
                status=random.choice(["new", "processing", "shipped", "done", "done", "cancelled"])); t = 0
            for p in random.sample(prods, random.randint(1, 3)):
                q = random.randint(1, 2); OrderItem.objects.create(order=o_, product=p, qty=q, price=p.price); t += p.price * q
            Order.objects.filter(pk=o_.pk).update(total=t, created=timezone.now() - timedelta(days=random.randint(0, 60), hours=random.randint(0, 23)))
        self.stdout.write(self.style.SUCCESS(f"Tayyor: {n} mahsulot, {Post.objects.count()} blog, {ContactMessage.objects.count()} xabar, {Order.objects.count()} buyurtma"))
