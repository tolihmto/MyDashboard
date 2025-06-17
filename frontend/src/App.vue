<template>
  <div class="app">
    <nav class="navbar">
      <h1>Mon Dashboard</h1>
      <select v-model="selectedWidget" @change="addWidget">
        <option disabled value="">Ajouter un widget...</option>
        <option value="todo">Todo List</option>
        <option value="calculator">Calculatrice</option>
        <option value="weather">Météo</option>
      </select>
    </nav>

    <draggable
      v-model="widgets"
      class="dashboard"
      item-key="id"
      :animation="200"
      ghost-class="ghost"
      @end="onDragEnd"
    >
      <template #item="{ element }">
        <div :key="element.id">
          <DashboardWidget
            :widget="element"
            @close="removeWidget(element.id)"
            @update="saveWidgets"
          />
        </div>
      </template>
    </draggable>
  </div>
</template>

<script>
import draggable from 'vuedraggable'
import DashboardWidget from './components/DashboardWidget.vue'
import axios from 'axios'

export default {
  components: { draggable, DashboardWidget },
  data() {
    return {
      selectedWidget: '',
      widgets: []
    }
  },
  methods: {
    async loadWidgets() {
      const res = await axios.get('http://localhost:5000/api/widgets')
      this.widgets = res.data
    },
    async saveWidgets() {
      await axios.post('http://localhost:5000/api/widgets', this.widgets)
    },
    async addWidget() {
      if (!this.selectedWidget) return
      this.widgets.push({
        id: Date.now(),
        type: this.selectedWidget,
        config: {}
      })
      this.selectedWidget = ''
      this.saveWidgets()
    },
    async removeWidget(id) {
      this.widgets = this.widgets.filter(w => w.id !== id)
      this.saveWidgets()
    },
    onDragEnd() {
      this.saveWidgets()
    }
  },
  watch: {
    widgets: {
      handler() {
        this.saveWidgets()
      },
      deep: true
    }
  },
  mounted() {
    this.loadWidgets()
  }
}
</script>

<style scoped>
.app {
  min-height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  font-family: sans-serif;
  background-color: #1e1e1e;
  color: white;
}

.navbar {
  background: #121212;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #2e2e2e;
}

.navbar select {
  background: #2e2e2e;
  color: white;
  border: none;
  padding: 0.4rem 0.6rem;
  border-radius: 5px;
}

.dashboard {
  flex: 1;
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  padding: 2rem;
  justify-content: center;
  align-content: start;
  overflow-y: auto;
}




.ghost {
  opacity: 0.5;
}
</style>
