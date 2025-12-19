// Dummy data untuk demo awal
window.onload = function() {
    // Grafik garis jumlah serangan
    var ctxLine = document.getElementById('attackLineChart').getContext('2d');
    new Chart(ctxLine, {
        type: 'line',
        data: {
            labels: ['10:00', '11:00', '12:00', '13:00', '14:00'],
            datasets: [{
                label: 'Jumlah Serangan',
                data: [2, 5, 3, 7, 4],
                borderColor: 'rgba(255,99,132,1)',

                document.addEventListener("DOMContentLoaded", function () {
                    // Pie chart jenis serangan
                    const pieCtx = document.getElementById("attackTypeChart").getContext("2d");
                    const pieChart = new Chart(pieCtx, {
                        type: "pie",
                        data: { labels: [], datasets: [{ data: [], backgroundColor: ["#ff6384", "#36a2eb", "#ffce56", "#4bc0c0", "#9966ff"] }] },
                        options: { responsive: true, plugins: { legend: { position: "bottom" } } },
                    });

                    // Bar chart statistik serangan
                    const barCtx = document.getElementById("attackStatChart").getContext("2d");
                    const barChart = new Chart(barCtx, {
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
                        fetch("/api/attack_types").then(r => r.json()).then(data => {
                            pieChart.data.labels = data.labels;
                            pieChart.data.datasets[0].data = data.data;
                            pieChart.update();
                        });
                        // Bar chart: statistik serangan
                        fetch("/api/stats").then(r => r.json()).then(data => {
                            barChart.data.labels = data.labels;
                            barChart.data.datasets[0].data = data.data;
                            barChart.update();
                        });
                        // Top IPs
                        fetch("/api/top_ips").then(r => r.json()).then(data => {
                            const topIpList = document.getElementById("topIpList");
                            topIpList.innerHTML = "";
                            data.forEach(([ip, count]) => {
                                const li = document.createElement("li");
                                li.textContent = `${ip} (${count}x)`;
                                topIpList.appendChild(li);
                            });
                        });
                        // Status
                        fetch("/api/status").then(r => r.json()).then(data => {
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
                        const resp = await fetch("/api/unblock_ip", { method: "POST", body: fd });
                        const data = await resp.json();
                        alert(data.msg || (data.ok ? `IP ${ip} di-unblock` : "Gagal unblock"));
                        document.getElementById("unblockIp").value = "";
                    };

                    // Config modal
                    document.getElementById("editConfigBtn").onclick = async function () {
                        document.getElementById("configModal").style.display = "block";
                        // Fetch config.json
                        const resp = await fetch("/api/config");
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
                        const resp = await fetch("/api/config", { method: "POST", body: fd });
                        if (resp.ok) {
                            alert("Config disimpan");
                            document.getElementById("configModal").style.display = "none";
                        } else {
                            const data = await resp.json();
                            alert("Gagal simpan config: " + (data.error || resp.status));
                        }
                    };
                });
