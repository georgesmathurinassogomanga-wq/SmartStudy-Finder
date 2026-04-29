function renderSearchChart(data) {
    // Data attendu : [{label: "POO", value: 10}, ...]

    const ctx = document.getElementById("chart");

    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(d => d.label),
            datasets: [{
                label: 'Recherches',
                data: data.map(d => d.value)
            }]
        }
    });
}