    // Advanced analytics widgets (real ML backend)
    document.addEventListener("DOMContentLoaded", function () {
        // Anomaly Detection Chart
        const anomalyCtx = document.getElementById("anomalyChart");
        if (anomalyCtx) {
            fetch("/api/analytics/anomaly", setAuthHeader())
                .then(r => r.json())
                .then(data => {
                    const chart = new Chart(anomalyCtx, {
                        type: "bar",
                        data: {
                            labels: data.dates,
                            datasets: [{
                                label: "Attacks",
                                data: data.attacks,
                                backgroundColor: data.dates.map((d, i) => data.anomalies.some(a => a.date === d) ? "#dc3545" : "#0dcaf0")
                            }]
                        },
                        options: {
                            plugins: { legend: { display: false } },
                            scales: { y: { beginAtZero: true, title: { display: true, text: "Attacks" } } }
                        }
                    });
                    if (data.anomalies.length > 0) {
                        document.getElementById("anomalySummary").textContent =
                            "Anomalies: " + data.anomalies.map(a => `${a.date} (${a.attacks})`).join(", ");
                    } else {
                        document.getElementById("anomalySummary").textContent = "No anomalies detected.";
                    }
                });
        }
        // Attack Trends Chart
        const trendCtx = document.getElementById("trendChart");
        if (trendCtx) {
            fetch("/api/analytics/trend", setAuthHeader())
                .then(r => r.json())
                .then(data => {
                    new Chart(trendCtx, {
                        type: "line",
                        data: {
                            labels: data.dates,
                            datasets: [
                                { label: "Attacks", data: data.attacks, borderColor: "#ffc107", backgroundColor: "rgba(255,193,7,0.2)", fill: true },
                                { label: "Trend (7d avg)", data: data.trend, borderColor: "#0d6efd", borderDash: [5,5], fill: false }
                            ]
                        },
                        options: { plugins: { legend: { display: true } } }
                    });
                });
        }
        // Predictive Analytics Chart
        const predCtx = document.getElementById("predictiveChart");
        if (predCtx) {
            fetch("/api/analytics/predict", setAuthHeader())
                .then(r => r.json())
                .then(data => {
                    new Chart(predCtx, {
                        type: "line",
                        data: {
                            labels: data.future_days,
                            datasets: [{
                                label: "Forecast",
                                data: data.forecast,
                                borderColor: "#0d6efd",
                                backgroundColor: "rgba(13,110,253,0.2)",
                                fill: true,
                                borderDash: [5, 5]
                            }]
                        },
                        options: { plugins: { legend: { display: true } } }
                    });
                });
        }
    });
    // Tampilkan signature/pola deteksi aktif
    fetch("/api/signatures", setAuthHeader()).then(r => r.json()).then(data => {
        const tbody = document.querySelector("#signatureTable tbody");
        tbody.innerHTML = "";
        data.forEach(sig => {
            const tr = document.createElement("tr");
            tr.innerHTML = `<td>${sig.name}</td><td><code>${sig.regex}</code></td><td>${sig.severity}</td>`;
            tbody.appendChild(tr);
        });
    });
// Utility functions for JWT Auth
function showLoginModal() {
    const modal = new bootstrap.Modal(document.getElementById('loginModal'));
    modal.show();
}

function isAuthenticated() {
    return !!localStorage.getItem('jwt_token');
}

function setAuthHeader(options = {}) {
    const token = localStorage.getItem('jwt_token');
    if (token) {
        options.headers = options.headers || {};
        options.headers['Authorization'] = 'Bearer ' + token;
    }
    return options;
}

