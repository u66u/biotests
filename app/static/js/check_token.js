document.getElementById('menu-container').addEventListener('htmx:afterSwap', function(event) {
    var response = JSON.parse(event.detail.xhr.responseText);
    var menu = document.getElementById('menu');
    var textColor = menu.getAttribute('text-color');
    var hoverTextColor = menu.getAttribute('data-hover-text-color');

    var menuItems = `
        <nav class="text-sm mb-8">
            <ul id class="flex justify-start space-x-4">
                <li><a href="/" class="${textColor} ${hoverTextColor} text-lg">Home</a></li>
                <li class="hidden sm:inline">·</li>
                <li><a href="/tests" class="${textColor} ${hoverTextColor} text-lg">Tests</a></li>
                <li class="hidden sm:inline">·</li>
                <li><a href="/about" class="${textColor} ${hoverTextColor} text-lg">About</a></li>
                <li class="hidden sm:inline">·</li>
                <li><a href="/profile" class="${textColor} ${hoverTextColor} text-lg">Profile</a></li>
                <li class="hidden sm:inline">·</li>
                <li><a href="/logout" class="${textColor} ${hoverTextColor} text-lg">Logout</a></li>
            </ul>
        </nav>
    `;

    if (response.valid) {
        menu.innerHTML = menuItems;
    } else {
        menu.innerHTML = `
            <nav class="text-sm mb-8">
                <ul id class="flex justify-start space-x-4">
                <li><a href="/" class="${textColor} ${hoverTextColor} text-lg">Home</a></li>
                <li class="hidden sm:inline">·</li>
                <li><a href="/tests" class="${textColor} ${hoverTextColor} text-lg">Tests</a></li>
                <li class="hidden sm:inline">·</li>
                <li><a href="/about" class="${textColor} ${hoverTextColor} text-lg">About</a></li>
                <li class="hidden sm:inline">·</li>
                <li><a href="/login" class="${textColor} ${hoverTextColor} text-lg">Login</a></li>
                </ul>
            </nav>
        `;
    }
});
