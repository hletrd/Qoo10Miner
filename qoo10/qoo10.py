from xml.dom.minidom import Element
from selenium import webdriver

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains

import time
import os
import sys
import random
import json
import datetime

try:
  from webdriver_manager.chrome import ChromeDriverManager
  from webdriver_manager.firefox import GeckoDriverManager
except:
  sys.stderr.write("webdriver-manager not installed. Automatic installation not supported.\n")

timeout = 10
timeout_mameq = 10

#login

from . import locales
from . import loginmethods

class Qoo10:
  def __init__(self, datadir: str, locale: str, executable_path: str=None, install:bool =False, browser: str='chrome', load_saved: bool=True, headless: bool=False, logging: bool=True) -> None:
    if not os.path.exists(datadir):
      os.mkdir(datadir)
    self.browser = browser
    if browser == 'firefox':
      self.opts = FirefoxOptions()
      self.opts.add_argument("-profile")
      if headless == True:
        self.opts.add_argument("--headless")
      self.opts.add_argument(os.path.join(os.getcwd(), datadir))
      self.opts.set_preference("intl.accept_languages", "ko-KR")
      self.opts.set_preference("general.useragent.override", "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1")
    elif browser == 'chrome':
      self.opts = ChromeOptions()
      if headless == True:
        self.opts.add_argument("--headless")
      #self.opts.add_experimental_option('mobileEmulation', {'deviceMetrics': {'width': 390, 'height': 644, 'pixelRatio': 3.0}}) 
      self.opts.add_experimental_option('prefs', {'intl.accept_languages': 'ko,ko_KR'})
      self.opts.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_0_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1")
      self.opts.add_argument("user-data-dir={}".format(datadir))
    
    self.executable_path = executable_path
    self.datadir = datadir
    if load_saved == True:
      self.load_collected_disk()
    else:
      self.collected_brandmon = {}

    url = locale
    if browser == 'firefox':
      if install == True:
        service = FirefoxService(executable_path=GeckoDriverManager().install())
      elif self.executable_path != None:
        service = FirefoxService(executable_path=self.executable_path)
      else:
        service = None
      self.driver = webdriver.Firefox(service=service, options=self.opts)
    elif browser == 'chrome':
      if install == True:
        service = ChromeService(executable_path=ChromeDriverManager().install())
      elif self.executable_path != None:
        service = ChromeService(executable_path=self.executable_path)
      else:
        service = None
      self.driver = webdriver.Chrome(service=service, options=self.opts)
    self.driver.set_window_size(390, 780)
    #self.driver.set_window_size(500, 1000)
    self.driver.get("https://" + url)
    try:
      mobileweb = self.driver.find_element(By.ID, "btn_download_app_close")
      mobileweb.click()
    except:
      pass
    self.locale = locale
    self.logging = logging

  def save_collected(self, mon_type: str, collected: list[str]) -> None:
    if self.locale not in self.collected_brandmon:
      self.collected_brandmon[self.locale] = {}
    self.collected_brandmon[self.locale][mon_type] = collected
  
  def load_collected(self, mon_type: str) -> list[str]:
    if self.locale in self.collected_brandmon and mon_type in self.collected_brandmon[self.locale]:
      return self.collected_brandmon[self.locale][mon_type]
    else:
      return []

  def save_collected_disk(self) -> None:
    with open (os.path.join(self.datadir, 'collected.json'), 'w') as f:
      f.write(json.dumps(self.collected_brandmon))

  def load_collected_disk(self) -> None:
    try:
      with open (os.path.join(self.datadir, 'collected.json'), 'r') as f:
        self.collected_brandmon = json.loads(f.read())
    except:
      self.collected_brandmon = {}

  def set_locale(self, locale: str) -> None:
    url = locale
    self.driver.get("https://" + url)
    self.locale = locale

    if self.browser == 'firefox':
      if locale == 'singapore':
        self.opts.set_preference("intl.accept_languages", "en-US")
      elif locale == 'global':
        self.opts.set_preference("intl.accept_languages", "en-US")
    elif self.browser == 'chrome':
      if locale == 'singapore':
        self.opts.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
      elif locale == 'global':
        self.opts.add_experimental_option('prefs', {'intl.accept_languages': 'ko,ko_KR'})
    #TODO: implementing dynamic locale when set_locale is called

    self.close_popup()

  def render_msg(self, msg: str) -> None:
    self.driver.execute_script("""
      let body = document.getElementsByTagName('body')[0];
      let msg = document.createElement('div');
      msg.setAttribute('style', 'position: absolute; top: 10px; left: 10px; padding: 10px 30px; background-color: rgba(255, 255, 255, 0.85); border: 1px #ccc solid; color: #444; font-size: 35pt; font-weight: 700; z-index: 1000;');
      msg.innerHTML = '{}';
      body.parentNode.insertBefore(msg, body);""".format(msg))

  def quit(self) -> None:
    self.driver.quit()
  
  def log(self, message: str, error: bool=False) -> None:
    if self.logging == True or error == True:
      print(datetime.datetime.now().strftime("%H:%M:%S"), message)

  def close_popup(self) -> None:
    try:
      mobileweb = self.driver.find_element(By.ID, "btn_download_app_close")
      mobileweb.click()
      self.log('[click] close app download popup')
    except:
      pass
    try:
      wish = self.driver.find_element(By.CLASS_NAME, "wishplus-notice__button")
      closebutton = wish.find_element(By.TAG_NAME, "button")
      closebutton.click()
      self.log('[click] close wish popup')
    except:
      pass

  def login(self, loginmethod: str=loginmethods.login_qoo10, username: str='', password: str='', random_delay: bool=True) -> None:
    self.close_popup()

    login_btn = None
    try:
      menu_icon = self.driver.find_element(By.CSS_SELECTOR, ".header__icon--menu")
      menu_icon.click()

      self.log('[click] menu')

      if random_delay == True:
        time.sleep(random.uniform(0.5, 2))

      login_btn = self.driver.find_element(By.ID, "nav_login_view").find_element(By.CLASS_NAME, "name")
      if 'login' not in login_btn.get_attribute('innerHTML').lower():
        self.log('[alert] already logged in')
        return
    except (NoSuchElementException, ElementNotInteractableException):
      bottom_bar = self.driver.find_element(By.ID, "common_bottom_tab_bar")
      mypage = bottom_bar.find_elements(By.TAG_NAME, "a")[4]
      mypage.click()

      self.log('[click] mypage')

      if random_delay == True:
        time.sleep(random.uniform(0.5, 2))

      buttons = self.driver.find_element(By.ID, "aspnetForm").find_elements(By.TAG_NAME, "a")
      for button in buttons:
        if button.get_attribute('href') != None and 'login' in button.get_attribute('href').lower():
          login_btn = button
          break

    if login_btn == None:
      self.log('[alert] already logged in')
      return
    
    try:
      login_btn.click()
      self.log('[click] login button')
    except (NoSuchElementException, ElementNotInteractableException):
      self.log('[alert] already logged in')
      return

    if random_delay == True:
      time.sleep(random.uniform(0.5, 2))

    if loginmethod == loginmethods.login_qoo10:
      div = self.driver.find_element(By.CLASS_NAME, "login_type")
      login_qoo10 = div.find_element(By.TAG_NAME, "a")
      login_qoo10.click()

      if random_delay == True:
        time.sleep(random.uniform(0.5, 1.5))

      self.driver.execute_script("document.getElementById('login_id').value='{}'".format(username))
      self.driver.execute_script("document.getElementById('id_passwd').value='{}'".format(password))
      self.render_msg('Please log in.')

    elif loginmethod == loginmethods.login_facebook:
      div = self.driver.find_element(By.CLASS_NAME, "sns_mthd")
      login = div.find_elements(By.TAG_NAME, "a")
      login[0].click()
    elif loginmethod == loginmethods.login_google:
      div = self.driver.find_element(By.CLASS_NAME, "sns_mthd")
      login = div.find_elements(By.TAG_NAME, "a")
      login[1].click()
    elif loginmethod == loginmethods.login_line:
      div = self.driver.find_element(By.CLASS_NAME, "sns_mthd")
      login = div.find_elements(By.TAG_NAME, "a")
      login[2].click()
    elif loginmethod == loginmethods.login_kakaotalk:
      div = self.driver.find_element(By.CLASS_NAME, "sns_mthd")
      login = div.find_elements(By.TAG_NAME, "a")
      login[3].click()
    elif loginmethod == loginmethods.login_apple:
      div = self.driver.find_element(By.CLASS_NAME, "sns_mthd")
      login = div.find_elements(By.TAG_NAME, "a")
      login[4].click()
    else:
      self.render_msg('Please log in.')

    self.log('[alert] Waiting for login', error=True)
    while True:
      try:
        login_btn = self.driver.find_element(By.CLASS_NAME, "footer-conts__btn").find_elements(By.TAG_NAME, "button")[1]
        if 'Logout' in login_btn.get_attribute('onclick'):
          break
      except:
        pass
      try:
        user_info = self.driver.find_element(By.CLASS_NAME, "qbx_usr_inf")
        break
      except:
        pass
      time.sleep(0.3)
    self.log('[alert] Login completed', error=True)
    if random_delay == True:
      time.sleep(random.uniform(0.5, 2))
    self.close_popup()

    self.go_home()
      
  #Brandmon collector
  def collect_brandmon(self, random_delay: bool=True) -> tuple[int, int]:
    brandmoncnt = 0
    mameqcnt = 0
    try:
      collected = self.load_collected('brandmon')

      try:
        shopping_tweets_present = EC.presence_of_element_located((By.ID, "h3_header_top_area"))
        WebDriverWait(self.driver, timeout).until(shopping_tweets_present)
      except TimeoutException:
        self.log('[error] timeout (shopping tweets link not found)', error=True)
        return brandmoncnt, mameqcnt

      self.close_popup()

      shopping_tweets = self.driver.find_element(By.ID, "h3_header_top_area")
      shopping_link = shopping_tweets.find_element(By.CLASS_NAME, "main-tt__lnk")
      try:
        shopping_link.click()
        self.log('[click] shopping tweets')
      except ElementClickInterceptedException:
        self.log('[error] click intercepted. failed to click shopping tweets', error=True)
        self.log('[navigate] scroll and retry')
        self.driver.execute_script("window.scrollBy(0, 300);")
        try:
          shopping_link.click()
          self.log('[click] shopping tweets')
        except ElementClickInterceptedException:
          self.log('[error] click intercepted. failed to click shopping tweets', error=True)
        except TimeoutException:
          self.log('[error] timeout (shopping tweets list not found)', error=True)
      except TimeoutException:
        self.log('[error] timeout (shopping tweets list not found)', error=True)

      while True:
        try:
          shopping_tweets_present = EC.presence_of_element_located((By.ID, "ul_shopping_tweet_push_list"))
          WebDriverWait(self.driver, timeout).until(shopping_tweets_present)
        except TimeoutException:
          self.log('[error] timeout (shopping tweets list not found)', error=True)
          self.log('[message] back to the main page')
          try:
            admon_popup = self.driver.find_element(By.ID, "countdown_span")
            self.driver.execute_script("closeLayer();")
          except:
            pass
          self.go_home()
          self.log('[message] waiting...')
          if random_delay == True:
            time.sleep(random.uniform(1.5, 4))
          try:
            shopping_tweets_present = EC.presence_of_element_located((By.ID, "h3_header_top_area"))
            WebDriverWait(self.driver, timeout).until(shopping_tweets_present)
          except TimeoutException:
            self.log('[error] timeout (shopping tweets link not found)', error=True)
            break
          shopping_tweets = self.driver.find_element(By.ID, "h3_header_top_area")
          shopping_tweets.find_element(By.CLASS_NAME, "main-tt__lnk").click()
          self.log('[click] shopping tweets')
          continue
        self.log('[fetch] parsing shopping tweets')
        all_tweets = self.driver.find_element(By.ID, "ul_shopping_tweet_push_list").find_elements(By.TAG_NAME, "li")
        found = False
        for i in all_tweets:
          try:
            mon = i.find_element(By.CLASS_NAME, "mon")
            link = i.find_element(By.TAG_NAME, "a")
            mark = link.find_element(By.TAG_NAME, "mark")
            href = link.get_attribute("href")
            click = i.find_element(By.TAG_NAME, "h2")
          except:
            continue
          time.sleep(1)
          if href in collected:
            continue
          collected.append(href)
          self.driver.get(href)
          if random_delay == True:
            time.sleep(random.uniform(1.5, 4))
          found = True
          break

        #time.sleep(4)
        mon_type = 0
        if found == True:
          try:
            time.sleep(1)
            mameq = self.driver.find_element(By.ID, "mameQ_event_banner").find_element(By.TAG_NAME, "a")
            mameq.click()
            self.log('[collect] mameq')
            if random_delay == True:
              time.sleep(random.uniform(1.5, 4))
            mameqcnt += 1
            mon_type = 1
          except:
            try:
              brandmon = self.driver.find_element(By.ID, "brandmon_banner_get_btn")
              time.sleep(5)
              brandmon.click()
              self.log('[collect] brandmon')
              if random_delay == True:
                time.sleep(random.uniform(1.5, 4))
              brandmoncnt += 1
              mon_type = 2
            except:
              pass

          try:
            x_present = EC.presence_of_element_located((By.CLASS_NAME, "innr_cont"))
            WebDriverWait(self.driver, timeout).until(x_present)
          except TimeoutException:
            self.log('[error] timeout (mameq result not found)', error=True)
          if mon_type == 1:
            self.driver.execute_script("if(window.goClose) goClose();")
            self.log('[click] close the popup')
            if random_delay == True:
              time.sleep(random.uniform(1.5, 4))
          self.driver.back()
          self.log('[navigate] back')
          self.log('[message] back to the tweet list')
          if random_delay == True:
            time.sleep(random.uniform(1.5, 4))
          time.sleep(1)
        else:
          self.driver.back()
          self.log('[navigate] back')
          time.sleep(1)
          break
      
      self.close_popup()

      self.save_collected('brandmon', collected)
      self.save_collected_disk()
      return brandmoncnt, mameqcnt
    except:
      self.log('[error] unhandled exception.', error=True)
      import traceback
      traceback.print_exc()
      return brandmoncnt, mameqcnt

  #qlounge
  def collect_mameq(self, random_delay: bool=True) -> int:
    collected_mameq = self.load_collected('mameq')
    mameq_cnt = 0
    action = ActionChains(self.driver)
    links = self.driver.find_elements(By.CLASS_NAME, "swp_slide")
    action.drag_and_drop_by_offset(links[4], -240, 0).perform()
    if random_delay == True:
      time.sleep(random.uniform(0.3, 0.8))
    action.drag_and_drop_by_offset(links[8], -240, 0).perform()
    if random_delay == True:
      time.sleep(random.uniform(0.3, 0.8))
    for i in links:
      a = i.find_element(By.TAG_NAME, "a")
      href = a.get_attribute('href')
      if 'Funzone' in href:
        a.click()
        self.log('[click] Q lounge')
        if random_delay == True:
          time.sleep(random.uniform(1, 2))
        break
    links = self.driver.find_elements(By.TAG_NAME, "a")
    rewardlink = False
    for i in links:
      href = i.get_attribute('href')
      img = None
      try:
        img = i.find_element(By.TAG_NAME, 'img')
        #print(href, img, img.get_attribute('src'))
        if href != None and 'https' in href and (('8927' in href or '8448' in href) and 'dynamicad' in href.lower()):
          i.click()
          self.log('[click] mameq rewards')
          if random_delay == True:
            time.sleep(random.uniform(1.5, 3))
          rewardlink = True
          break
      except:
        pass
    if rewardlink == False:
      self.log('[error] failed to find rewards page link. directly browse', error=True)
      self.driver.get('https://special.qoo10.sg/DynamicAD/8448/')
      if random_delay == True:
        time.sleep(random.uniform(1, 2))
      #self.log('[error] failed to find rewards page', error=True)
      #return 0
    try:
      WebDriverWait(self.driver, timeout).until(EC.number_of_windows_to_be(2))
    except TimeoutException:
      pass
    original_tab = self.driver.current_window_handle
    for window_handle in self.driver.window_handles:
      if window_handle != original_tab:
        self.driver.switch_to.window(window_handle)
        self.log('[browse] move to the new tab')
        break

    while True:
      tables = self.driver.find_elements(By.TAG_NAME, "table")
      opened = False
      found = False
      for table in tables:
        try:
          tds = table.find_elements(By.TAG_NAME, "td")
        except:
          self.log('[error] exception raised', error=True)
          import traceback
          traceback.print_exc()
          tds = []
        for td in tds:
          try:
            a = td.find_element(By.TAG_NAME, "a")
            href = a.get_attribute('href')
            img = a.find_element(By.TAG_NAME, "img")
            src = img.get_attribute('src')
            if img != None and ('Collect' in src or 'Visit' in src or 'Browse' in src or 'MameQ' in src) and 'DynamicAD' in href and href not in collected_mameq:
              found = True
              if random_delay == True:
                time.sleep(random.uniform(1, 2))
              collected_mameq.append(href)
              try:
                img.click()
                self.log('[click] mameq page')
              except ElementClickInterceptedException:
                self.log('[error] mameq page click intercepted', error=True)
                self.driver.execute_script("window.scrollBy(0, 300);")
                img.click()
              if random_delay == True:
                time.sleep(random.uniform(1, 2))
              try:
                WebDriverWait(self.driver, timeout).until(EC.number_of_windows_to_be(3))
              except TimeoutException:
                self.log('[error] timeout (failed to enter mameq page)', error=True)
                pass
              list_tab = self.driver.current_window_handle
              for window_handle in self.driver.window_handles:
                if window_handle != original_tab and window_handle != list_tab:
                  self.driver.switch_to.window(window_handle)
                  self.log('[navigate] move to the new tab')
                  break
              while True:
                buttons = self.driver.find_elements(By.TAG_NAME, "a")
                for button in buttons:
                  href = button.get_attribute('href')
                  if href != None and 'javascript' in href and 'EventApply' in href:
                    try:
                      img_button = button.find_element(By.TAG_NAME, "img")
                      img_button.click()
                      self.log('[click] mameq')
                      if random_delay == True:
                        time.sleep(random.uniform(0.5, 1.5))
                      break
                    except ElementClickInterceptedException:
                      self.log('[error] click intercepted. failed to click button', error=True)
                      self.log('[navigate] scroll and retry')
                      self.driver.execute_script("window.scrollBy(0, 300);")
                    except ElementNotInteractableException:
                      self.log('[error] element not interactable. failed to click button', error=True)
                      self.log('[interact] scroll and retry')
                      self.driver.execute_script("window.scrollBy(0, 300);")
                failed = False
                try:
                  x_present = EC.presence_of_element_located((By.CLASS_NAME, "ly_event_apply"))
                  WebDriverWait(self.driver, timeout_mameq).until(x_present)
                except TimeoutException:
                  self.log('[error] timeout. retry', error=True)
                  try:
                    img_button = button.find_element(By.TAG_NAME, "img")
                    img_button.click()
                  except ElementClickInterceptedException:
                    self.log('[error] click intercepted. failed to click button', error=True)
                    self.log('[navigate] scroll and retry')
                    self.driver.execute_script("window.scrollBy(0, 300);")
                  except ElementNotInteractableException:
                    self.log('[error] element not interactable. failed to click button', error=True)
                    self.log('[interact] scroll and retry')
                    self.driver.execute_script("window.scrollBy(0, 300);")
                  try:
                    x_present = EC.presence_of_element_located((By.CLASS_NAME, "ly_event_apply"))
                    WebDriverWait(self.driver, timeout_mameq).until(x_present)
                  except TimeoutException:
                    self.log('[error] 2nd timeout. try next mameq', error=True)
                    failed = True
                except ElementClickInterceptedException:
                  self.log('[error] failed to click button', error=True)
                  failed = True
                except ElementNotInteractableException:
                  self.log('[error] failed to click button', error=True)
                  failed = True
                except NoSuchElementException:
                  self.log('[error] No mameq found', error=True)
                  failed = True
                if failed == False:
                  img_found = False
                  popups = self.driver.find_elements(By.CLASS_NAME, "ly_event_apply")
                  redeemed = False
                  for popup in popups:
                    try:
                      img = popup.find_element(By.TAG_NAME, "img")
                      if 'wait' in img.get_attribute('src'):
                        img_found = True
                        break
                    except:
                      pass
                    try:
                      sorry = popup.find_element(By.ID, "SorryTxt")
                      if 'redeem' in sorry.get_attribute("innerHTML"):
                        redeemed = True
                        break
                    except:
                      pass
                  if img_found == True:
                    self.log('[fail] failed to collect mameq. retry')
                    if random_delay == True:
                      time.sleep(random.uniform(1.5, 4))
                    self.driver.execute_script("if(window.goClose) goClose();")
                    if random_delay == True:
                      time.sleep(random.uniform(1, 2))
                    continue
                  elif redeemed == True:
                    self.log('[fail] mameq fully redeemed. close popup')
                    break
                  else:
                    self.log('[collect] collected mameq. close popup')
                    mameq_cnt += 1
                    break
                else:
                  break
              self.driver.execute_script("if(window.goClose) goClose();")
              if random_delay == True:
                time.sleep(random.uniform(0.5, 1.5))
                
              self.driver.close()
              self.driver.switch_to.window(list_tab)
              self.log('[navigate] close tab')
              opened = True
              break
          except NoSuchElementException:
            pass
          except StaleElementReferenceException:
            pass
        if opened == True:
          break
      if found == False:
        break
    
    self.log('[message] collected all mameqs. close')
    self.driver.close()
    try:
      self.driver.switch_to.window(original_tab)
    except:
      pass
    
    self.go_home()

    self.save_collected('mameq', collected_mameq)
    try:
      self.set_locale(self.locale)
    except:
      pass
    return mameq_cnt
  
  def go_home(self) -> None:
    try:
      home_btn = self.driver.find_element(By.ID, 'common_bottom_tab_bar').find_element(By.TAG_NAME, 'a')
      if 'home' in home_btn.get_attribute('innerHTML'):
        home_btn.click()
      else:
        raise NoSuchElementException
      self.log('[click] main page')
    except (ElementClickInterceptedException, NoSuchElementException):
      self.log('[error] cannot click main page link', error=True)
      self.driver.get('https://' + self.locale)

  def attend(self, random_delay: bool=True) -> None:
    action = ActionChains(self.driver)
    links = self.driver.find_elements(By.CLASS_NAME, "swp_slide")
    action.drag_and_drop_by_offset(links[4], -240, 0).perform()
    if random_delay == True:
      time.sleep(random.uniform(0.3, 0.8))
    action.drag_and_drop_by_offset(links[8], -240, 0).perform()
    if random_delay == True:
      time.sleep(random.uniform(0.3, 0.8))
    for i in links:
      a = i.find_element(By.TAG_NAME, "a")
      href = a.get_attribute('href')
      if 'Funzone' in href:
        a.click()
        self.log('[click] Q lounge')
        if random_delay == True:
          time.sleep(random.uniform(1, 3))
        break
    try:
      self.driver.switch_to.frame(self.driver.find_element(By.ID, "RouletteQMobile"))
      stamp = self.driver.find_element(By.ID, "td_today")
      self.log('[click] stamp found')
      self.driver.execute_script("Attendance.apply();")
      stamp.click()
      self.log('[click] stamp')
    except NoSuchElementException:
      self.log('[error] attendance not available', error=True)
    self.driver.switch_to.default_content()
    
    if random_delay == True:
      time.sleep(random.uniform(1, 3))
    try:
      ok = self.driver.find_element(By.CLASS_NAME, "btn--submit")
      ok.click()
      self.log('[click] ok')
      if random_delay == True:
        time.sleep(random.uniform(1, 3))
    except NoSuchElementException:
      try:
        self.driver.switch_to.frame(self.driver.find_element(By.ID, "RouletteQMobile"))
        self.driver.switch_to.frame(self.driver.find_element(By.ID, "roulette_board"))
        play = self.driver.find_element(By.TAG_NAME, "button")
        play.click()
        self.log('[click] roulette play')
        if random_delay == True:
          time.sleep(random.uniform(1.5, 4))
      except:
        self.log('[error] roulette not available', error=True)

    self.set_locale(self.locale)
  
  def collect_mameball(self, random_delay: bool=True) -> None:
    action = ActionChains(self.driver)
    links = self.driver.find_elements(By.CLASS_NAME, "swp_slide")
    action.drag_and_drop_by_offset(links[4], -240, 0).perform()
    if random_delay == True:
      time.sleep(random.uniform(0.3, 0.8))
    action.drag_and_drop_by_offset(links[8], -240, 0).perform()
    if random_delay == True:
      time.sleep(random.uniform(0.3, 0.8))
    for i in links:
      a = i.find_element(By.TAG_NAME, "a")
      href = a.get_attribute('href')
      if 'Funzone' in href:
        a.click()
        self.log('[click] Q lounge')
        if random_delay == True:
          time.sleep(random.uniform(1, 3))
        break
    dashboard = self.driver.find_element(By.ID, "dashboard")
    try:
      mameball = dashboard.find_elements(By.TAG_NAME, "tr")[3].find_element(By.TAG_NAME, "a")
      mameball.click()
      self.log('[click] collected mameball')
    except IndexError:
      self.log('[error] mameball not found', error=True)
    except ElementClickInterceptedException:
      self.log('[error] click intercepted. failed to collect mameball', error=True)
      self.log('[navigate] scroll and retry')
      self.driver.execute_script("window.scrollBy(0, 300);")
      try:
        mameball.click()
      except ElementClickInterceptedException:
        self.log('[error] click intercepted. failed to collect mameball (2nd)', error=True)
        self.log('[navigate] scroll and retry')
        self.driver.execute_script("window.scrollBy(0, 300);")
        try:
          mameball.click()
        except ElementClickInterceptedException:
          self.log('[error] failed collecting mameq', error=True)
    if random_delay == True:
      time.sleep(random.uniform(1, 3))
    self.set_locale(self.locale)