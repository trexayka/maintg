import asyncio
import logging
import random
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

API_TOKEN = '9129606105:AAEC73332d5tYSeMWVdE4ioGwc7Qgiz6H88'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

user_games = dict()

class CurrencyStates(StatesGroup):
    waiting_for_amount = State()

NAMES_POOL = ["Артём", "София", "Максим", "Виктория", "Михаил", "Анастасия", "Иван", "Полина", "Даниил", "Екатерина", "Кирилл", "Алиса", "Егор", "Ксения", "Дмитрий", "Валерия", "Андрей", "Дарья", "Никита", "Арина", "Матвей", "Ульяна", "Роман", "Вероника", "Тимур", "Маргарита"]

CARS = {
    "Эконом": [("Lada Granta", 900000), ("Lada Vesta", 1400000), ("Hyundai Solaris", 1600000), ("Kia Rio", 1650000), ("VW Polo", 1700000), ("Skoda Rapid", 1750000), ("Renault Logan", 1100000), ("Chery Tiggo 4", 2000000), ("Haval Jolion", 2200000), ("Geely Coolray", 2400000), ("Ford Focus", 1500000), ("Nissan Almera", 1200000), ("Daewoo Nexia", 600000), ("Lada Niva", 1000000), ("Chevrolet Cobalt", 1300000)],
    "Комфорт": [("Toyota Camry", 3800000), ("Kia K5", 3500000), ("Hyundai Sonata", 3400000), ("Skoda Octavia", 2900000), ("VW Passat", 3600000), ("Mazda 6", 3300000), ("Honda Accord", 3700000), ("Toyota RAV4", 4200000), ("Kia Sportage", 3800000), ("Hyundai Tucson", 3700000), ("Nissan X-Trail", 3500000), ("Subaru Forester", 4000000), ("Geely Monjaro", 4300000), ("Exeed TXL", 4100000), ("Chery Tiggo 8", 3900000)],
    "Премиум": [("BMW 3", 5500000), ("BMW 5", 7800000), ("BMW X5", 11500000), ("Mercedes C", 5800000), ("Mercedes E", 8200000), ("Mercedes GLE", 12000000), ("Audi A4", 5400000), ("Audi A6", 7600000), ("Audi Q7", 11000000), ("Lexus ES", 6800000), ("Lexus RX", 9500000), ("Land Cruiser 300", 13500000), ("Volvo XC90", 9200000), ("Genesis G80", 7400000), ("Li Auto L9", 8500000)],
    "Люкс": [("Porsche 911", 18000000), ("Porsche Cayenne", 17500000), ("Porsche Taycan", 16000000), ("Mercedes-AMG GT", 21000000), ("Mercedes G63", 28000000), ("BMW M5", 16500000), ("Audi RS6", 17000000), ("Nissan GT-R", 15000000), ("Corvette C8", 14500000), ("Lamborghini Huracan", 35000000), ("Lamborghini Urus", 38000000), ("Ferrari Roma", 36000000), ("Aston Martin", 27000000), ("Bentley GT", 34000000), ("Rolls-Royce Cullinan", 55000000)]
}

BASE_REAL_ESTATE = [
    ("studio", "🏬 Студия", 7000000, 3),
    ("1k", "🛋 1-комнатная квартира", 11000000, 5),
    ("2k", "🔑 2-комнатная квартира", 16000000, 8),
    ("3k", "🏰 3-комнатная квартира", 24000000, 12),
    ("house", "🏡 Загородный дом", 35000000, 18)
]

EDU_DB = {
    "col_avia": ("Колледж: Авиатехник", "col", 3, 16, 20, 140000),
    "col_mech": ("Колледж: Автомеханик", "col", 3, 16, 0, 120000),
    "col_cook": ("Колледж: Повар-кондитер", "col", 3, 16, 0, 120000),
    "col_sys": ("Колледж: Сисадмин", "col", 3, 16, 25, 120000),
    "col_builder": ("Колледж: Промышленное ПГС", "col", 3, 16, 15, 130000),
    "col_electr": ("Колледж: Электрик-энергетик", "col", 3, 16, 15, 125000),
    "col_account": ("Колледж: Бухгалтерский учет", "col", 3, 16, 20, 135000),
    "col_design": ("Колледж: Графический дизайн", "col", 3, 16, 30, 150000),
    "col_law": ("Колледж: Юриспруденция", "col", 3, 16, 25, 140000),
    "uni_pilot": ("ВУЗ: Лётная эксплуатация", "uni", 4, 18, 65, 550000),
    "uni_it": ("ВУЗ: Программная инженерия", "uni", 4, 18, 55, 450000),
    "uni_med": ("ВУЗ: Лечебное дело", "uni", 4, 18, 60, 450000),
    "uni_fin": ("ВУЗ: Экономика и финансы", "uni", 4, 18, 50, 450000),
    "uni_arch": ("ВУЗ: Архитектура и урбанистика", "uni", 5, 18, 60, 500000),
    "uni_cyber": ("ВУЗ: Кибербезопасность", "uni", 4, 18, 65, 480000),
    "uni_market": ("ВУЗ: Интернет-маркетинг", "uni", 4, 18, 45, 400000),
    "uni_law": ("ВУЗ: Юриспруденция (Адвокатура)", "uni", 5, 18, 55, 460000),
    "uni_mgimo": ("ВУЗ: Международные отношения", "uni", 4, 18, 70, 600000),
    "uni_eng": ("ВУЗ: Авиакосмическое строениe", "uni", 5, 18, 65, 520000)
}

COURSES_DB = {
    "crs_barber": ("Курс: Барбер-стилист", 35000, 16),
    "crs_smm": ("Курс: Маркетинг и SMM", 45000, 16),
    "crs_design": ("Курс: UI/UX Веб-дизайн", 60000, 16),
    "crs_video": ("Курс: Монтаж видео и Reels", 40000, 16),
    "crs_trad": ("Курс: Криптотрейдинг и Финансы", 75000, 18)
}

JOBS_DB = [
    ("flyers", "📄 Раздача листовок", 80000, 14, None),
    ("cur", "📦 Курьер", 180000, 14, None),
    ("waiter", "🍽 Официант", 360000, 18, None),
    ("taxi", "🚕 Таксист", 500000, 18, None),
    ("barber", "✂️ Топ-барбер", 850000, 16, "Курс: Барбер-стилист"),
    ("mech", "🔧 Автомеханик", 950000, 18, "Колледж: Автомеханик"),
    ("chef", "👨‍🍳 Шеф-повар", 1100000, 18, "Колледж: Повар-кондитер"),
    ("smm", "📱 Маркетолог", 1150000, 16, "Курс: Маркетинг и SMM"),
    ("aviatech", "🛩 Авиатехник", 1250000, 18, "Колледж: Авиатехник"),
    ("sysadmin", "🖥 Сисадмин", 1300000, 18, "Колледж: Сисадмин"),
    ("designer", "🎨 UI/UX Дизайнер", 1450000, 16, "Курс: UI/UX Веб-дизайн"),
    ("builder", "🏗 Инженер-строитель", 1600000, 18, "Колледж: Промышленное ПГС"),
    ("electr", "⚡ Инженер-энергетик", 1550000, 18, "Колледж: Электрик-энергетик"),
    ("account", "📈 Главный бухгалтер", 1700000, 18, "Колледж: Бухгалтерский учет"),
    ("lawyer_col", "⚖️ Юрист (колледж)", 1650000, 18, "Колледж: Юриспруденция"),
    ("doctor", "🩺 Врач-хирург", 2400000, 21, "ВУЗ: Лечебное дело"),
    ("analyst", "📊 Финансовый аналитик", 2800000, 21, "ВУЗ: Экономика и финансы"),
    ("dev", "💻 Senior-разработчик", 3800000, 21, "ВУЗ: Программная инженерия"),
    ("arch", "🏛 Главный архитектор", 3200000, 23, "ВУЗ: Архитектура и урбанистика"),
    ("cyber", "🛡 Эксперт по кибербезопасности", 3600000, 21, "ВУЗ: Кибербезопасность"),
    ("advocate", "💼 Адвокат высшей категории", 3400000, 23, "ВУЗ: Юриспруденция (Адвокатура)"),
    ("diplomat", "🌐 Дипломат МИД", 4500000, 21, "ВУЗ: Международные отношения"),
    ("rocket", "🚀 Инженер-ракетостроитель", 4100000, 23, "ВУЗ: Авиакосмическое строениe"),
    ("pilot", "✈️ Пилот ГА", 4200000, 21, "ВУЗ: Лётная эксплуатация")
]

