import qoo10

locale = qoo10.locales.qoo10_singapore
datadir = 'data'

collector = qoo10.Qoo10(datadir=datadir, locale=locale, browser='chrome', install=False)

collector.login(loginmethod=qoo10.loginmethods.login_kakaotalk)
result = collector.collect_mameq()
print('Collected {} mameqs'.format(result))

collector.quit()