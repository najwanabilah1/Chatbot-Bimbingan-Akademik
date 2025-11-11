document.addEventListener("DOMContentLoaded", async () => {
  try {
    const res = await fetch("http://127.0.0.1:5000/api/admin/stats");
    const data = await res.json();

    const visitorLabels = (data.daily_visits || []).map(d => d.tanggal);
    const visitorCounts = (data.daily_visits || []).map(d => d.jumlah);

    const questionLabels = (data.daily_questions || []).map(d => d.tanggal);
    const questionCounts = (data.daily_questions || []).map(d => d.jumlah);

    const datasetCount = data.total_dataset || 0;
    const topQuestions = data.top_questions || [
      { label: 'A', value: 30 }, { label: 'B', value: 20 }
    ];

    const commonOptions = {
      responsive: true,
      maintainAspectRatio: false, // biar fleksibel
      animation: { duration: 1200, easing: 'easeOutQuart' },
      plugins: { legend: { display: true, position: 'top' } }
    };

    // Visitors Line Chart
    new Chart(document.getElementById("chartVisitors"), {
      type: "line",
      data: {
        labels: visitorLabels,
        datasets: [{
          label: "Kunjungan",
          data: visitorCounts,
          borderColor: "#0a1b9f",
          backgroundColor: "rgba(10,27,159,0.2)",
          fill: true,
          tension: 0.4,
          pointRadius: 5,
          pointBackgroundColor: '#2563eb'
        }]
      },
      options: commonOptions
    });

    // Questions Bar Chart dengan gradient
    const ctxBar = document.getElementById("chartQuestions").getContext('2d');
    const gradientBar = ctxBar.createLinearGradient(0,0,0,300);
    gradientBar.addColorStop(0,'#2563eb');
    gradientBar.addColorStop(1,'#0a1b9f');
    new Chart(ctxBar, {
      type: "bar",
      data: {
        labels: questionLabels,
        datasets: [{
          label: "Jumlah Pertanyaan",
          data: questionCounts,
          backgroundColor: gradientBar,
          borderRadius: 10
        }]
      },
      options: commonOptions
    });

    // Dataset Doughnut
    new Chart(document.getElementById("chartDataset"), {
      type: "doughnut",
      data: {
        labels: ["Dataset Tersedia", "Kosong"],
        datasets: [{
          data:[datasetCount, Math.max(100-datasetCount,0)],
          backgroundColor:["#0a1b9f","#cbd5e1"],
          hoverOffset:10
        }]
      },
      options: commonOptions
    });

    // Top Questions Pie
    new Chart(document.getElementById("chartTopQuestions"), {
      type: "pie",
      data: {
        labels: topQuestions.map(t => t.label),
        datasets: [{
          data: topQuestions.map(t => t.value),
          backgroundColor:['#0a1b9f','#2563eb','#60a5fa','#93c5fd','#bfdbfe'],
          hoverOffset:8
        }]
      },
      options: commonOptions
    });

  } catch (err) {
    console.error("Gagal memuat data statistik:", err);
  }
});