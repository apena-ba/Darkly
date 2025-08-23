# Open Redirect in redirect page

## 📖 Vulnerability Explanation
The redirect page uses the url parameter _site_ to make the user follow the redirection. As this parameter is not protected, it allows attackers to modify the url and redirect users, who trust the domain, into malicious websites.

## ⚙️ Exploitation Process
Modify the original url present in the page footer and set the value of the _site_ parameter to something else.

```
curl -s 'http://BornToSec.com/index.php?page=redirect&site=malicious.com' | grep flag
```

## 🔧 Fix
Defining a whitelist of the allowed redirection domain names would protect the url.

## ☝️🤓 Advanced explanation
The major risk associated to this vulnerability is **phishing**. Users could think this is a trusted link, but are redirected to a fake login or malicious site. This technique can also bypass restrictions, as it uses a trusted domain.

The following code mitigates the vulnerability using a whitelist.

```
<?php

$redirects = [
    'twitter' => 'https://twitter.com/BornToSec',
    'facebook' => 'https://facebook.com/BornToSec'
];

$site = $_GET['site'] ?? null;

if (isset($redirects[$site])) {
    // Redirect to the link in whitelist
    header("Location: " . $redirects[$site]);
} else {
    // Display error page
}

?>
```