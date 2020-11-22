from getpass import getpass


def get_code():
    while True:
        code = input('国家或地区码[可选，用于国外手机]: ')
        if code == '':
            break
        try:
            code = int(code)
        except ValueError:
            print('国家或地区码不正确。')
        else:
            break
    return code


def login(api, *args):
    while True:
        user = input('邮箱或手机号: ')
        try:
            int(user)
        except ValueError:
            if '@' in user:
                password = getpass('密码: ')
                r = api.login(user, password)
            else:
                print('格式不正确。')
                continue
        else:
            code = get_code()
            password = getpass('密码: ')
            if code != '':
                r = api.login_cellphone(user, password, code)
            else:
                r = api.login_cellphone(user, password)
        if r.status_code == 200:
            print('登录成功。')
            break
        else:
            print('登录失败，请重试。')


def logout(api, *args):
    api.logout()


notcloudmusic_plugin_info = {
    'name': 'basics',
    'version': '0.1.0',
    'author': 'NKID00',
    'link': 'https://github.com/NKID00/NotCloudMusic',
    'description': '各种基础命令',
    'commands': {
        'login': {
            'description': '使用邮箱或手机号进行交互式登录',
            'callable': login,
        },
        'logout': {
            'description': '退出登录',
            'callable': logout,
        },
    }
}
