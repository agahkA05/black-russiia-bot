# Основные настройки бота
BOT_TOKEN = "8172843951:AAFHMnhFITsIlnA9EwgpVenTHg47UO64bys"
ADMIN_USERNAME = "Aga_05"

# Настройки цен (без ограничений)
MIN_PRICE = 0.01
MAX_PRICE = 999999999.0
MIN_PRICE_RUB = 0.01
MAX_PRICE_RUB = 999999999.0

# Настройки базы данных
DATABASE_PATH = "black_russia_market.db"

# Настройки файлов
UPLOAD_PATH = "uploads/"
MAX_PHOTOS_PER_AD = 10

# Категории товаров для Black Russia
CATEGORIES = {
    'weapons': '🔫 Оружие и броня',
    'vehicles': '🚗 Транспорт',
    'houses': '🏠 Недвижимость',
    'drugs': '💊 Наркотики и химикаты',
    'money': '💰 Деньги и валюта',
    'resources': '🔧 Ресурсы и материалы',
    'accounts': '👤 Аккаунты',
    'services': '🛠️ Услуги'
}

# Подкатегории для каждой категории
SUBCATEGORIES = {
    'weapons': ['Пистолеты', 'Автоматы', 'Снайперские винтовки', 'Дробовики', 'Ножи', 'Бронежилеты', 'Патроны', 'Гранаты'],
    'vehicles': ['Автомобили', 'Мотоциклы', 'Вертолеты', 'Лодки', 'Велосипеды', 'Грузовики', 'Спортивные авто'],
    'houses': ['Квартиры', 'Дома', 'Офисы', 'Склады', 'Гаражи', 'Пентхаусы', 'Особняки'],
    'drugs': ['Марихуана', 'Кокаин', 'Героин', 'Амфетамин', 'Экстази', 'ЛСД', 'МДМА', 'Кетамин'],
    'money': ['Доллары', 'Евро', 'Рубли', 'Криптовалюта', 'Игровая валюта'],
    'resources': ['Дерево', 'Металл', 'Ткань', 'Пластик', 'Электроника', 'Химикаты', 'Сырье'],
    'accounts': ['Аккаунты с деньгами', 'Аккаунты с оружием', 'Аккаунты с недвижимостью', 'Новые аккаунты'],
    'services': ['Фарм денег', 'Фарм ресурсов', 'Защита', 'Транспорт', 'Доставка', 'Обучение']
}

# Валюты
CURRENCIES = ['USD', 'RUB', 'EUR']

# Состояния товаров
CONDITIONS = ['new', 'used', 'broken']
CONDITION_NAMES = {
    'new': 'Новый',
    'used': 'Б/у',
    'broken': 'Сломанный'
}

# Серверы Black Russia
SERVERS = [
    'RED', 'GREEN', 'BLUE', 'YELLOW', 'ORANGE', 'PURPLE', 'LIME', 'PINK', 'CHERRY', 'BLACK',
    'INDIGO', 'WHITE', 'MAGENTA', 'CRIMSON', 'GOLD', 'AZURE', 'PLATINUM', 'AQUA', 'GRAY', 'ICE',
    'CHILLI', 'CHOCO', 'MOSCOW', 'SPB', 'UFA', 'SOCHI', 'KAZAN', 'SAMARA', 'ROSTOV', 'ANAPA',
    'EKB', 'KRASNODAR', 'ARZAMAS', 'NOVOSIB', 'GROZNY', 'SARATOV', 'OMSK', 'IRKUTSK', 'VOLGOGRAD', 'VORONEZH',
    'BELGOROD', 'MAKHACHKALA', 'VLADIKAVKAZ', 'VLADIVOSTOK', 'KALININGRAD', 'CHELYABINSK', 'KRASNOYARSK', 'CHEBOKSARY', 'KHABAROVSK', 'PERM',
    'TULA', 'RYAZAN', 'MURMANSK', 'PENZA', 'KURSK', 'ARKHANGELSK', 'ORENBURG', 'KIROV', 'KEMEROVO', 'TYUMEN',
    'TOLYATTI', 'IVANOVO', 'STAVROPOL', 'SMOLENSK', 'PSKOV', 'BRYANSK', 'OREL', 'YAROSLAVL', 'BARNAUL', 'LIPETSK',
    'ULYANOVSK', 'YAKUTSK', 'TAMBOV', 'BRATSK', 'ASTRAKHAN', 'CHEREPOVETS', 'MAGADAN', 'PODOLSK', 'SURGUT', 'IZHEVSK',
    'TOMSK', 'TVER', 'VOLOGDA', 'TAGANROG', 'NOVGOROD', 'KALUGA', 'VLADIMIR', 'CHITA', 'KOSTROMA'
]

# Причины жалоб
COMPLAINT_REASONS = {
    'forbidden': '🚫 Запрещенный товар',
    'overpriced': '💰 Завышенная цена',
    'bad_photos': '📸 Некачественные фото',
    'fake_description': '📝 Ложное описание',
    'scam': '👤 Мошенничество',
    'spam': '📢 Спам',
    'fake_account': '👤 Фейковый аккаунт',
    'inappropriate': '🔞 Неподходящий контент'
}