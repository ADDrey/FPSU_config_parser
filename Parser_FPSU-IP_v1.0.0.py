import os
import re
from io import StringIO
from datetime import datetime

# Путь к папке с конфигами
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIGS_PATH = EXEC_DIR + '\\CFG'
DATE = datetime.now()

# Приглашение в программу
WELCOMMING = """
---------------------------------- Парсер конфигураций ФПСУ-IP ----------------------------------
Был запущен скрипт парсера конфигурций ФПСУ-IP.
Данный скрипт имеет следующие функции:
    1. Получение состояния IPFIX-серверов (Да(настроен)/Нет (не настроен).
    2. Получение состояния МСЭ ФПСУ-IP (Да/Нет/Строка состояния не найдена в КФГ).
    3. Получение информации о первом правиле в МСЭ ФПСУ-IP (Название первого правила в МСЭ).
    4. Получение информации о количестве правил в МСЭ ФПСУ-IP (Количество правил в МСЭ ФПСУ-IP).
    5. Получение информации об адресах ФПСУ-IP на портах (Все IP адреса на 1 и 2 порту ФПСУ-IP).
    6. Получение информации об абонентах на LAN порту ФПСУ-IP (Сеть и маска/Хост).
    7. Получение информации об абонентах на WAN порту ФПСУ-IP (Сеть и маска/Хост).
    8. Выполнить функции 1-5.
    0. Прекратить работу скрипта.

Для запуска парсинга конфигурации необходимо:
    - В каталоге, где размещен даннный СКРИПТ, создать каталог с именем "CFG".
    - Положить в созданный каталог файлы конфигураций ФПСУ-IP для парсинга.
    
Если все готово, то введите номер функции (из списка выше), которую необходимо выполнить: """

