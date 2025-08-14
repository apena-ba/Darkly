# Weak Credentials + Improper Restriction of Login Attempts

## 📖 Vulnerability Explanation
The application does not limit the authentication attempts, making a brute force attack possible. In addition to this, there is no strong password policy, facilitating password attacks.

## ⚙️ Exploitation Process
We will use ```hydra``` to perform the brute force attack and ```Seclists``` for the wordlists arguments. 

- Run hydra with the correct wordlists path:

```
hydra -L /sgoinfre/students/apena-ba/cybersecurity/SecLists/Usernames/top-usernames-shortlist.txt -P /sgoinfre/students/apena-ba/cybersecurity/SecLists/Passwords/Common-Credentials/xato-net-10-million-passwords-100.txt 127.0.0.1 -s 9090 http-get-form '/index.php:page=signin&username=^USER^&password=^PASS^&Login=Login:WrongAnswer.gif'
```

In order to use the http-get-form module, we must define a format string containing three parts:
1. Route to the login page
2. Parameters must contain at least one format string ```^USER^``` or ```^PASS^```
3. Failure string present in the response to recognise valid attempts

> It looks like any username works for the password _shadow_

## 🧰 Additional Resources
Hydra is a brute force attack tool used to test password security on several protocols and services. It uses wordlists as parameters and can be used for both password bruteforcing and password spraying.

- https://github.com/vanhauser-thc/thc-hydra

The wordlists we used for the brute force attack are part of the SecLists project, which is a recognised repository with multiple wordlists for various purposes.

- https://github.com/danielmiessler/SecLists.git

## 🔧 Fix
To protect the app authentication, two fixes should be implemented:

1. **Strong password policy**: Forcing users to set strong passwords limits the risk of being compromised by a malicious actor
2. **Limit login attempts**: To prevent brute force attacks, the app should restrict the amount of attempts on each account

## ☝️🤓 Advanced explanation
In order to strenghen the security posture of the application, we could use IDS/IPS to detect and protect against brute force attacks in real time. Furthermore, these systems log suspicious activities reinforcing the security on a network level.