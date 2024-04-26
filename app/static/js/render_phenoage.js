document.addEventListener('htmx:afterSwap', function(event) {
    if (event.detail.target.id === 'result') {
        const response = JSON.parse(event.detail.xhr.response);
        const biologicalAge = response.result;
        const birthday = new Date(document.getElementById('birthday').value);
        const chronologicalAge = Math.floor((new Date() - birthday) / (365.25 * 24 * 60 * 60 * 1000));
        const difference = biologicalAge - chronologicalAge;

        let arrowPosition;
        if (difference < -10) {
            arrowPosition = 0;
        } else if (difference > 10) {
            arrowPosition = 100;
        } else {
            arrowPosition = (difference + 10) * 5;
        }

        const scale = `
            <div class="mt-4">
                <div class="flex justify-between">
                    <span>-10</span>
                    <span>-5</span>
                    <span>0</span>
                    <span>+5</span>
                    <span>+10</span>
                </div>
                <div class="relative h-6 bg-gray-200">
                    <div class="absolute inset-0 flex items-center" style="left: ${arrowPosition}%;">
                        <div class="h-8 w-0.5 bg-black"></div>
                    </div>
                    <div class="absolute inset-0 flex items-center justify-center">
                        <div class="h-3 w-3 bg-black transform rotate-45"></div>
                    </div>
                </div>
            </div>
        `;

        event.detail.target.innerHTML = `
            <p>Chronological age: ${chronologicalAge} years.</p>
            <p>Biological age: ${biologicalAge.toFixed(2)} years.</p>
            <p>The difference between your biological age and chronological age is ${difference.toFixed(2)} years.</p>
            ${scale}
        `;
    }
});