class Config():

    def __init__(self, filename):
        """Инициализация переменных класса Config"""
        
        self.config = open(CONFIGS_PATH + '/' + filename).read()
        self.sn = filename[:-1].replace('.', '')
    
    
    def get_ipfix_status(self) -> str:
        """Получение информации о наличии данных об IPFIX серверах на ФПСУ-IP"""
        
        start_frase = 'IPFIX сервер'
        
        if self.config.find(start_frase) != -1:
            return 'Да (настроен)'
        else:
            return 'Нет (ненастроен)'

    
    def get_fw_status(self) -> str:
        """Получение информации о состоянии МСЭ ФПСУ-IP"""
        
        start_frase = 'Межсетевой экран активен:'
        
        if self.config.find(start_frase) != -1:
            status = self.config[self.config.find(start_frase) + len(start_frase) : ]
            status = status[ : status.find('\n')]
        else:
            status = 'Строка состояния МСЭ не найдена в КФГ'
        return status.strip()
    
    
    def get_fw_first_rule(self) -> str:
        """Получение информации о первом правиле в МСЭ ФПСУ-IP"""
        
        start_frase = self.config.find('Правила трафика')
        end_frase_1 = self.config.find('Интервалы времени', start_frase)
        end_frase_2 = self.config.find('Фильтрация трафика по содержимому', start_frase)
        
        if start_frase == -1 or (end_frase_1 == -1 and end_frase_2 == -1):
            return 'Правил трафика нет'
        elif end_frase_1 == -1:
            fw_rules = self.config[start_frase : end_frase_2]
        else:
            fw_rules = self.config[start_frase : end_frase_1]
            
        fw_rules_list = fw_rules.split('\n')
        
        return str(''.join(fw_rules_list[2]).strip())   # todo: Возможно надо будет указать другой индекс
    
    
    def get_fw_count_rules(self) -> str:
        """Получение информации о количестве правил в МСЭ ФПСУ-IP"""
        
        start_frase = self.config.find('Правила трафика')
        end_frase_1 = self.config.find('Интервалы времени', start_frase)
        end_frase_2 = self.config.find('Фильтрация трафика по содержимому', start_frase)
        
        if start_frase == -1 or (end_frase_1 == -1 and end_frase_2 == -1):
            return 'Правил трафика нет'
        elif end_frase_1 == -1:
            fw_rules = self.config[start_frase : end_frase_2]
        else:
            fw_rules = self.config[start_frase : end_frase_1]
            
        count = 0
        
        for rule in re.findall('\s\s\s\d{1,2}.', fw_rules):
            count += 1
            
        if str(count) not in '0':
            return str(count)
        else:
            return 'Правил трафика нет'
      
      
    def get_ip_from_port(self) -> str:
        """Получение информации об адресах ФПСУ-IP на портах"""
        
        port1 = self.config.find(' ПОРТ 1  ')
        port2 = self.config.find(' ПОРТ 2  ')
        
        ip_port_1 = self.config[port1 : min( self.config.find('ФПСУ-IP', port1) if self.config.find('ФПСУ-IP', port1) > -1 else len(self.config) - 1, 
                                                self.config.find('АБОНЕНТЫ', port1) if self.config.find('АБОНЕНТЫ', port1) > -1 else len(self.config) - 1, 
                                                self.config.find('МАРШРУТИЗАТОРЫ', port1) if self.config.find('МАРШРУТИЗАТОРЫ', port1) > -1 else len(self.config) - 1)]
        ip_port_2 = self.config[port2 : min( self.config.find('ФПСУ-IP', port2) if self.config.find('ФПСУ-IP', port2) > -1 else len(self.config) - 1, 
                                                self.config.find('АБОНЕНТЫ', port2) if self.config.find('АБОНЕНТЫ', port2) > -1 else len(self.config) - 1, 
                                                self.config.find('МАРШРУТИЗАТОРЫ', port2) if self.config.find('МАРШРУТИЗАТОРЫ', port2) > -1 else len(self.config) - 1)]
        
        return get_clear_ip_from_port(ip_port_1) + ';' + get_clear_ip_from_port(ip_port_2)
   
        
    def get_abonents_from_lan(self, sn: str) -> str:
        """Получение информации об абонентах на LAN порту ФПСУ-IP"""
        
        port1 = self.config.find(' ПОРТ 1  ')
        port2 = self.config.find(' ПОРТ 2  ')
        place_tunnels = self.config.find('  ФПСУ-IP')
        abonents_lan_port = ''
        
        if ((place_tunnels > port1 and place_tunnels < port2 and port1 < port2) 
            or (place_tunnels > port1 and place_tunnels > port2 and port1 > port2)):
            abonents_lan_port = self.config[self.config.find('АБОНЕНТЫ', port2) : port1 if port1 > port2 else len(self.config)]
        elif ((place_tunnels > port2 and place_tunnels < port1 and port2 < port1) 
              or (place_tunnels > port2 and place_tunnels > port1 and port2 > port1)):
            abonents_lan_port = self.config[self.config.find('АБОНЕНТЫ', port1) : port2 if port2 > port1 else len(self.config)]
        else:
            return 'LAN порт не обнаружен'
            
        str_abonents_lan_port = ''

        while abonents_lan_port.find('  Адрес', 8) > -1 :
            for addr in re.findall('(?:\d{1,3}.){3}\d{1,3}',abonents_lan_port[abonents_lan_port.find('  Адрес'): abonents_lan_port.find('\n')]):
                str_abonents_lan_port += ''.join(drop_lzeros(addr)).strip() + ';'
            str_abonents_lan_port += '\n' + str(sn) + ';'
            abonents_lan_port = abonents_lan_port[abonents_lan_port.find('  Адрес', 8): len(abonents_lan_port)]
            
        # удаление последнего переноса с серийным номером
        str_abonents_lan_port = str_abonents_lan_port[0 : abonents_lan_port.rfind(str(sn)) - len(sn) - 2]
        
        return str_abonents_lan_port
        
        
    def get_abonents_from_wan(self, sn: str) -> str:
        """Получение информации об абонентах на WAN порту ФПСУ-IP"""
        
        port1 = self.config.find(' ПОРТ 1  ')
        port2 = self.config.find(' ПОРТ 2  ')
        place_tunnels = self.config.find('  ФПСУ-IP')
        abonents_wan_port = ''
        
        if ((place_tunnels > port1 and place_tunnels < port2 and port1 < port2) 
            or (place_tunnels > port1 and place_tunnels > port2 and port1 > port2)):
            abonents_wan_port = self.config[self.config.find('АБОНЕНТЫ', port1) : port2 if port2 > port1 else len(self.config)]
        elif ((place_tunnels > port2 and place_tunnels < port1 and port2 < port1) 
              or (place_tunnels > port2 and place_tunnels > port1 and port2 > port1)):
            abonents_wan_port = self.config[self.config.find('АБОНЕНТЫ', port2) : port1 if port1 > port2 else len(self.config)]
        else:
            return 'WAN порт не обнаружен'
            
        str_abonents_wan_port = ''

        while abonents_wan_port.find('  Адрес', 8) > -1 :
            for addr in re.findall('(?:\d{1,3}.){3}\d{1,3}',abonents_wan_port[abonents_wan_port.find('  Адрес'): abonents_wan_port.find('\n')]):
                str_abonents_wan_port += ''.join(drop_lzeros(addr)).strip() + ';'
                
            str_abonents_wan_port += '\n' + str(sn) + ';'
            abonents_wan_port = abonents_wan_port[abonents_wan_port.find('  Адрес', 8): len(abonents_wan_port)]
            
        # удаление последнего переноса с серийным номером
        str_abonents_wan_port = str_abonents_wan_port[0 : abonents_wan_port.rfind(str(sn)) - len(sn) - 2]
        
        return str_abonents_wan_port
            
    function_name = {
        'get_ipfix_status' : get_ipfix_status,
        'get_fw_status' : get_fw_status,
        'get_fw_first_rule' : get_fw_first_rule,
        'get_fw_count_rules' : get_fw_count_rules,
        'get_ip_from_port' : get_ip_from_port,
        'get_abonents_from_lan' : get_abonents_from_lan,
        'get_abonents_from_wan' : get_abonents_from_wan
    }


