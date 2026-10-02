from json import load, dump
import os



# Текущая версия бомбера
VERSION = '1.07'

# Стандартный цвет программы
MY_COLOR = 'deeppurpleaccent100'

# Название конфига
CONFIG_NAME = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')



def check_config():
    '''Просмотр конфига'''

    while True:
        try:
            with open(CONFIG_NAME) as f:
                return load(f)
        except:
            with open(CONFIG_NAME, 'w') as f:
                f.write('{"theme": "dark", "feedback": "True", "type_attack": "MIX", "attack": "False", "key": "", "color": "deeppurpleaccent100"}')



def change_config(key, value):
    '''Редактирование конфига'''

    config = check_config()
    config[key] = f'{value}'
    with open(CONFIG_NAME, 'w') as f:
        dump(config, f)


