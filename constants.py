import json
import os

CFG = os.path.join(os.path.dirname(__file__), 'cfg.dat')

def load_cfg():
    with open(CFG, 'r') as fp:
        cfg = json.load(fp)
    return cfg

def save_cfg(d):
    with open(CFG, 'w') as fp:
        json.dump(d, fp, indent=3)

if os.path.lexists(CFG):
    cfg = load_cfg()
    for k, v in cfg.items():
        locals()[k] = v
else:
    APP_ID = os.getenv('APP_ID', "123")
    APP_SECRET = os.getenv('APP_SECRET', "123")
    TOKEN = os.getenv('TOKEN', "123")
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '123')
    # 微信代理服务器地址
    WEIXIN_PROXY_SERVER_HOST = os.getenv('WEIXIN_PROXY_SERVER_HOST', 'http://localhost')
    WEIXIN_PROXY_SERVER_PORT = int(os.getenv('WEIXIN_PROXY_SERVER_PORT', '8004'))

    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_DB = os.getenv('MYSQL_DB')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    
    MYSQL_HOST_CENTER = os.getenv('MYSQL_HOST_CENTER')
    MYSQL_USER_CENTER = os.getenv('MYSQL_USER_CENTER')
    MYSQL_DB_CENTER = os.getenv('MYSQL_DB_CENTER')
    MYSQL_PASSWORD_CENTER = os.getenv('MYSQL_PASSWORD_CENTER')



WEIXIN_PROXY_SERVER_ADDR = f'{WEIXIN_PROXY_SERVER_HOST}:{WEIXIN_PROXY_SERVER_PORT}'

KF_ACCOUNTS_EXPIRED_TIME = 3600  # 客服信息缓存时间(单位:秒)