def menu(option):
    try:
        total = len(os.listdir(CONFIGS_PATH))
    except FileNotFoundError:
        return'\nКаталог "CFG" с конфигурациями не обнаружен. Может его и нет?\n'

    match option:
        case '1':
            case_output(total, 'SN_FPSU;Status_IPFIX\n', 'get_ipfix_status')
            return ('\n\tИнформация по Статусу IPFix собрана в файл: ' 
                    + 'fpsu_pars_opt{}_{}-{}.csv'.format(option, DATE.day, DATE.month) + '\n')
        case '2':
            case_output(total, 'SN_FPSU;Status_FW\n', 'get_fw_status')
            return ( '\n\tИнформация по Статусу МСЭ собрана в файл: ' 
                    + 'fpsu_pars_opt{}_{}-{}.csv'.format(option, DATE.day, DATE.month) + '\n')
        case '3':
            case_output(total, 'SN_FPSU;FW_First_Rule\n', 'get_fw_first_rule')
            return ( '\n\tИнформация по первому правилу в МСЭ собрана в файл: ' 
                    + 'fpsu_pars_opt{}_{}-{}.csv'.format(option, DATE.day, DATE.month) + '\n')
        case '4':
            case_output(total, 'SN_FPSU;FW_Quantity_Rules\n', 'get_fw_count_rules')
            return ( '\n\tИнформация о количестве правил в МСЭ собрана в файл: ' 
                    + 'fpsu_pars_opt{}_{}-{}.csv'.format(option, DATE.day, DATE.month) + '\n')
        case '5':
            case_output(total, 'SN_FPSU;IP_Port_1;IP_Port_2\n', 'get_ip_from_port')
            return ( '\n\tИнформация об адресах на портах ФПСУ-IP собрана в файл: ' 
                    + 'fpsu_pars_opt{}_{}-{}.csv'.format(option, DATE.day, DATE.month) + '\n')    
        case '6':
            case_output(total, 'SN_FPSU;IP_abonent_LAN;MASK_abonent_LAN\n', 'get_abonents_from_lan', 'sn')
            return ( '\n\tИнформация об абонентах на LAN порту ФПСУ-IP собрана в файл: ' 
                    + 'fpsu_pars_opt{}_{}-{}.csv'.format(option, DATE.day, DATE.month) + '\n')      
        case '7':
            case_output(total, 'SN_FPSU;IP_abonent_WAN;MASK_abonent_WAN\n', 'get_abonents_from_wan', 'sn')
            return ( '\n\tИнформация об абонентах на WAN порту ФПСУ-IP собрана в файл: ' 
                    + 'fpsu_pars_opt{}_{}-{}.csv'.format(option, DATE.day, DATE.month) + '\n')                       
        case '8':
            w_file.write('SN_FPSU;Status_IPFIX;Status_FW;FW_First_Rule;FW_Quantity_Rules;IP_Port_1;IP_Port_2\n')
            for num, filename in enumerate(os.listdir(CONFIGS_PATH)):           
                if filename.endswith('.SBT') or filename.endswith('.OOT'):
                    config = Config(filename)
                    sn = config.sn
                    print(sn + ': ' + str(num + 1) + '/' + str(total))
                    w_file.write(   sn + ';' +
                                    config.get_ipfix_status() + ';' +
                                    config.get_fw_status() + ';' +
                                    config.get_fw_first_rule() + ';' +
                                    config.get_fw_count_rules() + ';' + 
                                    config.get_ip_from_port() + '\n')
            return ( '\n\tИнформация собрана в файл: ' 
                    + 'fpsu_pars_opt{}_{}-{}.csv'.format(option, DATE.day, DATE.month) + '\n')
        case _:
            return 'Такой функции нет в меню!!!'


