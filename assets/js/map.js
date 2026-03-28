document.addEventListener('DOMContentLoaded', () => {
    const mapPins = document.querySelectorAll('.map-pin');
    const tooltip = document.getElementById('map-tooltip');
    const desiToggle = document.getElementById('desi-toggle');
    const mapContainer = document.querySelector('.map-container');

    // CITY DATA (The Board's Memory)
    const cities = {
        'paris': {
            name: 'Paris',
            date: 'Oct 2021',
            hook: 'Autumn leaves and the sparkle of the Eiffel.',
            url: 'posts/2021/paris-oct.html',
            isDesi: false
        },
        'amsterdam': {
            name: 'Amsterdam',
            date: 'Jul 2022',
            hook: 'Canals, bikes, and water-level living.',
            url: 'posts/2022/amsterdam-jul.html',
            isDesi: false
        },
        'brussels': {
            name: 'Brussels',
            date: 'Dec 2025',
            hook: 'Chocolate, Art Nouveau, and Christmas magic.',
            url: 'posts/2025/brussels-dec.html',
            isDesi: false
        },
        'gothenburg': {
            name: 'Gothenburg',
            date: 'Jul 2020',
            hook: 'Swedish summer and archipelago dreams.',
            url: 'posts/2020/gothenburg-jul.html',
            isDesi: false
        },
        'prague': {
            name: 'Prague',
            date: 'Jun 2022',
            hook: 'The scent of damp stone and warm trdelník.',
            url: 'posts/2022/prague-jun.html',
            isDesi: true
        },
        'vienna': {
            name: 'Vienna',
            date: 'May 2025',
            hook: 'Imperial coffee houses and waltz echoes.',
            url: 'posts/2025/vienna-may.html',
            isDesi: true
        },
        'florence': {
            name: 'Florence',
            date: 'Apr 2022',
            hook: 'Renaissance art and Tuscan light.',
            url: 'posts/2022/florence-apr.html',
            isDesi: false
        },
        'sozopol': {
            name: 'Sozopol',
            date: 'Jul 2025',
            hook: 'Black Sea whispers and ancient wooden houses.',
            url: 'posts/2025/sozopol-jul.html',
            isDesi: false
        },
        'malta': {
            name: 'Malta',
            date: 'Aug 2025',
            hook: 'Golden limestone and ancient temples.',
            url: 'posts/2025/malta-aug.html',
            isDesi: false
        },
        'goa': {
            name: 'Goa',
            date: 'Dec 2022',
            hook: 'The Desi soul: Spices, sun, and sand.',
            url: 'posts/2022/goa-dec.html',
            isDesi: true
        }
    };

    mapPins.forEach(pin => {
        pin.addEventListener('mouseenter', (e) => {
            const cityId = pin.getAttribute('data-city');
            const city = cities[cityId];
            if (!city) return;

            // Update Tooltip
            tooltip.innerHTML = `
                <h4>${city.name}</h4>
                <p class="meta">${city.date}</p>
                <p>${city.hook}</p>
            `;
            
            // Position Tooltip
            const rect = mapContainer.getBoundingClientRect();
            const pinRect = pin.getBoundingClientRect();
            
            tooltip.style.left = (pinRect.left - rect.left + 20) + 'px';
            tooltip.style.top = (pinRect.top - rect.top - 40) + 'px';
            tooltip.style.opacity = '1';
        });

        pin.addEventListener('mouseleave', () => {
            tooltip.style.opacity = '0';
        });

        pin.addEventListener('click', () => {
            const cityId = pin.getAttribute('data-city');
            const city = cities[cityId];
            if (city) window.location.href = city.url;
        });
    });

    // Desi Filter Logic
    desiToggle.addEventListener('change', () => {
        const isChecked = desiToggle.checked;
        
        mapPins.forEach(pin => {
            const cityId = pin.getAttribute('data-city');
            const city = cities[cityId];
            
            if (isChecked) {
                if (city.isDesi) {
                    pin.classList.add('desi-highlight');
                    const pulse = pin.querySelector('.pulse');
                    if (pulse) pulse.style.fill = 'var(--color-saffron)';
                    pin.style.opacity = '1';
                } else {
                    pin.style.opacity = '0.2';
                }
            } else {
                pin.classList.remove('desi-highlight');
                pin.style.opacity = '1';
                const pulse = pin.querySelector('.pulse');
                if (pulse) pulse.style.fill = 'var(--color-saffron)';
            }
        });
    });
});