CITIES_STR = "Москва,Санкт-Петербург,Новосибирск,Екатеринбург,Казань,Нижний Новгород,Челябинск,Красноярск,Самара,Уфа,Ростов-на-Дону,Омск,Краснодар,Воронеж,Пермь,Волгоград,Саратов,Тюмень,Тольятти,Барнаул,Ижевск,Махачкала,Хабаровск,Ульяновск,Иркутск,Владивосток,Ярославль,Кемерово,Томск,Набережные Челны,Ставрополь,Оренбург,Новокузнецк,Рязань,Балашиха,Пенза,Чебоксары,Липецк,Калининград,Астрахань,Тула,Киров,Сочи,Курск,Улан-Удэ,Тверь,Магнитогорск,Сургут,Брянск,Иваново,Якутск,Владимир,Симферополь,Белгород,Нижний Тагил,Калуга,Чита,Грозный,Волжский,Смоленск,Подольск,Саранск,Вологда,Курган,Череповец,Орёл,Архангельск,Владикавказ,Нижневартовск,Йошкар-Ола,Стерлитамак,Мурманск,Кострома,Новороссийск,Тамбов,Химки,Мытищи,Нальчик,Таганрог,Нижнекамск,Благовещенск,Комсомольск-на-Амуре,Петрозаводск,Королёв,Шахты,Энгельс,Великий Новгород,Люберцы,Братск,Старый Оскол,Ангарск,Сыктывкар,Дзержинск,Псков,Орск,Красногорск,Армавир,Балаково,Бийск,Южно-Сахалинск,Уссурийск,Прокопьевск,Норильск,Рыбинск,Волгодонск,Сызрань,Петропавловск-Камчатский,Каменск-Уральский,Новочеркасск,Альметьевск,Златоуст,Северодвинск,Хасавюрт,Керчь,Домодедово,Салават,Миасс,Копейск,Пятигорск,Электросталь,Майкоп,Находка,Березники,Коломна,Щёлково,Серпухов,Ковров,Нефтекамск,Кисловодск,Батайск,Рубцовск,Обнинск,Кызыл,Дербент,Нефтеюганск,Назрань,Каспийск,Новочебоксарск,Новомосковск,Ессентуки"
ROOTS_STR = "Берёзовка,Сосновка,Дубровка,Малиновка,Ольховка,Ивановка,Михайловка,Николаевка,Александровка,Покровка,Никольское,Троицкое,Спасское,Рождествено,Архангельское,Богородское,Знаменское,Вознесенка,Успенка,Петровка,Васильевка,Сергеевка,Дмитровка,Павловка,Фёдоровка,Степановка,Григорьевка,Алексеевка,Андреевка,Семёновка,Кукуево,Простоквашино,Заречье,Подгорное,Нагорное,Озёрное,Лесное,Полевое,Луговое,Речное,Каменка,Песчанка,Глинка,Ключи,Родники,Отрадное,Светлое,Красное,Белое,Зелёный Бор,Калиновка,Рябиновка,Вишнёвка,Яблоновка,Грушевка,Черёмушки,Тополёвка,Клёново,Липовка,Ясенево"
RU_SETTLEMENTS = CITIES_STR.split(",") + [f"{t} {r}" for t in ("деревня", "село", "посёлок", "станица", "хутор", "слобода") for r in ROOTS_STR.split(",")]

DISEASES_DB = [
    {"id": "flu", "name": "🤧 Грипп или тяжелое ОРВИ", "min_age": 0, "chance": 0.06, "complication": "Перешло в острую пневмонию (-35 здоровья)"},
    {"id": "poison", "name": "🤢 Острое пищевое отравление", "min_age": 0, "chance": 0.03, "complication": "Сильное обезвоживание и гастрит (-25 здоровья)"},
    {"id": "gastritis", "name": "🩹 Обострение гастрита и язвы", "min_age": 14, "chance": 0.04, "complication": "Внутреннее кровотечение (-40 здоровья)"},
    {"id": "appendicitis", "name": "🔪 Острый аппендицит", "min_age": 7, "chance": 0.015, "complication": "Перитонит (смертельная угроза)"},
    {"id": "cardio", "name": "❤️ Гипертонический криз / Проблемы с сердцем", "min_age": 35, "chance": 0.03, "complication": "Микроинфаркт (-50 здоровья)"}
]

KIDS_EVENTS = [
    ("📖 Прочитал интересную книгу во дворе (+3 Ум, +2 Счастье)", 0, 0, 3, 2),
    ("🌳 Гулял с друзьями до вечера на площадке (+3 Счастье)", 0, 0, 0, 3),
    ("🚲 Покатался на велосипеде по лужам (+2 Здоровье, +3 Счастье)", 0, 2, 0, 3),
    ("🔑 Потерял ключи от квартиры, искал полдня (-2 Счастье)", 0, 0, 0, -2),
    ("🍏 Упал с дерева, содрал коленку (-4 Здоровье, -3 Счастье)", 0, -4, 0, -3),
]