def case_output(total: str, table_head: str, func_name, args = ''):
    """Функция обхода файлов по функции, соответствующей выбранному пунктом меню"""
    with open (EXEC_DIR + '\\fpsu_pars_opt{}_{}-{}.csv'.format(func_name, DATE.day, DATE.month), 'w') as w_file:
        w_file.write(table_head)
        
        for num, filename in enumerate(os.listdir(CONFIGS_PATH)):           
            if filename.endswith('.SBT') or filename.endswith('.OOT'):
                config = Config(filename)
                sn = config.sn
                
                print(sn + ': ' + str(num + 1) + '/' + str(total))
                if args == '':
                    w_file.write(   sn + ';' + config.function_name[func_name](config) + '\n')
                elif args in 'sn':
                    w_file.write(   sn + ';' + config.function_name[func_name](config, sn) + '\n')
    

def drop_lzeros(ip):
    """Функция удаления ведущих нулей в IP-адресах и масках сетей"""
    
    octets = [i.lstrip('0') for i in ip.split('.')]
    new_ip = ''
    
    for i in octets:
        if i == '':
            new_ip += '0.'
        else:
            new_ip += i + '.'
            
    return new_ip[:-1]


def get_clear_ip_from_port(ip_from_port: str) -> str:
    """Подается строка в которой адрес порта представлен ввиде (IP_адрес маска_сети). Отделяется IP от маски"""
    
    port_ip = ''
    
    for addr in re.findall('(?:\d{1,3}.){3}\d{1,3}', ip_from_port):
        if '255' not in str(addr)[0:3]:
            port_ip += ''.join(drop_lzeros(addr)).strip() + ', '
    port_ip = port_ip[0 : port_ip.rfind(', ')]
    
    return port_ip


def main():
    while True:
        try:
            options_list = '0 1 2 3 4 5 6 7 8'
            option = str(input(WELCOMMING)).strip()
            if option in options_list:
                if option not in '0': #при "0" или "" будет завершать работу скрипта.
                    menu(option)
                else:
                    print('\n\tСкрипт остановлен.\n\tПока!')
                    return
            else:
                print('Такой функции нет! Попробуйте еще раз.')
        except PermissionError:
            print('Ошибка доступа к файлу. Может он уже используется / открыт?')
            input('Нажмите Enter для повтора...')
        except KeyboardInterrupt:
            print('\n\tСкрипт остановлен.\n\tПока!')
            return
        except Exception as e:
            raise
            return
        else:
            input('Нажмите Enter для повтора...')

if __name__ == '__main__':
    main()
