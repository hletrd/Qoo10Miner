## Qoo10 miner

* Automated brandmon mining from Qoo10

### Prerequisites

* Selenium
```
$ pip install -r requirements.txt
```

* ChromeDriver
  * macOS
```
$ brew cask install chromedriver
```

  * Linux
    * [Download chromedriver](https://googlechromelabs.github.io/chrome-for-testing/) and put in into PATH.

  * Windows
    * [Download chromedriver](https://googlechromelabs.github.io/chrome-for-testing/) and put in into PATH.

### Usage

* Start with importing Qoo10 module.
```
import qoo10
```
* ```qoo10.Qoo10()```: Create a Qoo10 instance.
  * ```datadir```: set data directory to store cookies and other data.
  * ```locale```: set locale. Available locales are ```qoo10.locales.qoo10_global``` (which directs to qoo10.com) and ```qoo10.locales.qoo10_singapore``` (which directs to qoo10.sg).
  * ```executable_path``` (optional): set path to ChromeDriver/GeckoDriver executable.
  * ```install``` (optional, ```False``` by default): set to ```True``` to install ChromeDriver/GeckoDriver automatically via webdriver_manager. webdriver_manager is required.
  * ```browser``` (optional, ```chrome``` by default): set browser to use. Available browsers are ```chrome``` and ```firefox```.
  * ```load_saved``` (optional, ```True``` by default): set to ```True``` to load saved cookies and other data.
  * ```headless``` (optional, ```False``` by default): set to ```True``` to run browser in headless mode.
  * ```logging``` (optional, ```True``` by default): set to ```True``` to enable logging.
* ```qoo10.set_locale()```: Set locale.
  * ```locale```: set locale. Available locales are ```qoo10.locales.qoo10_global``` (which directs to qoo10.com) and ```qoo10.locales.qoo10_singapore``` (which directs to qoo10.sg).
* ```qoo10.login()```: Login to Qoo10.
  * ```loginmethod``` (optional, ```qoo10.loginmethods.qoo10``` by default): set login method. Available login methods are ```qoo10.loginmethods.qoo10``` (Qoo10 account), ```qoo10.loginmethods.login_facebook``` (Facebook account), ```qoo10.loginmethods.login_google``` (Google account), ```qoo10.loginmethods.login_line``` (Line account), ```qoo10.loginmethods.login_kakaotalk``` (KakaoTalk account) and ```qoo10.loginmethods.apple``` (Apple account). May require manual CAPTCHA for Qoo10 login, thereby not supporting headless mode.
  * ```username```: email address.
  * ```password```: password.
  * ```random_delay``` (optional, ```True``` by default): add random delay between each actions.
* ```qoo10.collect_brandmons()```: Collect all brandmons that are available from the main page.
  * ```random_delay``` (optional, ```True``` by default): add random delay between each actions.
* ```qoo10.collect_mameq()```: Collect MameQs that are available from the daily mission page. Note that this function is only available for ```qoo10.sg```.
  * ```random_delay``` (optional, ```True``` by default): add random delay between each actions.
* ```qoo10.attend()```: Attend daily mission.
  * ```random_delay``` (optional, ```True``` by default): add random delay between each actions.
* ```qoo10.collect_mameball()```: Collect 3 daily mameballs.
  * ```random_delay``` (optional, ```True``` by default): add random delay between each actions.

### Examples
* Complete daily MameQ mission and collect up to 10 MameQs with Kakao-linked account: [example_kakaologin.py](example_kakaologin.py)
* Complete daily MameQ mission and collect up to 10 MameQs with Qoo10 account: [example_qoo10login.py](example_qoo10login.py)
* Collect all brandmons from Qoo10: [example_brandmon.py](example_brandmon.py)
* Always-on daemon to automatically collect all brandmons and to automatically finish all daily mission: [example_daemon.py](example_daemon.py)