def build_200_events():
    ev = list()
    for b in "по авиации,по психологии,по истории,по программированию,по экономике,по медицине,по физике,по философии,по бизнесу,по биографиям,по космосу,по инженерии,по праву,по искусству,по логике,по химии,по литературе,по географии,по математике,по астрономии".split(","):
        ev.append((f"📚 Прочитана книга {b} (+4 Ум, +3 Счастье)", 0, 0, 4, 3, 0))
    for ill in "легкая простуда,сезонная аллергия,ангина,пищевое отравление,сильная мигрень,грипп,боль в спине,растяжение связок,бессонница,усталость глаз,бронхит,насморк,солнечный удар,ушиб колена,переутомление,температура,зубная боль,ожог на кухне,сквозняк в транспорте,осенняя хандра".split(","):
        ev.append((f"🤒 Подхвачена {ill} (-6 Здоровье, -4 Счастье)", 0, -6, 0, -4, 0))
    for cg in "пятёрка в четверти,победа в олимпиаде,поход в зоопарк,поездка на море,похвала учителя,находка на улице,победа в школьном турнире,вкусный торт,новый конструктор,поход в кино,успешный проект,помощь родителям,победа в конкурсе рисунков,катание на коньках,лепка снеговика,поездка в лагерь,первое место в эстафете,поход в аквапарк,успешный экзамен,грамота за старание,весёлые каникулы,сборка модели самолёта,урок шахмат,посещение планетария,прогулка в парке,новый рюкзак".split(","):
        ev.append((f"🎈 Событие: {cg} (+2 000₽, +5 Счастье)", 2000, 0, 0, 5, 0))
    for ag in "подработка на выходных,помощь с переездом,продажа старых вещей,удачный фриланс,премия за работу,находка купюры,помощь соседу,выигрыш в лотерею,удачная сделка,подработка курьером,бонус от руководства,подарок от родных,сдача металла,перевод текста,настройка ПК,сборка мебели,доставка документов,помощь на мероприятии,фотосъёмка праздника,репетиторство,ремонт телефона,консультация,перепродажа гаджета,подработка на складе,бонус за переработку,приз в конкурсе,возврат долга,надбавка".split(","):
        ev.append((f"💰 Удача: {ag} (+14 000₽, +4 Счастье)", 14000, 0, 0, 4, 0))
    for ex in "потерян кошелёк,штраф за переход,сломался экран,порвалась куртка,потеряны наушники,поломка техники,ремонт дома,потерян зонт,ошибка перевода,порвалась обувь,разбита кружка,переплата за услуги,забыт пакет,поломка велосипеда,затраты на лекарства,порвался рюкзак,поцарапаны часы,неудачная покупка,комиссия банка,потеряны ключи".split(","):
        ev.append((f"💸 Неприятность: {ex} (-4 500₽, -4 Счастье)", -4500, 0, 0, -4, 0))
    for sp in "утренняя пробежка,спортзал,бассейн,велопрогулка,зарядка утром,прогулка в лесу,футбол с друзьями,йога,поход в баню,здоровый сон,отказ от фастфуда,витамины,лыжи,турник во дворе,прогулка 10 км,баскетбол,настольный теннис,растяжка,контрастный душ,горный воздух,тренировка,поход с палатками,прогулка у реки,активный отдых,свежий воздух,гимнастика,прогулка под дождём,массаж,визит к врачу,день без гаджетов".split(","):
        ev.append((f"💪 Здоровье: {sp} (+5 Здоровье, +4 Счастье)", 0, 5, 0, 4, 0))
    for cu in "театр,музей,концерт,классический фильм,встреча с другом,семейный ужин,настольные игры,иностранные слова,головоломки,лекция,экскурсия,новое блюдо,медитация,порядок дома,помощь животным,волонтёрство,рассказы,игра на гитаре,рисование,сложный пазл,планетарий,набережная,встреча рассвета,фотопрогулка,библиотека,документальное кино,история авиации,шахматы,кроссворды,душевный разговор".split(","):
        ev.append((f"🌟 Вдохновение: {cu} (+2 Ум, +6 Счастье)", 0, 0, 2, 6, 0))
    return ev

EVENTS_200 = build_200_events()

class Game:
    def __init__(self, rnd=False):
        self.age = 7.0
        self.alive = True
        self.health = 100
        self.mind = 20
        self.happy = 90
        self.money = 5000
        self.salary = 0
        self.job = "Нет"
        self.studying = None
        self.study_left = 0
        self.diplomas = list()
        self.cars = list()
        self.realty = list()
        self.partner = None
        self.kids = 0
        
        self.usd = 0
        self.usd_rate = 90.0
        self.usd_change = 0.0

        self.eur = 0
        self.eur_rate = 98.0
        self.eur_change = 0.0

        self.cny = 0
        self.cny_rate = 12.5
        self.cny_change = 0.0
        
        self.active_disease = None
        self.name = random.choice(["Александр Иванов", "Максим Смирнов", "Артем Кузнецов", "Дмитрий Волков", "Кирилл Соколов", "Иван Морозов"]) if rnd else "Тимофей Зайцев"
        self.city = random.choice(RU_SETTLEMENTS) if rnd else "Москва"
        
        self.update_region_coeff()
            
        self.school_grade = 1
        self.last_relation_age = 7.0
        self.last_kid_attempt_age = -1.0
        
        self.classmates = []
        sampled_names = random.sample(NAMES_POOL, 15)
        for name in sampled_names:
            self.classmates.append({
                "name": name, 
                "friend_val": 50, 
                "romance_val": 0, 
                "friend_status": "Друг", 
                "romance_status": "Нет", 
                "last_talk_age": -1.0, 
                "debt": 0
            })

    def update_region_coeff(self):
        if self.city == "Москва":
            self.region_coeff = 1.0
        elif self.city in ["Санкт-Петербург", "Сочи"]:
            self.region_coeff = 0.7
        elif self.city in ["Новосибирск", "Екатеринбург", "Казань", "Нижний Новгород", "Краснодар", "Владивосток"]:
            self.region_coeff = 0.45
        elif any(sett in self.city for sett in ["деревня", "село", "посёлок", "хутор", "станица"]):
            self.region_coeff = 0.15
        else:
            self.region_coeff = 0.3

    def update_currencies(self):
        old_usd = self.usd_rate
        ch_usd = random.uniform(-0.25, 0.35) if random.random() < 0.10 else random.uniform(-0.08, 0.08)
        self.usd_rate = max(55.0, min(250.0, round(self.usd_rate * (1 + ch_usd), 2)))
        self.usd_change = round(((self.usd_rate - old_usd) / old_usd) * 100, 1)

        old_eur = self.eur_rate
        ch_eur = random.uniform(-0.25, 0.35) if random.random() < 0.10 else random.uniform(-0.08, 0.08)
        self.eur_rate = max(60.0, min(270.0, round(self.eur_rate * (1 + ch_eur), 2)))
        self.eur_change = round(((self.eur_rate - old_eur) / old_eur) * 100, 1)

        old_cny = self.cny_rate
        ch_cny = random.uniform(-0.20, 0.30) if random.random() < 0.10 else random.uniform(-0.06, 0.06)
        self.cny_rate = max(8.0, min(40.0, round(self.cny_rate * (1 + ch_cny), 2)))
        self.cny_change = round(((self.cny_rate - old_cny) / old_cny) * 100, 1)

    def text(self):
        edu_str = ""
        if self.school_grade > 0:
            edu_str = f"Школа ({self.school_grade} класс)"
        elif self.studying:
            edu_str = f"{self.studying} (осталось {self.study_left} г.)"
        else:
            edu_str = ", ".join(self.diplomas) if self.diplomas else "Нет"
            
        disease_str = f"⚠️ <b>Болезнь: {self.active_disease['name']}</b>" if self.active_disease else "Здоров"
        
        usd_tr = f"+{self.usd_change}%" if self.usd_change >= 0 else f"{self.usd_change}%"
        eur_tr = f"+{self.eur_change}%" if self.eur_change >= 0 else f"{self.eur_change}%"
        cny_tr = f"+{self.cny_change}%" if self.cny_change >= 0 else f"{self.cny_change}%"
            
        return (
            f"👤 <b>{self.name}</b> | Возраст: <b>{self.age:.1f}</b>\n"
            f"📍 Место: {self.city} | Статус: {disease_str}\n"
            f"💰 Баланс: <b>{self.money:,} ₽</b>\n"
            f"💵 USD: <b>{self.usd}$</b> (Курс: {self.usd_rate}₽ | {usd_tr})\n"
            f"💶 EUR: <b>{self.eur}€</b> (Курс: {self.eur_rate}₽ | {eur_tr})\n"
            f"💴 CNY: <b>{self.cny}¥</b> (Курс: {self.cny_rate}₽ | {cny_tr})\n"
            f"🎓 Образование: {edu_str}\n"
            f"💼 Работа: {self.job} (+{self.salary:,}₽/год)\n"
            f"🏠 Недвижимость: {', '.join(self.realty) if self.realty else 'родительское жилье'}\n"
            f"🚘 Гараж: {', '.join(self.cars) if self.cars else 'пусто'}\n"
            f"❤️ Семья: {self.partner or 'Холост'} | Детей: {self.kids}\n"
            f"📊 Здоровье: {self.health}% | 🧠 Ум: {self.mind}% | 😊 Счастье: {self.happy}%"
        )

