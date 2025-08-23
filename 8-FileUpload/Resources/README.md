# File Upload

## 📖 Vulnerability Explanation
A file upload vulnerability occurs when a server doesn't validate an uploaded file properly. This can be abused to perform RCE in the server by uploading executable code into a malicious crafted file.

The server only checks the file type present in the form request body. By uploading a php file and changing the image type property, we can trick the server to accept the executable code.

## ⚙️ Exploitation Process

- Create a file called shell.php and send this request with ```curl``` to claim the flag:

```
touch shell.php && curl -s -X POST "http://BornToSec.com/?page=upload" -F "uploaded=@shell.php;filename=shell.php;type=image/jpeg" -F "Upload=Upload" | grep flag && rm shell.php
```

## 🔧 Fix
To protect against file upload attacks, it's crutial to perform a secure sanitization.

The process should be as following:
- **Check file magic bytes**: To make sure the file is an actual image
- **Allow only certain extensions**: Create a whitelist of allowed extensions
- **Generate a filename on the server**: Generating a new filename on the server prevents problems with filename attack techniques

## ☝️🤓 Advanced explanation
It is also possible to use a file processing tool, such as ImageMagick. However, it is important to make sure the packages are up to date, as it is common to see vulnerabilities associated with these tools.