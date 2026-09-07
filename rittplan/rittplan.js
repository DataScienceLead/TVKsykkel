(function () {
    'use strict';

    const weatherSummaries = {
        clearsky_day: 'Klar himmel',
        clearsky_night: 'Klar himmel',
        fair_day: 'Lettskyet',
        fair_night: 'Lettskyet',
        partlycloudy_day: 'Delvis skyet',
        partlycloudy_night: 'Delvis skyet',
        cloudy: 'Skyet',
        lightrain: 'Lett regn',
        rain: 'Regn',
        heavyrain: 'Kraftig regn',
        lightsleet: 'Lett sludd',
        sleet: 'Sludd',
        lightsnow: 'Lett snø',
        snow: 'Snø',
        fog: 'Tåke'
    };

    function googleDirectionsLink(destination, label = 'Google Maps') {
        const [lat, lng] = destination;
        const href = `https://www.google.com/maps/dir/?api=1&destination=${lat},${lng}&travelmode=driving`;
        return `<br><a href="${href}" target="_blank" rel="noopener">${label}</a>`;
    }

    function weatherSymbol(symbolCode) {
        if (!symbolCode) return '⛅';
        if (symbolCode.includes('thunder')) return '⛈️';
        if (symbolCode.includes('snow')) return '❄️';
        if (symbolCode.includes('rain')) return '🌧️';
        if (symbolCode.includes('sleet')) return '🌨️';
        if (symbolCode.includes('fog')) return '🌫️';
        if (symbolCode.includes('partlycloudy')) return '⛅';
        if (symbolCode.includes('cloudy')) return '☁️';
        if (symbolCode.includes('fair')) return '🌤️';
        if (symbolCode.includes('clearsky')) return '☀️';
        return '⛅';
    }

    function weatherSummary(symbolCode) {
        return weatherSummaries[symbolCode] || symbolCode?.replace(/_/g, ' ') || 'Værvarsel';
    }

    function buildMetForecastUrl(location) {
        const [lat, lng] = location.map((value) => Number(value.toFixed(4)));
        return `https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=${lat}&lon=${lng}`;
    }

    function pickForecastForTime(timeseries, targetTime) {
        const targetMs = new Date(targetTime).getTime();
        const closest = timeseries.reduce((best, entry) => {
            const distance = Math.abs(new Date(entry.time).getTime() - targetMs);
            return !best || distance < best.distance ? { entry, distance } : best;
        }, null);

        return closest && closest.distance <= 6 * 60 * 60 * 1000 ? closest.entry : null;
    }

    function formatForecastTime(value) {
        return new Intl.DateTimeFormat('nb-NO', {
            timeZone: 'Europe/Oslo',
            hour: '2-digit',
            minute: '2-digit'
        }).format(new Date(value));
    }

    function formatForecastDate(value) {
        return new Intl.DateTimeFormat('nb-NO', {
            timeZone: 'Europe/Oslo',
            day: 'numeric',
            month: 'long'
        }).format(new Date(value));
    }

    function unavailableWeatherCard(stage, message) {
        return `
            <div class="weather-card">
                <div class="weather-day">${stage.label}</div>
                <div class="weather-stage">${stage.stage}</div>
                <div class="weather-place">${stage.place}</div>
                <div class="weather-summary">${message}</div>
                ${stage.note ? `<div class="weather-note">${stage.note}</div>` : ''}
            </div>
        `;
    }

    function weatherCard(stage, entry) {
        const details = entry.data.instant.details;
        const nextHours = entry.data.next_6_hours || entry.data.next_1_hours || entry.data.next_12_hours || {};
        const symbolCode = nextHours.summary?.symbol_code || '';
        const precipitation = nextHours.details?.precipitation_amount;

        return `
            <div class="weather-card">
                <div class="weather-card-top">
                    <div>
                        <div class="weather-day">${stage.label}</div>
                        <div class="weather-stage">${stage.stage}</div>
                    </div>
                    <div class="weather-symbol" aria-hidden="true">${weatherSymbol(symbolCode)}</div>
                </div>
                <div class="weather-place">${stage.place}</div>
                <div class="weather-temp">${Math.round(details.air_temperature)}°</div>
                <div class="weather-summary">${weatherSummary(symbolCode)}</div>
                <div class="weather-meta">
                    <div>Prognosepunkt: ${formatForecastTime(entry.time)}</div>
                    <div>Vind: ${details.wind_speed.toFixed(1)} m/s</div>
                    <div>Nedbør: ${typeof precipitation === 'number' ? precipitation.toFixed(1) : '0.0'} mm</div>
                    <div>Skydekke: ${Math.round(details.cloud_area_fraction)} %</div>
                </div>
                ${stage.note ? `<div class="weather-note">${stage.note}</div>` : ''}
            </div>
        `;
    }

    async function loadWeatherForecast(options) {
        const {
            stages,
            statusId = 'weatherStatus',
            gridId = 'weatherGrid',
            messages = {}
        } = options;
        const weatherStatus = document.getElementById(statusId);
        const weatherGrid = document.getElementById(gridId);
        const forecastByLocation = new Map();
        const uniqueLocations = [...new Map(
            stages.map((stage) => [stage.location.join(','), stage.location])
        ).entries()];

        const results = await Promise.allSettled(uniqueLocations.map(async ([key, location]) => {
            const response = await fetch(buildMetForecastUrl(location), {
                headers: { Accept: 'application/json' }
            });
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            const forecast = await response.json();
            return [key, forecast?.properties?.timeseries || []];
        }));

        results.forEach((result) => {
            if (result.status === 'fulfilled') forecastByLocation.set(...result.value);
        });

        weatherGrid.innerHTML = stages.map((stage) => {
            const timeseries = forecastByLocation.get(stage.location.join(','));
            if (!timeseries?.length) {
                return unavailableWeatherCard(stage, 'Ingen automatisk prognose tilgjengelig akkurat nå.');
            }
            const entry = pickForecastForTime(timeseries, stage.targetTime);
            return entry
                ? weatherCard(stage, entry)
                : unavailableWeatherCard(stage, 'Det finnes ennå ikke et nært prognosepunkt for denne starttiden.');
        }).join('');

        const availableTimeseries = [...forecastByLocation.values()].filter((timeseries) => timeseries.length);
        const maxAvailableTime = availableTimeseries.length
            ? Math.max(...availableTimeseries.map((timeseries) => new Date(timeseries[timeseries.length - 1].time).getTime()))
            : null;
        const missingAllStagePoints = stages.every((stage) => (
            !pickForecastForTime(forecastByLocation.get(stage.location.join(',')) || [], stage.targetTime)
        ));

        if (forecastByLocation.size === 0) {
            weatherStatus.innerHTML = messages.failed || 'Kunne ikke laste værdata automatisk.';
        } else if (missingAllStagePoints && maxAvailableTime && messages.outOfRange) {
            weatherStatus.innerHTML = messages.outOfRange(formatForecastDate(maxAvailableTime));
        } else if (forecastByLocation.size < uniqueLocations.length) {
            weatherStatus.innerHTML = messages.partial || 'Værdata ble bare delvis oppdatert.';
        } else {
            weatherStatus.innerHTML = messages.complete || 'Værprognosene er oppdatert.';
        }
    }

    window.Rittplan = {
        googleDirectionsLink,
        loadWeatherForecast
    };
}());