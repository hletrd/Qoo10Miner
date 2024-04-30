import qoo10
import time
import datetime
import random
import sys

username = '' #your qoo10 username (email)
password = '' #your qoo10 password

driver_global = qoo10.Qoo10(datadir='data', locale=qoo10.locales.qoo10_global, browser='chrome', install=False)
driver_global.login(qoo10.loginmethods.login_qoo10, username=username, password=password)

driver_global.set_locale(qoo10.locales.qoo10_singapore)
driver_global.login(qoo10.loginmethods.login_qoo10, username=username, password=password)

#always-on daemon

attend_day = -1

while True:
  sys.stderr.write("run\n")

  while datetime.datetime.now().hour < 9 or datetime.datetime.now().hour > 23:
    if datetime.datetime.now().hour >= 1 and attend_day != datetime.datetime.now().day:
      attend_day = datetime.datetime.now().day
      sys.stderr.write("Attending\n")
      driver_global.set_locale(qoo10.locales.qoo10_global)
      driver_global.attend()
      driver_global.collect_mameball()
      driver_global.set_locale(qoo10.locales.qoo10_singapore)
      result = driver_global.collect_mameq()
      if result > 0:
        print('Collected {} daily mameqs from singapore'.format(result))
      time.sleep(random.randint(5, 30))

    sys.stderr.write("Waiting for morning...\n")
    time.sleep(1800)

  driver_global.set_locale(qoo10.locales.qoo10_global)
  result = driver_global.collect_brandmon()
  if sum(result) > 0:
    print('Collected {} brandmons and {} mameqs from global'.format(result[0], result[1]))
  else:
    # no new brandmon found
    pass
  sys.stderr.write("Done\n")
  time.sleep(random.randint(5, 20))

  driver_global.set_locale(qoo10.locales.qoo10_singapore)
  result = driver_global.collect_brandmon()
  if sum(result) > 0:
    print('Collected {} brandmons and {} mameqs from singapore'.format(result[0], result[1]))
  else:
    # no new brandmon found
    pass
  
  time.sleep(random.randint(60, 240))
