<template>
  <div class="keithley2400">
    <div class="header">
      <h1>Keithley SMU for tip fabrication</h1>
    </div>
    <div class="upper-container">
      <div class="connect-controls-container">
        <div class="com-port-container">
          <select id="com-port-select" class="select-field" v-model="selectedPort">
            <option value="">Select a COM port</option>
            <option v-for="port in availablePorts" :key="port" :value="port">
              {{ port }}
            </option>
          </select>
        </div>
        <div @click="connect" :class="['btn', { disabled: isConnected }]">
          Connect
        </div>
        <div @click="disconnect" :class="['btn', { disabled: !isConnected }]">
          Disconnect
        </div>
        <div class="btn" @click="refresh">Refresh</div>
      </div>
      <div class="info-container">
        <div class="time-container">
          <label>Time:</label>
          <span>{{ currentTime }}</span>
        </div>
        <div class="current-container">
          <label>Current:</label>
          <span>{{ currentValue }} A</span>
        </div>
      </div>
    </div>
    <div class="main-container">
      <div class="center-container">
        <div class="chart-container">
          <div class="chart-container">
            <canvas ref="currentChart"></canvas>
          </div>
        </div>
      </div>
      <div class="right-container">
        <div class="settings-actions-container">
          <div class="settings-container">
            <div class="label">Set Voltage(V)</div>
            <div class="input-container">
              <div
                class="input-field"
                contenteditable="true"
                @input="updateVoltage"
                @keydown.enter="handleEnterKeyVoltage"
                @keydown="handleKeydown"
                @blur="formatVoltage"
                @paste="handlePaste"
                :style="{ width: (voltage.toString().length + 1) + 'ch' }"
              >
                {{ voltage }}
              </div>

              <div class="btn" @click="setVoltage">Set</div>
            </div>
            <div class="label">Compliance (mA)</div>
            <div class="input-container">
              <div
                class="input-field"
                contenteditable="true"
                @input="updateCompliance"
                @keydown.enter="handleEnterKeyCompliance"
                @keydown="handleKeydown"
                @blur="formatCompliance"
                @paste="handlePaste"
                :style="{ width: (compliance.toString().length + 1) + 'ch' }"
              >
                {{ compliance }}
              </div>
              <div class="btn" @click="setCompliance">Set</div>
            </div>
            <div class="label">Update Time(s)</div>
            <div class="input-container">
              <div
                class="input-field"
                contenteditable="true"
                @input="updateUpdateTime"
                @keydown="handleKeydown"
              >
                {{ updateTime }}
              </div>
              <div class="btn" @click="setUpdateTime">Set</div>
            </div>
          </div>
          <div class="actions-container">
            <div
              @click="start"
              :class="['btn', { disabled: !isConnected || isRunning }]"
            >
              Start
            </div>
            <div @click="pause" :class="['btn', { disabled: !isRunning }]">Pause</div>
            <div @click="stop" :class="['btn', { disabled: !isRunning }]">Stop</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import Chart from "chart.js/auto";

let availablePorts = ref([]);
let selectedPort = ref("");
let isConnected = ref(false);
let isRunning = ref(false);
let isPaused = ref(false);
let voltage = ref(0);
let compliance = ref(10);
let currentChart = ref(null);
let chartData = {
  labels: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
  datasets: [
    {
      label: "Current (A)",
      data: [0, -0.2, -0.5, -1, -2, -3, -2, -1, -0.5, -0.2, 0],
      borderColor: "rgba(75, 192, 192, 1)",
      backgroundColor: "rgba(75, 192, 192, 0.2)",
      fill: false,
      tension: 0.4,
    },
  ],
};
let chart = null;
let currentTime = ref("");
let currentValue = ref('');

