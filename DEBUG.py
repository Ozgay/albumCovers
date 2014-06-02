from config import settings
import pprint

def p(info):
    if settings.c['debug']:
       print info 

def pd(info):
    if settings.c['debug']:
       pprint.pprint(info)
    
