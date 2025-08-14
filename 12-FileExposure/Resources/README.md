# File and Directory Exposure via accessible ```.hidden/``` directory

## 📖 Vulnerability Explanation
[Explain what the vulnerability is, how it works, and why it's dangerous. Include conditions required for exploitation if applicable.]

## ⚙️ Exploitation Process

- Enumerate the web directories via web fuzzing.
```
ffuf -u 'http://localhost:9090/FUZZ' -w /sgoinfre/students/apena-ba/cybersecurity/SecLists/Discovery/Web-Content/big.txt -fs 975

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0
________________________________________________

 :: Method           : GET
 :: URL              : http://localhost:9090/FUZZ
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

- Look for the flag using the command find:

```
find . -type f -exec grep flag {} \; -exec echo -e '\n [+] Flag found in file:' {} '\n' \;
```

## 🧰 Additional Resources Used *(Optional)*
- [Tool/Script Name]: [Brief description of purpose]
- Example: *Custom Python script to exploit XXE and read arbitrary files from the server.*

## 🔧 Fix
[Describe how to fix the vulnerability]

## ☝️🤓 Advanced explanation
[Provide advanced explanation for the bonus part]