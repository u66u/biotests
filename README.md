Make sure you have tailwind installed:
```
npm i -g tailwindcss
```

Download the latest version of htmx and run the tailwind watch server:
```
wget -O app/static/js/htmx.js https://raw.githubusercontent.com/bigskysoftware/htmx/master/src/htmx.js
cd app/static/css && npx tailwindcss -i styles.css -o tailwind.css --watch
```

TODO:
- Allow to take tests without login
- Create html templates for all pages
- Endpoint for password restoration
- Check for security vulnerabilities
- Add epigenetic tests