TOKEN_API = '6033644605:AAFyQBw1Ul-lQF2gi0CFWps6vRuhUUYEBxk'
CHAT_ID = -886480543
VERSION = 'Build 1.0.050323'

def CONSOLE_LOG(log_type=1, message='Сообщение не указано'):
    if log_type == 1:
        log_type = 'NOTE'
    elif log_type == 2:
        log_type = 'WARN'
    elif log_type == 3:
        log_type = 'ERROR'
    print(f'{log_type}: {message}')