def main_kb(g: Game):
    if g.active_disease:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Лечиться дома (Шанс выздоровления: 20%)", callback_data="treat_home")],
            [InlineKeyboardButton(text="🏥 Гос. больница (Шанс выздоровления: 80%)", callback_data="treat_gov")],
            [InlineKeyboardButton(text="🩺 Частная клиника [50 000₽] (Шанс: 100%)", callback_data="treat_priv")]
        ])

    kb = [
        [InlineKeyboardButton(text="🏃 Прожить полгода", callback_data="year"), InlineKeyboardButton(text="🏥 Здоровье и Отдых", callback_data="heal")],
        [InlineKeyboardButton(text="🛒 Магазин", callback_data="open_shop"), InlineKeyboardButton(text="👥 Школа и Друзья", callback_data="school_menu")],
        [InlineKeyboardButton(text="💱 Обменник валют", callback_data="currency_menu")]
    ]

    if g.age >= 16 and g.school_grade == -1:
        kb.append([InlineKeyboardButton(text="🎓 Поступить в колледж", callback_data="edu"), InlineKeyboardButton(text="🎒 Остаться до 11 класса", callback_data="go_to_10")])
    else:
        kb.append([InlineKeyboardButton(text="🎓 Учеба и Курсы", callback_data="edu"), InlineKeyboardButton(text="💼 Вакансии", callback_data="work")])
        
    kb.extend([
        [InlineKeyboardButton(text="🏠 Недвижимость", callback_data="realty_menu"), InlineKeyboardButton(text="🗺 Переезд", callback_data="relocate_menu")],
        [InlineKeyboardButton(text="🚘 Автосалон", callback_data="cars"), InlineKeyboardButton(text="❤️ Семья", callback_data="fam")],
        [InlineKeyboardButton(text="🔄 Новая игра", callback_data="new")]
    ])
    return InlineKeyboardMarkup(inline_keyboard=kb)

@dp.message(Command("start"))
async def start(m: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Канон (Москва, Тимофей Зайцев)", callback_data="init_0")],
        [InlineKeyboardButton(text="🎲 Случайный город/деревня РФ", callback_data="init_1")]
    ])
    await m.answer("🎮 <b>One Life Out of Eight Billion</b>\nВыберите старт:", reply_markup=kb, parse_mode="HTML")

@dp.callback_query(F.data == "new")
async def new_g(c: CallbackQuery):
    await start(c.message)
    await c.answer()

@dp.callback_query(F.data.startswith("init_"))
async def init_g(c: CallbackQuery):
    _, mode = c.data.split("_")
    g = Game(rnd=(mode == "1"))
    user_games[c.from_user.id] = g
    await c.message.edit_text(g.text(), reply_markup=main_kb(g), parse_mode="HTML")
    await c.answer()

@dp.callback_query(F.data == "year")
async def next_y(c: CallbackQuery):
    g = user_games.setdefault(c.from_user.id, Game())
    if not g.alive:
        return await c.answer("Игра окончена! Нажмите Новая игра.", show_alert=True)
    
    if g.active_disease:
        return await c.answer("❌ Вы не можете двигаться дальше пока не вылечитесь от болезни!", show_alert=True)
    
    g.age += 0.5
    g.update_currencies()
    
    if g.school_grade > 0 and g.age.is_integer() and g.age <= 18:
        g.school_grade += 1

    g.money = max(0, g.money + int(g.salary / 2) - len(g.cars) * 20000)
    if g.age < 55 and g.health < 100:
        g.health = min(100, g.health + 3)

    if len(g.realty) > 0:
        g.happy = min(100, g.happy + len(g.realty) * 2)

    logs = list()
    
    available_diseases = [d for d in DISEASES_DB if g.age >= d["min_age"]]
    for dis in available_diseases:
        mod_chance = dis["chance"] * (1.5 if g.health < 50 else 1.0)
        if random.random() < mod_chance:
            g.active_disease = dis
            logs.append(f"⚠️ <b>Внимание! Вы подхватили болезнь: {dis['name']}! Срочно выберите лечение.</b>")
            break

    if not g.active_disease:
        if g.age < 14:
            relatives_options = [
                ("👵 Бабушка прислала гостинец и денег", 1500),
                ("👴 Дедушка поделился пенсией", 1500),
                ("👩 Тетя передала конверт с деньгами", 1000),
                ("👨 Дядя подкинул на карманные расходы", 1000)
            ]
            for rel_msg, rel_sum in relatives_options:
                if random.random() < 0.5:
                    g.money += rel_sum
                    logs.append(f"🎁 {rel_msg}: +{rel_sum} ₽!")

            if 8 <= g.age < 14 and random.random() < 0.5:
                g.money += 700
                logs.append("🍾 Сдал накопившиеся бутылки: +700 ₽!")

            ev_item = random.choice(KIDS_EVENTS)
            logs.append(ev_item[0])
            g.health = max(0, min(100, g.health + ev_item[1]))
            g.mind = max(0, min(100, g.mind + ev_item[2]))
            g.happy = max(0, min(100, g.happy + ev_item[3]))
        else:
            valid_events = [(t, m, h, mi, ha) for t, m, h, mi, ha, min_a in EVENTS_200 if g.age >= min_a] if any(len(item) == 6 for item in EVENTS_200) else [(t, m, h, mi, ha, 0) for t, m, h, mi, ha in EVENTS_200]
            ev_t, ev_m, ev_h, ev_mind, ev_hap, *_ = random.choice(valid_events)
            g.money = max(0, g.money + int(ev_m / 2))
            g.health = max(0, min(100, g.health + ev_h))
            g.mind = max(0, min(100, g.mind + ev_mind))
            g.happy = max(0, min(100, g.happy + ev_hap))
            logs.append(ev_t)

    if g.age - g.last_relation_age >= 1.0:
        g.last_relation_age = g.age
        decayed = []
        for mate in g.classmates:
            if mate["friend_val"] > 0:
                mate["friend_val"] = max(0, mate["friend_val"] - 15)
                if mate["friend_val"] <= 20 and mate["friend_status"] != "Бывший друг":
                    mate["friend_status"] = "Бывший друг"
                    decayed.append(mate["name"])
        if decayed:
            logs.append(f"⚠️ Из-за нехватки общения дружба с <b>{', '.join(decayed)}</b> ослабла (-15)!")

    if g.studying:
        g.study_left -= 0.5
        g.mind = min(100, g.mind + 3)
        if g.study_left <= 0:
            g.diplomas.append(g.studying)
            logs.append(f"🎓 Окончено: <b>{g.studying}</b>!")
            g.studying = None
        else:
            logs.append(f"📖 Учеба: {g.studying} (осталось {g.study_left} г.)")

    if g.age > 70:
        g.health = max(0, g.health - random.randint(2, 4))
    if g.health <= 0 or g.age >= 100:
        g.alive = False
        logs.append("🪦 Жизнь подошла к концу.")
        
    await c.message.edit_text("📅 Прошло полгода.\n" + "\n".join(logs) + "\n\n" + g.text(), reply_markup=main_kb(g), parse_mode="HTML")
    await c.answer()

