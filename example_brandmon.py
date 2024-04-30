from qoo10 import helper

locale = 'global'
datadir = 'qoo10_0'

driver = helper.Qoo10(datadir=datadir, locale=locale, browser='chrome')

driver.login()
result = driver.collect_brandmon()
print('Collected {} brandmons and {} mameqs'.format(result[0], result[1]))
driver.quit()