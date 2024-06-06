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