@dp.callback_query(F.data.startswith("treat_"))
async def treat_disease(c: CallbackQuery):
    g = user_games.get(c.from_user.id)
    if not g or not g.active_disease: return
    
    action = c.data.split("_")[1]
    dis = g.active_disease
    
    success_chance = 0.20
    if action == "gov":
        success_chance = 0.80
    elif action == "priv":
        if g.money < 50000:
            return await c.answer("❌ У вас недостаточно денег для частной клиники (нужно 50 000 ₽)!", show_alert=True)
        g.money -= 50000
        success_chance = 1.00
        
    if random.random() < success_chance:
        g.active_disease = None
        await c.answer("🎉 Вы успешно вылечились!", show_alert=True)
    else:
        if random.random() < 0.25 and action != "priv":
            g.alive = False
            g.active_disease = None
            await c.message.edit_text(f"🪦 Болезнь ({dis['name']}) дала смертельное осложнение. Вы не справились.\n\n{g.text()}", parse_mode="HTML")
            return
        else:
            g.health = max(0, g.health - 30)
            log_msg = f"❌ Лечение не помогло! {dis['complication']}"
            g.active_disease = None
            await c.answer(log_msg, show_alert=True)
            
    await c.message.edit_text(g.text(), reply_markup=main_kb(g), parse_mode="HTML")

@dp.callback_query(F.data == "currency_menu")
async def currency_menu(c: CallbackQuery):
    g = user_games.get(c.from_user.id)
    if not g: return
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💵 Купить USD", callback_data="cur_buy_usd"), InlineKeyboardButton(text="💵 Продать USD", callback_data="cur_sell_usd")],
        [InlineKeyboardButton(text="💶 Купить EUR", callback_data="cur_buy_eur"), InlineKeyboardButton(text="💶 Продать EUR", callback_data="cur_sell_eur")],
        [InlineKeyboardButton(text="💴 Купить CNY", callback_data="cur_buy_cny"), InlineKeyboardButton(text="💴 Продать CNY", callback_data="cur_sell_cny")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
    ])
    await c.message.edit_text(
        f"💱 <b>Обменник валют</b>\n\n"
        f"Курсы на сегодня:\n"
        f"• USD: <b>{g.usd_rate} ₽</b> (У вас: {g.usd}$)\n"
        f"• EUR: <b>{g.eur_rate} ₽</b> (У вас: {g.eur}€)\n"
        f"• CNY: <b>{g.cny_rate} ₽</b> (У вас: {g.cny}¥)\n\n"
        f"Выберите операцию:",
        reply_markup=kb, parse_mode="HTML"
    )
    await c.answer()

@dp.callback_query(F.data.startswith("cur_"))
async def currency_action_start(c: CallbackQuery, state: FSMContext):
    parts = c.data.split("_")
    action, cur = parts[1], parts[2]
    await state.set_state(CurrencyStates.waiting_for_amount)
    await state.update_data(action=action, currency=cur)
    
    cur_names = {"usd": "Долларов (USD)", "eur": "Евро (EUR)", "cny": "Юаней (CNY)"}
    act_name = "купить" if action == "buy" else "продать"
    
    await c.message.edit_text(
        f"💱 Сколько <b>{cur_names[cur]}</b> вы хотите {act_name}?\n"
        f"Введите целое число в чат следующим сообщением:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 Отмена", callback_data="currency_menu")]]),
        parse_mode="HTML"
    )
    await c.answer()

@dp.message(CurrencyStates.waiting_for_amount)
async def process_currency_amount(m: Message, state: FSMContext):
    g = user_games.get(m.from_user.id)
    if not g:
        await state.clear()
        return
        
    try:
        amount = int(m.text.strip())
        if amount <= 0: raise ValueError()
    except ValueError:
        return await m.answer("❌ Пожалуйста, введите корректное положительное число!")

    data = await state.get_data()
    action = data["action"]
    cur = data["currency"]
    
    rates = {"usd": g.usd_rate, "eur": g.eur_rate, "cny": g.cny_rate}
    rate = rates[cur]
    total_cost = int(amount * rate)
    
    cur_symbols = {"usd": "$", "eur": "€", "cny": "¥"}
    sym = cur_symbols[cur]

    if action == "buy":
        if g.money < total_cost:
            await state.clear()
            return await m.answer(f"❌ Недостаточно средств! Нужно {total_cost:,} ₽, а у вас {g.money:,} ₽.", reply_markup=main_kb(g))
        
        g.money -= total_cost
        if cur == "usd": g.usd += amount
        elif cur == "eur": g.eur += amount
        elif cur == "cny": g.cny += amount
        
        await state.clear()
        await m.answer(f"✅ Успешно куплено {amount}{sym} за {total_cost:,} ₽!", reply_markup=main_kb(g))
        
    else:
        cur_balances = {"usd": g.usd, "eur": g.eur, "cny": g.cny}
        if cur_balances[cur] < amount:
            await state.clear()
            return await m.answer(f"❌ У вас нет столько валюты! Доступно: {cur_balances[cur]}{sym}.", reply_markup=main_kb(g))
            
        if cur == "usd": g.usd -= amount
        elif cur == "eur": g.eur -= amount
        elif cur == "cny": g.cny -= amount
        
        g.money += total_cost
        await state.clear()
        await m.answer(f"✅ Успешно продано {amount}{sym} за {total_cost:,} ₽!", reply_markup=main_kb(g))

@dp.callback_query(F.data == "relocate_menu")
async def relocate_menu_act(c: CallbackQuery):
    g = user_games.get(c.from_user.id)
    if not g: return
    destinations = ["Москва", "Санкт-Петербург", "Сочи", "Казань", "Екатеринбург", "Владивосток", "Краснодар", "деревня Берёзовка", "село Сосновка"]
    options = [d for d in destinations if d != g.city]
    random_options = random.sample(options, min(5, len(options)))
    random_options.append("🎲 Случайный уголок РФ")

    btns = []
    for dest in random_options:
        cost = 15000 if dest in ["Москва", "Санкт-Петербург", "Сочи", "Владивосток"] else 7000
        if "Случайный" in dest: cost = 10000
        btns.append([InlineKeyboardButton(text=f"✈️ В {dest} (Билет: {cost:,}₽)", callback_data=f"move_{dest}")])
        
    btns.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back")])
    await c.message.edit_text(f"🗺 <b>Переезд в другой город РФ</b>\nТекущее место: <b>{g.city}</b>\nВыберите направление:", reply_markup=InlineKeyboardMarkup(inline_keyboard=btns), parse_mode="HTML")
    await c.answer()

@dp.callback_query(F.data.startswith("move_"))
async def move_action(c: CallbackQuery):
    g = user_games.get(c.from_user.id)
    if not g: return
    dest = c.data[5:]
    cost = 15000 if dest in ["Москва", "Санкт-Петербург", "Сочи", "Владивосток"] else (10000 if "Случайный" in dest else 7000)
    
    if g.money < cost:
        return await c.answer(f"❌ Нужно {cost:,} ₽ на билеты и перевозку вещей!", show_alert=True)
        
    g.money -= cost
    if "Случайный" in dest:
        g.city = random.choice(RU_SETTLEMENTS)
    else:
        g.city = dest
        
    g.update_region_coeff()
    g.happy = min(100, g.happy + 10)
    
    await c.answer(f"🎉 Вы успешно переехали в город: {g.city}!", show_alert=True)
    await c.message.edit_text(g.text(), reply_markup=main_kb(g), parse_mode="HTML")

