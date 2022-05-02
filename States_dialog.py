from aiogram.dispatcher.filters.state import State, StatesGroup


class states(StatesGroup):
    spam = State()
    blacklist = State()
    whitelist = State()
    S_ENTER_ID_TEH_Admin = State()
    S_ENTER_ID_Admin_plus = State()
    S_ENTER_ID_Admin = State()
    S_ENTER_ID_Konsultant = State()
    S_PIZDIM_TELEPHONE = State()
    S_ENTER_ID_ADRESS = State()
    S_NAME = State()


class dialog:
    START_TEH_ADMIN = 'Добро пожаловать в высшую панель ТехАдмина\nВся клавиатура в твоем распоряжении'
    START_ADMIN_PLUS = 'Добро пожаловать в панель Админ+\nВся клавиатура в твоем распоряжении'
    START_ADMIN = 'Добро пожаловать в панель Админа\nВся клавиатура в твоем распоряжении'
    START_KONSULTANT = 'Добро пожаловать в панель Консультанта\nВся клавиатура в твоем распоряжении'
    START_FIRST_USER = 'Привет! Рад, что ты решил посмотреть, что есть у нас. Сейчас покажу все' \
                       '\nНо сначала, как я могу к тебе обращаться?'

    SUCCESSFUL_PAYMENT = 'Спасибо, что обратились именно к нам! Будем рады, если вы внесете свой вклад' \
                         ' в повышение качества обслуживания и оставите свой отзыв'

    HELP = 'Привет, рад, что тебя заинтересовала эта вкладка\n\nОсвновной разрабочик бота: @Andre1_Ts'

    SPAM_START = 'Напиши текст рассылки'
    SPAM_END = 'Рассылка завершена'

    NEW_TEH_ADMIN = "Введи ID и ФИО нового ТехAдмина в формате '123456' - 'Иванов Иван Иванович' "
    NEW_TEH_ADMIN_FINAL = 'Новый ТехАдмин добавлен'
    NEW_TEH_ADMIN_FINAL_TO = 'Поздравляю, ты новый ТехАдмин XD'

    NEW_ADMIN_PLUS = "Введи ID и ФИО нового Aдмина+ в формате '123456' - 'Иванов Иван Иванович' "
    NEW_ADMIN_PLUS_FINAL = 'Новый Админ+ добавлен'
    NEW_ADMIN_PLUS_FINAL_TO = 'Поздравляю, ты новый Админ+ XD'

    NEW_ADMIN = "Введи ID и ФИО нового Aдмина в формате '123456' - 'Иванов Иван Иванович' "
    NEW_ADMIN_FINAL = 'Новый Админ добавлен'
    NEW_ADMIN_FINAL_TO = 'Поздравляю, ты новый Админ XD'

    NEW_KONSULTANT = "Введи ID и ФИО нового Консультанта в формате '123456' - 'Иванов Иван Иванович' "
    NEW_KONSULTANT_FINAL = 'Новый Консультант добавлен'
    NEW_KONSULTANT_FINAL_TO = 'Поздравляю, ты новый ТехАдмин XD'

    TEXT_RANDOM = 'Не знаю, что на это ответить('
