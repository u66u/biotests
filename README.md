Requires python 3.12

Make sure you have tailwind installed:
```
npm i -g tailwindcss
```

Download the latest version of htmx and run the tailwind watch server:
```
wget -O app/static/js/htmx.js https://raw.githubusercontent.com/bigskysoftware/htmx/master/src/htmx.js
cd app/static/css && npx tailwindcss -i styles.css -o tailwind.css --watch
```
Keep in mind that the produced tailwind.css file will be cached in the browser, so live reload might seem like it's not working. In that case use incognito mode or turn off caching in F12 -> Network.

TODO:
- Create html template for profile
- Password restoration and logout
- Check for security vulnerabilities
- Add epigenetic tests