@dp.callback_query(F.data == "realty_menu")
async def realty_menu_act(c: CallbackQuery):
    g = user_games.get(c.from_user.id)
    if not g: return
    btns = []
    for r_id, title, base_p, hap_bonus in BASE_REAL_ESTATE:
        price = int(base_p * g.region_coeff)
        btns.append([InlineKeyboardButton(text=f"{title} — {price:,} ₽", callback_data=f"buyrealty_{r_id}")])
    btns.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back")])
    await c.message.edit_text(f"🏠 <b>Агентство недвижимости ({g.city}):</b>\nЦены адаптированы под твой регион!", reply_markup=InlineKeyboardMarkup(inline_keyboard=btns), parse_mode="HTML")
    await c.answer()

@dp.callback_query(F.data.startswith("buyrealty_"))
async def buy_realty_act(c: CallbackQuery):
    g = user_games.get(c.from_user.id)
    if not g: return
    r_id = c.data.split("_")[1]
    item = next((item for item in BASE_REAL_ESTATE if item[0] == r_id), None)
    if not item: return
    _, title, base_p, hap_bonus = item
    price = int(base_p * g.region_coeff)
    
    if g.money < price: return await c.answer(f"❌ Нужно {price:,} ₽!", show_alert=True)
    g.money -= price
    g.realty.append(title)
    g.happy = min(100, g.happy + hap_bonus)
    await c.answer(f"🎉 Вы успешно купили: {title}!", show_alert=True)
    await c.message.edit_text(g.text(), reply_markup=main_kb(g), parse_mode="HTML")

@dp.callback_query(F.data == "open_shop")
async def process_shop(c: CallbackQuery):
    g = user_games.get(c.from_user.id)
    if not g: return
    builder = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🍫 Шоколад (250₽) [+1 ум, +1 счастье]", callback_data="buy_chocolate")],
        [InlineKeyboardButton(text="🥤 Кока-кола (150₽) [+1 счастье]", callback_data="buy_cola")],
        [InlineKeyboardButton(text="⚡ Энергетик (300₽) [+5 ум, +1 счастье]", callback_data="buy_energy")],
        [InlineKeyboardButton(text="🥔 Чипсы (100₽) [+1 счастье]", callback_data="buy_chips")],
        [InlineKeyboardButton(text="🍏 Яблоко (200₽) [+1 счастье, +1 здоровье]", callback_data="buy_apple")],
        [InlineKeyboardButton(text="💊 Таблетки (1000₽) [+3 здоровье]", callback_data="buy_pills")],
        [InlineKeyboardButton(text="🍺 Пиво (500₽) [+2 счастье, -1 зд] (18+)", callback_data="buy_beer")],
        [InlineKeyboardButton(text="🍾 Водка (2000₽) [+4 счастье, -2 зд] (18+)", callback_data="buy_vodka")],
        [InlineKeyboardButton(text="🧠 Семакс (30000₽) [+15 ум]", callback_data="buy_semax")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
    ])
    await c.message.edit_text(f"🛒 <b>Магазин товаров</b>\n💰 Баланс: <b>{g.money:,} руб.</b>", reply_markup=builder, parse_mode="HTML")
    await c.answer()

@dp.callback_query(F.data.startswith("buy_"))
async def process_buy_item(c: CallbackQuery):
    g = user_games.get(c.from_user.id)
    if not g: return
    items = {
        "buy_chocolate": (250, 1, 1, 0, 0, "🍫 Съел шоколад! (+1 ум, +1 счастье)"),
        "buy_cola": (150, 0, 1, 0, 0, "🥤 Выпил кока-колу! (+1 счастье)"),
        "buy_energy": (300, 5, 1, 0, 0, "⚡ Выпил энергетик! (+5 ум, +1 счастье)"),
        "buy_chips": (100, 0, 1, 0, 0, "🥔 Похрустел чипсами! (+1 счастье)"),
        "buy_apple": (200, 0, 1, 1, 0, "🍏 Съел яблоко! (+1 счастье, +1 здоровье)"),
        "buy_pills": (1000, 0, 0, 3, 0, "💊 Принял таблетки! (+3 здоровье)"),
        "buy_beer": (500, 0, 2, -1, 18, "🍺 Выпил пива! (+2 счастье, -1 здоровье)"),
        "buy_vodka": (2000, 0, 4, -2, 18, "🍾 Выпил водки! (+4 счастье, -2 здоровье)"),
        "buy_semax": (30000, 15, 0, 0, 0, "🧠 Прокапал Семакс! (+15 ум)")
    }
    if c.data not in items: return
    price, d_int, d_hap, d_hp, min_age, msg = items[c.data]
    
    if g.age < min_age: return await c.answer(f"❌ Доступно только с {min_age} лет!", show_alert=True)
    if g.money < price: return await c.answer("❌ Недостаточно денег!", show_alert=True)
        
    g.money -= price
    g.mind = min(100, g.mind + d_int)
    g.happy = min(100, g.happy + d_hap)
    g.health = min(100, g.health + d_hp)
    await c.answer(msg, show_alert=True)
    await process_shop(c)

@dp.callback_query(F.data == "heal")
async def heal_m(c: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏃 Пробежка и сон (Бесплатно | +6% Здор)", callback_data="h_free")],
        [InlineKeyboardButton(text="🏥 Поликлиника (3 000₽ | +18% Здор)", callback_data="h_med")],
        [InlineKeyboardButton(text="🏨 Частная клиника (25 000₽ | +45% Здор)", callback_data="h_vip")],
        [InlineKeyboardButton(text="🌴 Санаторий и спа (60 000₽ | 100%)", callback_data="h_spa")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back")]
    ])
    await c.message.edit_text("🏥 <b>Восстановление здоровья и сил:</b>", reply_markup=kb, parse_mode="HTML")
    await c.answer()

@dp.callback_query(F.data.startswith("h_"))
async def heal_act(c: CallbackQuery):
    g = user_games.get(c.from_user.id)
    if not g: return
    _, act = c.data.split("_")
    if act == "free":
        g.health = min(100, g.health + 6)
        g.happy = min(100, g.happy + 5)
        await c.answer("💪 Вы отлично отдохнули!")
    elif act == "med":
        if g.money < 3000: return await c.answer("❌ Нужно 3 000 ₽!", show_alert=True)
        g.money -= 3000
        g.health = min(100, g.health + 18)
        await c.answer("💊 Лечение помогло (+18% Здоровье)!")
    elif act == "vip":
        if g.money < 25000: return await c.answer("❌ Нужно 25 000 ₽!", show_alert=True)
        g.money -= 25000
        g.health = min(100, g.health + 45)
        await c.answer("🩺 Частная клиника (+45% Здоровье)!")
    elif act == "spa":
        if g.money < 60000: return await c.answer("❌ Нужно 60 000 ₽!", show_alert=True)
        g.money -= 60000
        g.health = 100
        g.happy = 100
        await c.answer("🌴 Здоровье и счастье восстановлены на 100%!")
    await c.message.edit_text(g.text(), reply_markup=main_kb(g), parse_mode="HTML")

