from aiogram import types


class Keyboard_reply:
    def __init__(self):
        self.buttons_for_start_teh_admin_keyboard = ['Добавить ТехAдмина', 'Добавить Aдмина+',
                                                     'Добавить Aдмина', 'Добавить Kонcультанта', 'Рассылка']
        self.buttons_for_start_admin_plus_keyboard = ['Добавить Aдмина', 'Добавить Kонcультанта', 'Рассылка']
        self.buttons_for_start_admin_keyboard = ['Добавить Kонcультанта', 'Рассылка']
        self.buttons_for_start_konsultant_keyboard = ['Добавить Карточку товара']
        self.buttons_for_start_skip_keyboard = ['Пропустить']
        self.buttons_for_start_katalog = ['Каталог']
        self.buttons_for_after_purchase_keyboard = ['Оставить отзыв', 'К началу']
        self.buttons_for_back_action = ['Назад']


    def reply_keyboard(self, block):
        reply_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

        if block == 'start_teh_admin_keyboard':
            reply_keyboard.add(*self.buttons_for_start_teh_admin_keyboard)
            return reply_keyboard
        elif block == 'start_admin_plus_keyboard':
            reply_keyboard.add(*self.buttons_for_start_admin_plus_keyboard)
            return reply_keyboard
        elif block == 'start_admin_keyboard':
            reply_keyboard.add(*self.buttons_for_start_admin_keyboard)
            return reply_keyboard
        elif block == 'start_konsultant_keyboard':
            reply_keyboard.add(*self.buttons_for_start_konsultant_keyboard)
            return reply_keyboard
        elif block == 'start_skip_keyboard':
            reply_keyboard.add(*self.buttons_for_start_skip_keyboard)
            return reply_keyboard
        elif block == 'start_katalog_keyboard':
            reply_keyboard.add(*self.buttons_for_start_katalog)
            return reply_keyboard
        elif block == 'after_purchase_keyboard':
            reply_keyboard.add(*self.buttons_for_after_purchase_keyboard)
            return reply_keyboard
        elif block == 'back_action':
            reply_keyboard.add(*self.buttons_for_back_action)
            return reply_keyboard
        elif block == '':
            reply_keyboard.add(*self.buttons_for_)
            return reply_keyboard
