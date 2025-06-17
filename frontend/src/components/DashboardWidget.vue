<template>
  <div
    class="widget"
    :style="widgetStyle"
    ref="widget"
    @mousedown="startResize"
  >
    <div class="widget-header">
      <button class="close-btn" @click="$emit('close')">✖</button>
    </div>
    <div class="widget-content">
      <component
        :is="getComponent()"
        :config="widget.config"
        @update="$emit('update')"
      />
    </div>
    <div class="resize-handle" @mousedown.stop.prevent="initManualResize" />
  </div>
</template>

<script>
import TodoWidget from './TodoWidget.vue'
import CalculatorWidget from './CalculatorWidget.vue'
import WeatherWidget from './WeatherWidget.vue'

export default {
  props: ['widget'],
  components: {
    TodoWidget,
    CalculatorWidget,
    WeatherWidget
  },
  data() {
    return {
      resizeObserver: null,
      resizing: false,
      startX: 0,
      startY: 0,
      startWidth: 0,
      startHeight: 0
    }
  },
  computed: {
    widgetStyle() {
      return {
        width: this.widget?.config?.width || '350px',
        height: this.widget?.config?.height || '300px'
      }
    }
  },
  methods: {
    getComponent() {
      switch (this.widget.type) {
        case 'todo': return 'TodoWidget'
        case 'calculator': return 'CalculatorWidget'
        case 'weather': return 'WeatherWidget'
        default: return 'div'
      }
    },
    initResizeObserver() {
      this.resizeObserver = new ResizeObserver(() => {
        const el = this.$refs.widget
        if (!this.widget?.config) return

        const newWidth = `${el.offsetWidth}px`
        const newHeight = `${el.offsetHeight}px`

        if (
          this.widget.config.width !== newWidth ||
          this.widget.config.height !== newHeight
        ) {
          this.widget.config.width = newWidth
          this.widget.config.height = newHeight
          this.$emit('update') // Sauvegarde à chaque changement
        }
      })
      this.resizeObserver.observe(this.$refs.widget)
    },
    initManualResize(e) {
      this.resizing = true
      const el = this.$refs.widget
      this.startX = e.clientX
      this.startY = e.clientY
      this.startWidth = el.offsetWidth
      this.startHeight = el.offsetHeight

      window.addEventListener('mousemove', this.performResize)
      window.addEventListener('mouseup', this.stopResize)
    },
    performResize(e) {
      if (!this.resizing) return
      const el = this.$refs.widget

      const newWidth = this.startWidth + (e.clientX - this.startX)
      const newHeight = this.startHeight + (e.clientY - this.startY)

      el.style.width = `${newWidth}px`
      el.style.height = `${newHeight}px`

      // Ajout : mettre à jour config et sauvegarder
      this.widget.config.width = `${newWidth}px`
      this.widget.config.height = `${newHeight}px`
      this.$emit('update')
    },
    stopResize() {
      this.resizing = false
      window.removeEventListener('mousemove', this.performResize)
      window.removeEventListener('mouseup', this.stopResize)

      const el = this.$refs.widget
      this.widget.config.width = `${el.offsetWidth}px`
      this.widget.config.height = `${el.offsetHeight}px`
      this.$emit('update')
    }
  },
  mounted() {
    this.initResizeObserver()
  },
  beforeUnmount() {
    if (this.resizeObserver) this.resizeObserver.disconnect()
  }
}
</script>

<style scoped>
.widget {
  position: relative;
  background: #2b2b2b;
  color: #fff;
  border-radius: 12px;
  padding: 2rem 1rem 1rem 1rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  resize: none; /* Désactive resize CSS par défaut */
}

.widget-header {
  position: absolute;
  top: 8px;
  right: 10px;
}

.close-btn {
  background: transparent;
  border: none;
  color: #c2c2c2;
  font-size: 1rem;
  cursor: pointer;
}

.widget-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

/* Resize handle visuel */
.resize-handle {
  width: 16px;
  height: 16px;
  background: transparent;
  position: absolute;
  right: 2px;
  bottom: 2px;
  cursor: nwse-resize;
  z-index: 10;
}
</style>
