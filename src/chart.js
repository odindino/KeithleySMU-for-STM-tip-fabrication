import Chart from "chart.js/auto";

export function createChart(ctx) {
  return new Chart(ctx, {
    type: "line",
    data: {
      labels: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
      datasets: [
        {
          label: "STM Probe Shape",
          data: [0, -0.2, -0.5, -1, -2, -3, -2, -1, -0.5, -0.2, 0],
          borderColor: "rgba(75, 192, 192, 1)",
          backgroundColor: "rgba(75, 192, 192, 0.2)",
          fill: false,
          tension: 0.4,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          title: {
            display: true,
            text: "Time",
          },
        },
        y: {
          title: {
            display: true,
            text: "Current (A)",
          },
          ticks: {
            callback: function (value) {
              return value.toExponential(2);
            },
          },
        },
      },
      plugins: {
        legend: {
          position: "top",
        },
        title: {
          display: true,
          text: "STM Probe Shape",
        },
      },
    },
  });
}