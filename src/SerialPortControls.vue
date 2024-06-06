<template>
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
</template>

<script setup>
import { ref, onMounted } from "vue";

const availablePorts = ref([]);
const selectedPort = ref("");
const isConnected = ref(false);

onMounted(async () => {
  await getAvailablePorts();
});

async function getAvailablePorts() {
  availablePorts.value = await window.pywebview.api.get_ports();
}

async function connect() {
  if (!selectedPort.value) return;
  const success = await window.pywebview.api.connect(selectedPort.value);
  if (success) {
    isConnected.value = true;
  }
}

async function disconnect() {
  const success = await window.pywebview.api.disconnect();
  if (success) {
    isConnected.value = false;
  }
}

async function refresh() {
  await getAvailablePorts();
}
</script>

<style scoped>
.connect-controls-container {
  display: flex;
  flex: auto;
  gap: 10px;
}

.com-port-container {
  display: flex;
  flex: auto;
  width: 120%;
}

.select-field {
  padding: 8px;
  border: 1px solid #c5cae9;
  border-radius: 4px;
  font-size: 14px;
  width: 100%;
  box-sizing: border-box;
}

.btn {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
  text-align: center;
  user-select: none;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: #eee;
}

.btn.disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
