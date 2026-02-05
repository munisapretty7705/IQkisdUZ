from aiogram.fsm.state import StatesGroup, State
# R.Mehriniso
# til va menu xududlari
class Form(StatesGroup):
    language = State()
    chose_menu = State()

    
    # Munisa Akbarovna 
    # ro'yxatdan utish buyicha 
    name=State()
    birth_date= State()
    viloyat=State()
    tuman=State()
    location_type = State()
    bogcha_type = State()     # Davlat / Xususiy
    bogcha_number = State()   # Bog‘cha raqami
    confirm = State() 

    # Marjona Sultonova
    # test state
    user_test = State()
