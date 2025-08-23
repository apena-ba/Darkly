# Improper Input Validation in survey POST request

## 📖 Vulnerability Explanation
An improper input validation happens when the server trusts the user's input. Attackers can take advantage of this, leading to:

- **DoS:** Might overload the server or cause unexpected behaviour
- **Injection attacks:** If the input is used in file paths or SQL queries
- **Data corruption:** Data becomes unreliable

## ⚙️ Exploitation Process
When clicking on a number in the survey page, the app sends a request with the selected value. We can upload an arbitrary amount in the _valeur_ field and get the flag.

```
curl -s -X POST -d 'sujet=2&valeur=11' 'http://BornToSec.com/index.php?page=survey' | grep flag
```

## 🔧 Fix
Sanitization on the server side is necessary. We can do this by checking that the user's input is in range.

## ☝️🤓 Advanced explanation
In order to check the input, we can use an _if_ statement and verify the data is a number between 1 and 10. 

```
<?php

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $valeur = filter_input(INPUT_POST, 'valeur', FILTER_VALIDATE_INT);

    if ($valeur !== false && $valeur >= 1 && $valeur <= 10) {
        // Process data submitted
    } else {
        // Display error
    }
}

?>
```