@dp.callback_query(F.data == "school_menu")
async def school_menu(c: CallbackQuery):
    g = user_games.get(c.from_user.id)
    if not g: return
    btns = []
    for idx, mate in enumerate(g.classmates):
        btns.append([InlineKeyboardButton(text=f"{mate['name']} (Дружба: {mate['friend_val']} | Романы: {mate['romance_val']})", callback_data=f"mate_{idx}")])
    btns.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back")])
    await c.message.edit_text("👥 <b>Школьные друзья и отношения:</b>\nВыберите человека:", reply_markup=InlineKeyboardMarkup(inline_keyboard=btns), parse_mode="HTML")
    await c.answer()

@dp.callback_query(F.data.startswith("mate_"))
async def mate_detail(c: CallbackQuery):
    g = user_games.get(c.from_user.id)
    if not g: return
    idx = int(c.data.split("_")[1])
    mate = g.classmates[idx]
    
    btns = [
        [InlineKeyboardButton(text="💬 Поговорить", callback_data=f"mact_talk_{idx}")],
        [InlineKeyboardButton(text="🌳 Погулять [+3 дружбы]", callback_data=f"mact_walk_{idx}")],
        [InlineKeyboardButton(text="💐 Цветы (4000₽) [+5 романов]", callback_data=f"mact_flowers_{idx}")],
        [InlineKeyboardButton(text="☕ Кафе (8500₽) [+10 романов]", callback_data=f"mact_cafe_{idx}")],
        [InlineKeyboardButton(text="📚 Учить уроки (+4 ум)", callback_data=f"mact_study_{idx}")],
        [InlineKeyboardButton(text="💵 Занять денег", callback_data=f"mact_borrow_{idx}")]
    ]
    if g.age >= 18.0:
        btns.append([InlineKeyboardButton(text="🍻 Пойти в бар", callback_data=f"mact_bar_{idx}")])
        btns.append([InlineKeyboardButton(text="🕺 Пойти в клуб", callback_data=f"mact_club_{idx}")])
        
    btns.append([InlineKeyboardButton(text="🔙 К списку друзей", callback_data="school_menu")])
    text_info = (
        f"👤 <b>{mate['name']}</b>\n"
        f"🤝 Дружба: {mate['friend_val']}/100 ({mate['friend_status']})\n"
        f"💖 Отношения: {mate['romance_val']}/100 ({mate['romance_status']})"
    )
    await c.message.edit_text(text_info, reply_markup=InlineKeyboardMarkup(inline_keyboard=btns), parse_mode="HTML")
    await c.answer()

@dp.callback_query(F.data.startswith("mact_"))
async def mate_action(c: CallbackQuery):
    g = user_games.get(c.from_user.id)
    if not g: return
    parts = c.data.split("_")
    action, idx = parts[1], int(parts[2])
    mate = g.classmates[idx]
    
    if action == "talk":
        if g.age - mate["last_talk_age"] < 0.5:
            return await c.answer("❌ Вы недавно уже общались! Попробуйте через полгода.", show_alert=True)
        mate["last_talk_age"] = g.age
        if random.random() < 0.5:
            mate["friend_val"] = min(100, mate["friend_val"] + 15)
            await c.answer("🎉 Разговор удался! (+15 дружбы)", show_alert=True)
        else:
            await c.answer("❌ Разговор не клеится.", show_alert=True)
    elif action == "walk":
        mate["friend_val"] = min(100, mate["friend_val"] + 3)
        await c.answer("🌳 Вы погуляли (+3 к дружбе)")
    elif action == "flowers":
        if g.money < 4000: return await c.answer("❌ Нужно 4 000 ₽!", show_alert=True)
        g.money -= 4000
        mate["romance_val"] = min(100, mate["romance_val"] + 5)
        if mate["romance_val"] > 50: mate["romance_status"] = "Пара"
        await c.answer("💐 Вы подарили цветы (+5 к романтике)")
    elif action == "cafe":
        if g.money < 8500: return await c.answer("❌ Нужно 8 500 ₽!", show_alert=True)
        g.money -= 8500
        mate["romance_val"] = min(100, mate["romance_val"] + 10)
        if mate["romance_val"] > 50: mate["romance_status"] = "Пара"
        await c.answer("☕ Вы сходили в кафе (+10 к романтике)")
    elif action == "study":
        g.mind = min(100, g.mind + 4)
        await c.answer("📚 Совместная учеба (+4 ум)")
    elif action == "borrow":
        limit = 2000 if g.age < 18 else 20000
        g.money += limit
        mate["debt"] += limit
        await c.answer(f"💵 Вы заняли {limit:,} ₽ у {mate['name']}!", show_alert=True)
    elif action == "bar" and g.age >= 18:
        g.happy = min(100, g.happy + 3)
        g.health = max(0, g.health - 1)
        await c.answer("🍻 Посидели в баре")
    elif action == "club" and g.age >= 18:
        g.happy = min(100, g.happy + 4)
        g.health = max(0, g.health - 2)
        await c.answer("🕺 Сходили в клуб")
    await mate_detail(c)

@dp.callback_query(F.data == "edu")
async def edu_m(c: CallbackQuery):
    g = user_games.setdefault(c.from_user.id, Game())
    has_col = any(d.startswith("Колледж:") for d in g.diplomas)
    has_uni = any(d.startswith("ВУЗ:") for d in g.diplomas)
    btns = [[InlineKeyboardButton(text="📖 Самообразование (+8% Ум)", callback_data="e_self")]]
    for k, (title, price, m_age) in COURSES_DB.items():
        btns.append([InlineKeyboardButton(text=f"⚡ {title} ({price:,}₽ | с {m_age}л)", callback_data=f"c_{k}")])
    for k, (title, kind, yrs, m_age, m_mind, paid_cost) in EDU_DB.items():
        is_paid = (kind == "col" and has_col) or (kind == "uni" and has_uni)
        cost_txt = f"{paid_cost:,}₽" if is_paid else "Бесплатно"
        btns.append([InlineKeyboardButton(text=f"🎓 {title} ({cost_txt})", callback_data=f"e_{k}")])
    btns.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back")])
    await c.message.edit_text("🎓 <b>Образование, колледжи, вузы и курсы:</b>", reply_markup=InlineKeyboardMarkup(inline_keyboard=btns), parse_mode="HTML")
    await c.answer()

@dp.callback_query(F.data == "e_self")
async def edu_self(c: CallbackQuery):
    g = user_games.get(c.from_user.id)
    if not g: return
    g.mind = min(100, g.mind + 8)
    g.happy = min(100, g.happy + 2)
    await c.answer("📖 Вы почитали книги (+8% Ум)!")
    await c.message.edit_text(g.text(), reply_markup=main_kb(g), parse_mode="HTML")

@dp.callback_query(F.data.startswith("c_"))
async def course_act(c: CallbackQuery):
    g = user_games.get(c.from_user.id)
    if not g: return
    c_key = c.data[2:]
    if c_key not in COURSES_DB: return
    title, price, m_age = COURSES_DB[c_key]
    if g.age < m_age: return await c.answer(f"❌ Нужен возраст от {m_age} лет!", show_alert=True)
    if title in g.diplomas: return await c.answer("❌ Вы уже прошли этот курс!", show_alert=True)
    if g.money < price: return await c.answer(f"❌ Нужно {price:,} ₽!", show_alert=True)
    g.money -= price
    g.diplomas.append(title)
    g.mind = min(100, g.mind + 12)
    await c.answer(f"⚡ Пройден курс: {title}!", show_alert=True)
    await c.message.edit_text(g.text(), reply_markup=main_kb(g), parse_mode="HTML")

