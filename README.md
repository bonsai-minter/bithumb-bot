# Bithumb bot
[RU](https://github.com/bonsai-minter/bithumb-bot#%D0%BD%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B8)
[EN](https://github.com/bonsai-minter/bithumb-bot#Settings)
## Settings

    [auth]
    
    api_key = "123456" #public key
    
    api_key_auth = "1234567890" #private key
    
    [notify]
    
    nootification_on_desktop = false #true or false
    
    enabled = false #true or false
    
    symbols = ["BTC-USDT","BIP-USDT"]
    
    timeout = 30 #seconds
    
    time = 1 #minutes
    
    [scallping]
    
    nootification_on_desktop = true #true or false
    
    enabled = true #true or false
    
    symbols = ["BTC-USDT"] #more pairs can be cause of errors
    
    percent = 0.001
    
    percent_to_play = 80
    
    save_percent = 2
    
    strategy = "last" #last(recomemded) or normal
   For start you need simple change value of api_key and api_key_auth. You can find this values in [Bithumb](https://www.bithumb.pro/ru-ru/account/user/api-key/list)
   ![Creating Api Key](https://i.imgur.com/HJZBYdD.png)After press the button you will need to write confidential data.
   ![conf data](http://i.imgur.com/mJAtNNF.png)
   After execute data you will show new api key
   ![api key](http://i.imgur.com/MxLNWIx.png)You need to press Modify and add access to Open Trading
   ![change settings](http://i.imgur.com/vhpvTpv.png)Only after press Save but if you had a static ip (in most cases no) set own ip in Restrict access to trusted IPs only 
If you havent static ip you will need to change the key in settings every month
VERY IMPORTANT!!! Save Secret key before exiting page
## Installing
On Linux:

    sudo apt install python3 python3-pip
    git clone https://github.com/bonsai-minter/bithumb-bot.git
    cd bithumb-bot
    pip3 install -r requirements.txt
    #Change settings in config.toml for example you can change with nano
    python3 main.py
   Or you can download from [last release](https://github.com/bonsai-minter/bithumb-bot/releases) files:
 
     main
     config.toml

   And start `./main` in command line

On Windows:
	Download [python3](https://www.python.org/ftp/python/3.8.3/python-3.8.3-amd64.exe)
	Execute python-#.#.#-amd64.exe

VERY IMPORTNANT!!!!!
you need add python in path

![path](https://gblobscdn.gitbook.com/assets/-LrUFpF96No0YKIFuw-v/-LrUpjlwRU4LMTTiOpc1/-LrUr6Jvx8n2ZtZ_ht4M/Screenshot_9.png)
	Download [release](https://github.com/bonsai-minter/bithumb-bot/archive/master.zip)
	Unzip master.zip
	Go to directory master
	Copy full path and after press Win + R after write `powershell`
	Write `cd '` Press Right Button on mouse and write `'` and press Enter
	You will go to folder with project
	Execute in command line `pip install -r requirements.txt`
	After change settings in config.toml
	At last execute `python main.py`

Or you can simple download main.exe and config.toml from [last release](https://github.com/bonsai-minter/bithumb-bot/releases) 
change settings in config.toml and execute main.exe

    

## Настройки

    [auth]
    
    api_key = "123456" #public key
    
    api_key_auth = "1234567890" #private key
    
    [notify]
    
    nootification_on_desktop = false #true or false
    
    enabled = false #true or false
    
    symbols = ["BTC-USDT","BIP-USDT"]
    
    timeout = 30 #seconds
    
    time = 1 #minutes
    
    [scallping]
    
    nootification_on_desktop = true #true or false
    
    enabled = true #true or false
    
    symbols = ["BTC-USDT"] #more pairs can be cause of errors
    
    percent = 0.001
    
    percent_to_play = 80
    
    save_percent = 2
    
    strategy = "last" #last(recomemded) or normal
   Для начала вам нужно просто изменить значение api_key и api_key_auth. Вы можете найти эти значения в разделе [Bithumb](https://www.bithumb.pro/ru-ru/account/user/api-key/list)
   ![Creating Api Key](https://i.imgur.com/HJZBYdD.png)После нажатия кнопки вам нужно будет вписать данные
   ![conf data](http://i.imgur.com/mJAtNNF.png)
После вы увидите свой ключ
   ![api key](http://i.imgur.com/MxLNWIx.png)Вам нужно разрешить во вкладке Modify разрешить открывать торги (Open Trading)
   ![change settings](http://i.imgur.com/vhpvTpv.png)Ключ не валидный)
После этого обязательно нажмите Save но если у вас есть статичный ip адрес впишите его в разделе Restrict access to trusted IPs only (В большинстве случаев у вас не статичный ip) Если у вас нет статичного ip вы вынуждены менять api ключи каждый месяц
ОЧЕНЬ ВАЖНО!! Запишите секретный ключ перед выходом со страницы
## Установка
На линукс:

    sudo apt install python3 python3-pip
    git clone https://github.com/bonsai-minter/bithumb-bot.git
    cd bithumb-bot
    pip3 install -r requirements.txt
    #Change settings in config.toml for example you can change with nano
    python3 main.py
  Или скачайте с [последнего релиза](https://github.com/bonsai-minter/bithumb-bot/releases) файлы:
 
     main
     config.toml

   А после запустите из командной строки `./main` 

На Windows:
	Скачайте [python3](https://www.python.org/ftp/python/3.8.3/python-3.8.3-amd64.exe)
	Запустите python-#.#.#-amd64.exe

Важно!!!!! добавить python in Path

![path](https://gblobscdn.gitbook.com/assets/-LrUFpF96No0YKIFuw-v/-LrUpjlwRU4LMTTiOpc1/-LrUr6Jvx8n2ZtZ_ht4M/Screenshot_9.png)
	Скачайте [релиз](https://github.com/bonsai-minter/bithumb-bot/archive/master.zip)
	Распакуйте master.zip
	Перейдите в деректорию master
	Скопируте полный путь а после нажмте Win + R и в этом окошке напишите `powershell`
Впишите  `cd '` После нажмите правой кнопкой мыши чтобы вставить путь, напишите `'` и нажмите Enter
	Вы перейдете в директорию проекта
	Напишите в консоли `pip install -r requirements.txt`
	Затем измените настройки в config.toml через обозреватель файлов
	И наконец запустите `python main.py`

Или вы можете просто скчать main.exe и config.toml с [последнего релиза](https://github.com/bonsai-minter/bithumb-bot/releases) 
Измените настройки в config.toml и запустите main.exe
