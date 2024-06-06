<template>
  <div class="settings-container">
    <div class="label">Set Voltage(V)</div>
    <div class="input-container">
      <div
        class="input-field"
        contenteditable="true"
        @input="updateVoltage"
        @keydown="handleKeydown"
      >
        {{ voltage }}
      </div>
      <div class="btn" @click="setVoltage">Set</div>
    </div>
    <div class="label">Compliance (mA)</div>
    <div class="input-container">
      <div
        class="input-field voltage"
        contenteditable="true"
        @input="updateCompliance"
        @keydown="handleKeydown"
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
</template>

<script>
export default {
  data() {
    return {
      voltage: 0,
      compliance: 10,
      updateTime: 1,
      isConnected: false,
    };
  },
  methods: {
    updateVoltage(event) {
      const inputValue = event.target.innerText;
      if (/^-?\d*\.?\d*$/.test(inputValue)) {
        this.voltage = inputValue;
      } else {
        event.target.innerText = this.voltage;
      }
    },
    updateCompliance(event) {
      const inputValue = event.target.innerText;
      if (/^-?\d*\.?\d*$/.test(inputValue)) {
        this.compliance = inputValue;
      } else {
        event.target.innerText = this.compliance;
      }
    },
    updateUpdateTime(event) {
      const inputValue = event.target.innerText;
      if (/^-?\d*\.?\d*$/.test(inputValue)) {
        this.updateTime = inputValue;
      } else {
        event.target.innerText = this.updateTime;
      }
    },
    handleKeydown(event) {
      if (event.key === "ArrowUp") {
        event.preventDefault();
        const value = parseFloat(event.target.innerText);
        event.target.innerText = (value + 0.1).toFixed(1);
        this.updateValue(event);
      } else if (event.key === "ArrowDown") {
        event.preventDefault();
        const value = parseFloat(event.target.innerText);
        event.target.innerText = (value - 0.1).toFixed(1);
        this.updateValue(event);
      }
    },
    updateValue(event) {
      const inputField = event.target.closest(".input-field");
      if (inputField.classList.contains("voltage")) {
        this.voltage = event.target.innerText;
      } else if (inputField.classList.contains("compliance")) {
        this.compliance = event.target.innerText;
      } else if (inputField.classList.contains("update-time")) {
        this.updateTime = event.target.innerText;
      }
    },
    async setVoltage() {
      await window.pywebview.api.set_voltage(this.voltage);
    },
    async setCompliance() {
      await window.pywebview.api.set_compliance(this.compliance);
    },
    async setUpdateTime() {
      await window.pywebview.api.set_update_time(this.updateTime);
    },
  },
};
</script>

<style scoped>
.input-field {
  width: 50%;
  padding: 8px;
  border: 1px solid #c5cae9;
  border-radius: 4px;
  font-size: 14px;
  flex: 1;
  outline: none;
}

.input-field:focus {
  border-color: #007bff;
}

.btn {
  width: 50%;
  padding: 8px 16px;
  background-color: #007bff;
  color: #fff;
  border-radius: 4px;
  cursor: pointer;
  user-select: none;
}

.btn:hover {
  background-color: #0056b3;
}
</style>