@dp.callback_query(F.data.startswith("e_"))
async def edu_act(c: CallbackQuery):
    g = user_games.get(c.from_user.id)
    if not g: return
    e_key = c.data[2:]
    if e_key not in EDU_DB: return
    title, kind, yrs, m_age, m_mind, paid_cost = EDU_DB[e_key]
    if g.studying: return await c.answer("❌ Вы уже где-то учитесь!", show_alert=True)
    if g.age < m_age: return await c.answer(f"❌ Нужен возраст от {m_age} лет!", show_alert=True)
    if g.mind < m_mind: return await c.answer(f"❌ Нужно минимум {m_mind}% ума!", show_alert=True)
    
    has_col = any(d.startswith("Колледж:") for d in g.diplomas)
    has_uni = any(d.startswith("ВУЗ:") for d in g.diplomas)
    is_paid = (kind == "col" and has_col) or (kind == "uni" and has_uni)
    cost = paid_cost if is_paid else 0
    
    if g.money < cost: return await c.answer(f"❌ Нужно {cost:,} ₽!", show_alert=True)
    if cost > 0: g.money -= cost
    
    g.studying = title
    g.study_left = yrs
    g.school_grade = 0
    await c.answer(f"🎓 Поступили на: {title}!", show_alert=True)
    await c.message.edit_text(g.text(), reply_markup=main_kb(g), parse_mode="HTML")

@dp.callback_query(F.data == "go_to_10")
async def go_to_10_act(c: CallbackQuery):
    g = user_games.get(c.from_user.id)
    if not g: return
    g.school_grade = 10
    await c.answer("🎒 Вы остались до 11 класса!", show_alert=True)
    await c.message.edit_text(g.text(), reply_markup=main_kb(g), parse_mode="HTML")

@dp.callback_query(F.data == "work")
async def work_m(c: CallbackQuery):
    g = user_games.setdefault(c.from_user.id, Game())
    btns = []
    for j_id, title, sal, m_age, req_dip in JOBS_DB:
        req_txt = f" (Нужно: {req_dip})" if req_dip else ""
        btns.append([InlineKeyboardButton(text=f"{title} — {sal:,}₽/г (с {m_age}л){req_txt}", callback_data=f"w_{j_id}")])
    btns.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back")])
    await c.message.edit_text("💼 <b>Доступные вакансии:</b>", reply_markup=InlineKeyboardMarkup(inline_keyboard=btns), parse_mode="HTML")
    await c.answer()

@dp.callback_query(F.data.startswith("w_"))
async def work_act_real(c: CallbackQuery):
    g = user_games.get(c.from_user.id)
    if not g: return
    j_id = c.data[2:]
    job_item = next((item for item in JOBS_DB if item[0] == j_id), None)
    if not job_item: return
    _, title, sal, m_age, req_dip = job_item
    if g.age < m_age: return await c.answer(f"❌ Нужен возраст от {m_age} лет!", show_alert=True)
    if req_dip and req_dip not in g.diplomas: return await c.answer(f"❌ Требуется: {req_dip}", show_alert=True)
    g.job = title
    g.salary = sal
    await c.answer(f"💼 Новая работа: {title}!")
    await c.message.edit_text(g.text(), reply_markup=main_kb(g), parse_mode="HTML")

@dp.callback_query(F.data == "cars")
async def cars_m(c: CallbackQuery):
    btns = [[InlineKeyboardButton(text=f"🚘 Класс: {cat}", callback_data=f"carcat_{cat}")] for cat in CARS.keys()]
    btns.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back")])
    await c.message.edit_text("🚘 <b>Автосалон:</b>", reply_markup=InlineKeyboardMarkup(inline_keyboard=btns), parse_mode="HTML")
    await c.answer()

@dp.callback_query(F.data.startswith("carcat_"))
async def carcat_m(c: CallbackQuery):
    cat = c.data[7:]
    btns = list()
    for idx, (name, price) in enumerate(CARS[cat]):
        btns.append([InlineKeyboardButton(text=f"{name} — {price:,} ₽", callback_data=f"buycar_{cat}_{idx}")])
    btns.append([InlineKeyboardButton(text="🔙 Назад", callback_data="cars")])
    await c.message.edit_text(f"🚘 <b>Класс: {cat}</b>", reply_markup=InlineKeyboardMarkup(inline_keyboard=btns), parse_mode="HTML")
    await c.answer()

@dp.callback_query(F.data.startswith("buycar_"))
async def buycar_act(c: CallbackQuery):
    g = user_games.get(c.from_user.id)
    if not g: return
    parts = c.data.split("_")
    cat, idx = parts[1], int(parts[2])
    name, price = CARS[cat][idx]
    if g.money < price: return await c.answer(f"❌ Нужно {price:,} ₽!", show_alert=True)
    g.money -= price
    g.cars.append(name)
    await c.answer(f"🎉 Вы купили {name}!", show_alert=True)
    await c.message.edit_text(g.text(), reply_markup=main_kb(g), parse_mode="HTML")

@dp.callback_query(F.data == "fam")
async def fam_m(c: CallbackQuery):
    g = user_games.get(c.from_user.id)
    if not g: return
    btns = list()
    if not g.partner and g.age >= 18:
        btns.append([InlineKeyboardButton(text="💍 Свадьба (1 000 000₽)", callback_data="fam_partner")])
    if g.partner:
        btns.append([InlineKeyboardButton(text="🍼 Завести ребенка (раз в год)", callback_data="fam_kid")])
    btns.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back")])
    await c.message.edit_text("❤️ <b>Семья:</b>", reply_markup=InlineKeyboardMarkup(inline_keyboard=btns), parse_mode="HTML")
    await c.answer()

@dp.callback_query(F.data == "fam_partner")
async def fam_partner_act(c: CallbackQuery):
    g = user_games.get(c.from_user.id)
    if not g: return
    if g.money < 1000000: return await c.answer("❌ Нужно 1 000 000 ₽ на свадьбу!", show_alert=True)
    g.money -= 1000000
    g.partner = random.choice(["Алина Смирнова", "Екатерина Попова", "Анастасия Лебедева", "Виктория Козлова"])
    g.happy = min(100, g.happy + 25)
    await c.answer(f"💍 Вы сыграли свадьбу с {g.partner}!")
    await fam_m(c)

@dp.callback_query(F.data == "fam_kid")
async def fam_kid_act(c: CallbackQuery):
    g = user_games.get(c.from_user.id)
    if not g: return
    if g.age - g.last_kid_attempt_age < 1.0:
        return await c.answer("❌ Можно пытаться только 1 раз в год!", show_alert=True)
    g.last_kid_attempt_age = g.age
    if random.random() < 0.5:
        g.kids += 1
        g.happy = min(100, g.happy + 15)
        mat_cap = 630000 if g.kids == 1 else (200000 if g.kids == 2 else 450000)
        g.money += mat_cap
        await c.answer(f"🎉 Родился ребенок! Мат. капитал: +{mat_cap:,} ₽!", show_alert=True)
    else:
        await c.answer("❌ Попытка не принесла результата.", show_alert=True)
    await fam_m(c)

@dp.callback_query(F.data == "back")
async def back_act(c: CallbackQuery, state: FSMContext):
    await state.clear()
    g = user_games.get(c.from_user.id)
    if not g:
        g = Game()
        user_games[c.from_user.id] = g
    await c.message.edit_text(g.text(), reply_markup=main_kb(g), parse_mode="HTML")
    await c.answer()

async def main():
    print("🤖 Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())