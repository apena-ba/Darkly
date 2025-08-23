# Broken Access Control in password recovery page

## 📖 Vulnerability Explanation
Broken access control vulnerability is a security flaw that allows unauthorized users to access, modify, or delete data they shouldn't have access to.

In this exercise, the password recovery page uses the parameter _mail_, which is set to _webmaster@borntosec.com_ by default. This parameter is not protected and can be modified, so attackers can abuse this flaw to check if an email exists in the database.

## ⚙️ Exploitation Process
Modify the value of the _mail_ parameter to another email adress.
- This request gives us the flag:

```
curl -s -X POST -d 'mail=malicious@gmail.com&Submit=Submit' 'http://BornToSec.com/index.php?page=recover' | grep flag
```

## 🔧 Fix
By returning the same response regardless of whether the email belongs to a user or not, it becomes impossible to enumerate users.

## ☝️🤓 Advanced explanation
This vulnerability can lead to several security issues:
- **Username enumeration:** The case that we chose to detail here. Attackers can determine whether a username exists in the system or not if the application returns a different response for valid accounts compared to invalid ones.
- **Admin account password reset:** If the app uses the email to send a password reset option for the admin account, an attacker could gain access to it by setting a different password.