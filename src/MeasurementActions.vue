<template>
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
</template>

<script>
export default {
  data() {
    return {
      isConnected: false,
      isRunning: false,
      isPaused: false,
    };
  },
  methods: {
    async start() {
      if (!this.isConnected || this.isRunning) return;
      this.isRunning = true;
      await window.pywebview.api.start_measurement();
      this.isPaused = false;
    },
    async pause() {
      if (!this.isRunning) return;
      this.isRunning = false;
      this.isPaused = true;
      await window.pywebview.api.pause_measurement();
    },
    async stop() {
      if (!this.isRunning) return;
      this.isRunning = false;
      this.isPaused = false;
      await window.pywebview.api.stop_measurement();
    },
  },
};
</script>

<style scoped>
.actions-container {
  display: flex;
  padding-right: 10px;
  gap: 10px;
}
.btn {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
  background-color: #007bff;
  color: #fff;
  cursor: pointer;
  transition: background-color 0.3s;
  text-align: center;
  user-select: none;
}

.btn:hover {
  background-color: #0056b3;
}

.btn.disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
