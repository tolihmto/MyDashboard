<template>
  <div class="widget" >
    <div class="widget-header">
        <button class="close-btn" @click="$emit('close')">✖</button>
    </div>
    <div class="widget-content">
      <component :is="getComponent()" :widget="widget" />
    </div>
  </div>
</template>

<script>
import TodoWidget from './TodoWidget.vue'
import CalculatorWidget from './CalculatorWidget.vue'
import WeatherWidget from './WeatherWidget.vue'

export default {
  props: ['widget'],
  components: { TodoWidget, CalculatorWidget, WeatherWidget},
  methods: {
    getComponent() {
      switch (this.widget.type) {
        case 'todo': return 'TodoWidget'
        case 'calculator': return 'CalculatorWidget'
        case 'weather': return 'WeatherWidget'
        default: return 'div'
      }
    }
  }
}
</script>

<style scoped>
.widget {
    position: relative;
    height: 100%;
    width: 100%;
    min-height: 160px;
    display: flex;
    flex-direction: column;
    background: #2b2b2b;
    padding: 2.5rem 1rem 1rem 1rem;
    border-radius: 10px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.2);
    font-size: 0.95rem;
}

.widget-header {
  position: absolute;
  top: 8px;
  right: 10px;
  padding: auto;
}

.close-btn {
  position: absolute;
  top: 0px;
  right: 0px;
  background: transparent;
  border: none;
  color: #c2c2c2;
  font-size: 1rem;
  cursor: pointer;
  z-index: 10;
}

.widget-content {
  margin-top: auto;
  margin-bottom: auto;
}
</style>