onMounted(() => {
  setTimeout(() => {
    window.pywebview.api
      .get_ports()
      .then((response) => {
        availablePorts.value = response;
      })
      .catch((error) => {
        console.error("Error getting COM ports:", error);
      });
  }, 1000);
  updateCurrentTime();
  setInterval(updateCurrentTime, 1000);

  const ctx = currentChart.value;
  chart = new Chart(ctx, {
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
});
function updateCurrentTime() {
  currentTime.value = new Date().toLocaleString();
}

function handleKeydown(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    return;
  }
  if (event.key === "ArrowUp") {
    event.preventDefault();
    const value = parseFloat(event.target.innerText);
    event.target.innerText = (value + 0.1).toFixed(1);
    updateValue(event);
  } else if (event.key === "ArrowDown") {
    event.preventDefault();
    const value = parseFloat(event.target.innerText);
    event.target.innerText = (value - 0.1).toFixed(1);
    updateValue(event);
  }
}

function handleEnterKey(event) {
  event.preventDefault();
  const inputValue = event.target.innerText;
  if (/^-?\d*\.?\d*$/.test(inputValue)) {
    voltage.value = parseFloat(inputValue);
  } else {
    voltage.value = NaN;
  }
  event.target.blur();
}

async function connect() {
  console.log("Connecting to port:", selectedPort.value);
  const success = await window.pywebview.api.connect(selectedPort.value);
  console.log("Connection success:", success);
  if (success) {
    isConnected.value = true;
  }
}

async function disconnect() {
  const success = await window.pywebview.api.disconnect();
  if (success) {
    isConnected.value = false;
    isRunning.value = false;
  }
}

function updateVoltage(event) {
  const inputValue = event.target.innerText;
  if (inputValue === '') {
    voltage.value = '';
  }
}

async function setVoltage() {
  await window.pywebview.api.set_voltage(voltage.value);
}

function updateCompliance(event) {
  const inputValue = event.target.innerText;
  if (inputValue === '') {
    compliance.value = '';
  }
}

async function setCompliance() {
  await window.pywebview.api.set_compliance(compliance.value);
}

function handleEnterKeyVoltage(event) {
  event.preventDefault();
  const inputValue = event.target.innerText;
  if (/^-?\d*\.?\d*$/.test(inputValue)) {
    voltage.value = parseFloat(inputValue);
  } else {
    voltage.value = NaN;
  }
  event.target.blur();
}

function handleEnterKeyCompliance(event) {
  event.preventDefault();
  const inputValue = event.target.innerText;
  if (/^-?\d*\.?\d*$/.test(inputValue)) {
    compliance.value = parseFloat(inputValue);
  } else {
    compliance.value = NaN;
  }
  event.target.blur();
}

function formatVoltage(event) {
  const value = event.target.innerText;
  if (value === '') {
    voltage.value = '';
  } else if (/^-?\d*\.?\d*$/.test(value)) {
    voltage.value = parseFloat(value);
  } else {
    voltage.value = NaN;
  }
  event.target.innerText = voltage.value.toString();
}

function formatCompliance(event) {
  const value = event.target.innerText;
  if (value === '') {
    compliance.value = '';
  } else if (/^-?\d*\.?\d*$/.test(value)) {
    compliance.value = parseFloat(value);
  } else {
    compliance.value = NaN;
  }
  event.target.innerText = compliance.value.toString();
}

async function start() {
  isRunning.value = true;
  await window.pywebview.api.start_measurement();

  if (!chart) {
    const ctx = currentChart.value;
    chart = new Chart(ctx, {
      type: "line",
      data: chartData,
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
              callback: function (value, index, values) {
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
            text: "Real-time Current",
          },
        },
      },
    });
  } else if (!isPaused.value) {
    chart.data.labels = [];
    chart.data.datasets[0].data = [];
    chart.update();
  }
  
  isPaused.value = false;
}

async function pause() {
  isRunning.value = false;
  isPaused.value = true;
  await window.pywebview.api.pause_measurement();
}

async function stop() {
  isRunning.value = false;
  isPaused.value = false;
  await window.pywebview.api.stop_measurement();
}

function updateCurrent(value) {
  if (isRunning.value && chart) {
    const parsedValue = parseFloat(value);
    currentValue.value = parsedValue.toString();
    chart.data.labels.push(new Date().toLocaleTimeString());
    chart.data.datasets[0].data.push(parsedValue);
    chart.update();
  }
}

window.updateCurrent = updateCurrent;
</script>

<style src="./app.css"></style>