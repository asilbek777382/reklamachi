from aiogram.dispatcher.filters.state import State,StatesGroup

class kirish(StatesGroup):
    login=State()
    parol=State()



class sett(StatesGroup):
    shaxsiyda=State()
    shuyerda=State()


class tastiq(StatesGroup):
    tastiq=State()

class xabar_sozlash_state(StatesGroup):
    boshi=State()
    xabar_sozlash=State()
    takrorlash=State()
    tugash_sanasi=State()
    xabarni_qadash=State()
    songgi_xabarni_ochirish=State()




class xabar_set_bol(StatesGroup):
    xabar_set_bol=State()


class xabar_set_bol(StatesGroup):
    xabar_set_bol=State()


class xabarn_sozlash(StatesGroup):
    xabarn_sozlash=State()
    matn=State()
    media=State()
    url_tugma=State()
class kanal(StatesGroup):
    kanal=State()
