import logging
import time


app_log = logging.getLogger('app')
app_log.setLevel(logging.INFO)


format = logging.Formatter('%(asctime)s\
    %(levelname)s %(module)s %(funcName)s %(message)s')

'''
    К имени файла лога дописывается текущая дата,
    что гарантирует создание нового файла
    каждый новый день.
'''

app_log_handler = logging.FileHandler('app_' + time.strftime('%d' '%m' '%y') + '.log')
app_log_handler.setFormatter(format)

app_log.addHandler(app_log_handler)


