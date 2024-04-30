## Qoo10 miner

* Automated brandmon mining from Qoo10

### Prerequisites

* Selenium
```
$ pip install -r requirements.txt
```
* ChromeDriver
#### macOS
```
$ brew cask install chromedriver
```
#### Linux
```
[Download chromedriver](https://googlechromelabs.github.io/chrome-for-testing/) and put in into PATH.
```
#### Windows
```
[Download chromedriver](https://googlechromelabs.github.io/chrome-for-testing/) and put in into PATH.
```

### Usage

* Examples
  * Complete daily MameQ mission and collect up to 10 MameQs with Kakao-linked account: [example_kakaologin.py](example_kakaologin.py)
  * Complete daily MameQ mission and collect up to 10 MameQs with Qoo10 account: [example_qoo10login.py](example_qoo10login.py)
  * Collect all brandmons from Qoo10: [example_brandmon.py](example_brandmon.py)
  * Always-on daemon to automatically collect all brandmons and to automatically finish all daily mission: [example_daemon.py](example_daemon.py)