document.addEventListener('DOMContentLoaded', function() {
    // JWT Auth: Show login modal if not authenticated
    if (!isAuthenticated()) {
        showLoginModal();
    }
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        let totpRequired = false;
        let lastLoginPayload = {};
        loginForm.onsubmit = async function(e) {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            let totp = document.getElementById('totp') ? document.getElementById('totp').value : undefined;
            let payload = { username, password };
            if (totp) payload.totp = totp;
            lastLoginPayload = payload;
            const resp = await fetch('/api/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (resp.status === 206) {
                // TOTP required, show TOTP input and QR code if provided
                const data = await resp.json();
                totpRequired = true;
                if (!document.getElementById('totp')) {
                    const totpDiv = document.createElement('div');
                    totpDiv.className = 'mb-3';
                    totpDiv.innerHTML = '<label for="totp" class="form-label">TOTP (Google Authenticator)</label>' +
                        '<input type="text" class="form-control" id="totp" required autocomplete="one-time-code">';
                    loginForm.insertBefore(totpDiv, loginForm.querySelector('button[type=submit]'));
                }
                if (data.totp_uri && !document.getElementById('totpQR')) {
                    const qrDiv = document.createElement('div');
                    qrDiv.className = 'mb-3';
                    qrDiv.id = 'totpQR';
                    const qrUrl = 'https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=' + encodeURIComponent(data.totp_uri);
                    qrDiv.innerHTML = '<label class="form-label">Scan QR di Authenticator:</label><br><img src="' + qrUrl + '" alt="TOTP QR">';
                    loginForm.insertBefore(qrDiv, loginForm.querySelector('button[type=submit]'));
                }
                document.getElementById('loginError').style.display = '';
                document.getElementById('loginError').textContent = 'Masukkan kode TOTP dari aplikasi Authenticator.';
            } else if (resp.ok) {
                const data = await resp.json();
                localStorage.setItem('jwt_token', data.access_token);
                bootstrap.Modal.getInstance(document.getElementById('loginModal')).hide();
                location.reload();
            } else {
                document.getElementById('loginError').style.display = '';
                document.getElementById('loginError').textContent = 'Login gagal. Cek username/password/TOTP.';
            }
        };
    }

    // Advanced analytics widgets (real ML backend)
    // ...existing code...

    // Tampilkan signature/pola deteksi aktif
    // ...existing code...

    // Pie chart jenis serangan
    const pieCtx = document.getElementById("attackTypeChart");
    if (pieCtx) {
        const pieChart = new Chart(pieCtx.getContext("2d"), {
            type: "pie",
            data: { labels: [], datasets: [{ data: [], backgroundColor: ["#ff6384", "#36a2eb", "#ffce56", "#4bc0c0", "#9966ff"] }] },
            options: { responsive: true, plugins: { legend: { position: "bottom" } } },
        });

        // Bar chart statistik serangan
        const barCtx = document.getElementById("attackStatChart");
        if (barCtx) {
            const barChart = new Chart(barCtx.getContext("2d"), {
                type: "bar",
                data: { labels: [], datasets: [{ label: "Serangan/jam", data: [], backgroundColor: "#36a2eb" }] },
                options: {
                    responsive: true,
                    plugins: { legend: { display: false } },
                    scales: { x: { title: { display: true, text: "Jam" } }, y: { title: { display: true, text: "Jumlah" }, beginAtZero: true } },
                },
            });

            // Fetch and update all dashboard data
            async function refreshDashboard() {
                // Pie chart: jenis serangan
                fetch("/api/attack_types", setAuthHeader()).then(r => r.json()).then(data => {
                    pieChart.data.labels = data.labels;
                    pieChart.data.datasets[0].data = data.data;
                    pieChart.update();
                });
                // Bar chart: statistik serangan
                fetch("/api/stats", setAuthHeader()).then(r => r.json()).then(data => {
                    barChart.data.labels = data.labels;
                    barChart.data.datasets[0].data = data.data;
                    barChart.update();
                });
                // Top IPs
                fetch("/api/top_ips", setAuthHeader()).then(r => r.json()).then(data => {
                    const topIpList = document.getElementById("topIpList");
                    topIpList.innerHTML = "";
                    data.forEach(([ip, count]) => {
                        const li = document.createElement("li");
                        li.textContent = `${ip} (${count}x)`;
                        topIpList.appendChild(li);
                    });
                });
                // Status
                fetch("/api/status", setAuthHeader()).then(r => r.json()).then(data => {
                    document.getElementById("statusSniffer").textContent = data.sniffer;
                    document.getElementById("statusIPS").textContent = data.ips;
                });
            }
            refreshDashboard();
            setInterval(refreshDashboard, 10000); // refresh tiap 10 detik

            // Unblock IP
            document.getElementById("unblockForm").onsubmit = async function (e) {
                e.preventDefault();
                const ip = document.getElementById("unblockIp").value;
                const fd = new FormData();
                fd.append("ip", ip);
                const resp = await fetch("/api/unblock_ip", setAuthHeader({ method: "POST", body: fd }));
                const data = await resp.json();
                alert(data.msg || (data.ok ? `IP ${ip} di-unblock` : "Gagal unblock"));
                document.getElementById("unblockIp").value = "";
            };

            // Config modal
            document.getElementById("editConfigBtn").onclick = async function () {
                document.getElementById("configModal").style.display = "block";
                // Fetch config.json
                const resp = await fetch("/api/config", setAuthHeader());
                if (resp.ok) {
                    const cfg = await resp.json();
                    document.getElementById("configTextarea").value = JSON.stringify(cfg, null, 2);
                } else {
                    document.getElementById("configTextarea").value = "Gagal load config.json";
                }
            };
            document.getElementById("closeConfigModal").onclick = function () {
                document.getElementById("configModal").style.display = "none";
            };
            document.getElementById("saveConfigBtn").onclick = async function () {
                const cfg = document.getElementById("configTextarea").value;
                const fd = new FormData();
                fd.append("cfg", cfg);
                const resp = await fetch("/api/config", setAuthHeader({ method: "POST", body: fd }));
                if (resp.ok) {
                    alert("Config disimpan");
                    document.getElementById("configModal").style.display = "none";
                } else {
                    const data = await resp.json();
                    alert("Gagal simpan config: " + (data.error || resp.status));
                }
            };
        }
    }
});
