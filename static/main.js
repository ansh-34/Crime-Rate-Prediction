function drawLineChart(canvasId, points, options) {
    var canvas = document.getElementById(canvasId);
    if (!canvas || !points || points.length === 0) return;

    var ctx = canvas.getContext("2d");
    var width = canvas.clientWidth;
    var height = canvas.height;
    canvas.width = width * window.devicePixelRatio;
    canvas.height = height * window.devicePixelRatio;
    ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
    ctx.clearRect(0, 0, width, height);

    var padding = { top: 24, right: 24, bottom: 44, left: 48 };
    var values = points.flatMap(function (point) {
        return options.keys.map(function (key) { return Number(point[key]); });
    });
    var minValue = Math.min.apply(null, values);
    var maxValue = Math.max.apply(null, values);
    var range = Math.max(maxValue - minValue, 1);
    var plotWidth = width - padding.left - padding.right;
    var plotHeight = height - padding.top - padding.bottom;

    function xAt(index) {
        return padding.left + (plotWidth * index) / Math.max(points.length - 1, 1);
    }

    function yAt(value) {
        return padding.top + plotHeight - ((value - minValue) / range) * plotHeight;
    }

    ctx.strokeStyle = "rgba(255,255,255,0.16)";
    ctx.lineWidth = 1;
    for (var i = 0; i <= 4; i++) {
        var y = padding.top + (plotHeight * i) / 4;
        ctx.beginPath();
        ctx.moveTo(padding.left, y);
        ctx.lineTo(width - padding.right, y);
        ctx.stroke();
    }

    options.keys.forEach(function (key, keyIndex) {
        ctx.strokeStyle = options.colors[keyIndex];
        ctx.lineWidth = 3;
        ctx.beginPath();
        points.forEach(function (point, index) {
            var x = xAt(index);
            var y = yAt(point[key]);
            if (index === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        });
        ctx.stroke();

        points.forEach(function (point, index) {
            ctx.beginPath();
            ctx.fillStyle = point.kind === "Forecast" ? "#ffc857" : options.colors[keyIndex];
            ctx.arc(xAt(index), yAt(point[key]), point.kind === "Forecast" ? 5 : 4, 0, Math.PI * 2);
            ctx.fill();
        });
    });

    ctx.fillStyle = "rgba(249,252,255,0.82)";
    ctx.font = "12px Outfit, sans-serif";
    points.forEach(function (point, index) {
        ctx.fillText(point.year, xAt(index) - 13, height - 18);
    });

    ctx.fillStyle = "rgba(200,217,234,0.9)";
    ctx.fillText(minValue.toFixed(1), 8, padding.top + plotHeight);
    ctx.fillText(maxValue.toFixed(1), 8, padding.top + 4);
}

function drawBarChart(canvasId, rows) {
    var canvas = document.getElementById(canvasId);
    if (!canvas || !rows || rows.length === 0) return;

    var ctx = canvas.getContext("2d");
    var width = canvas.clientWidth;
    var height = canvas.height;
    canvas.width = width * window.devicePixelRatio;
    canvas.height = height * window.devicePixelRatio;
    ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
    ctx.clearRect(0, 0, width, height);

    var topRows = rows.slice(0, 10).reverse();
    var maxRate = Math.max.apply(null, topRows.map(function (row) { return row.rate; }));
    var left = 92;
    var right = 28;
    var barHeight = 18;
    var gap = 11;
    var startY = 22;
    var plotWidth = width - left - right;

    ctx.font = "12px Outfit, sans-serif";
    topRows.forEach(function (row, index) {
        var y = startY + index * (barHeight + gap);
        var barWidth = (row.rate / Math.max(maxRate, 1)) * plotWidth;
        var gradient = ctx.createLinearGradient(left, 0, left + plotWidth, 0);
        gradient.addColorStop(0, "#00b6b3");
        gradient.addColorStop(1, "#ffc857");

        ctx.fillStyle = "rgba(249,252,255,0.82)";
        ctx.fillText(row.city, 0, y + 14);
        ctx.fillStyle = "rgba(255,255,255,0.12)";
        ctx.fillRect(left, y, plotWidth, barHeight);
        ctx.fillStyle = gradient;
        ctx.fillRect(left, y, barWidth, barHeight);
        ctx.fillStyle = "#f9fcff";
        ctx.fillText(row.rate.toFixed(2), left + Math.min(barWidth + 8, plotWidth - 34), y + 14);
    });
}

function renderDashboard() {
    if (!window.dashboardData) return;

    drawLineChart(
        "trendChart",
        window.dashboardData.history,
        { keys: ["rate"], colors: ["#00d7d2"] }
    );

    drawBarChart("cityChart", window.dashboardData.comparison);

    drawLineChart(
        "fitChart",
        window.dashboardData.actualVsPredicted,
        { keys: ["actual", "predicted"], colors: ["#ffc857", "#00d7d2"] }
    );
}

window.addEventListener("load", renderDashboard);
window.addEventListener("resize", renderDashboard);
