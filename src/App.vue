<template>
  <div class="keithley2400">
    <div class="header">
      <h1>Keithley SMU for tip fabrication</h1>
    </div>
    <div class="upper-container">
      <SerialPortControls />
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
          <canvas ref="currentChart"></canvas>
        </div>
      </div>
      <div class="right-container">
        <div class="settings-actions-container">
          <MeasurementSettings />
          <MeasurementActions />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { createChart } from "./chart.js";
import SerialPortControls from "./SerialPortControls.vue";
import MeasurementSettings from "./MeasurementSettings.vue";
import MeasurementActions from "./MeasurementActions.vue";

export default {
  components: {
    SerialPortControls,
    MeasurementSettings,
    MeasurementActions,
  },
  setup() {
    let currentChart = ref(null);
    let currentTime = ref("");
    let currentValue = ref("8.88E-8");

    onMounted(() => {
      updateCurrentTime();
      setInterval(updateCurrentTime, 1000);

      const ctx = currentChart.value;
      createChart(ctx);
    });

    function updateCurrentTime() {
      currentTime.value = new Date().toLocaleString();
    }

    function updateCurrent(value) {
      currentValue.value = value;
    }

    window.updateCurrent = updateCurrent;

    return {
      currentChart,
      currentTime,
      currentValue,
    };
  },
};
</script>

<style src="./app.css"></style>
