<template>
  <div class="todo-widget">
    <input
      v-model="editableTitle"
      class="title-input"
      @blur="saveConfig"
      placeholder="Titre de la todo"
    />

    <input
      v-model="newTask"
      @keyup.enter="addTask"
      placeholder="Nouvelle tâche"
      class="task-input"
    />

    <ul class="task-list">
      <li
        v-for="(todo, index) in config.tasks"
        :key="todo.id"
        class="task-item"
      >
        <input
          type="checkbox"
          :checked="todo.done"
          @change="toggleDone(index)"
        />
        <span :class="{ done: todo.done }">{{ todo.text }}</span>
        <button @click="deleteTask(index)" class="delete-btn">✖</button>
      </li>
    </ul>
  </div>
</template>


<script>
import axios from 'axios'

export default {
  props: ['widget'],
  data() {
    return {
      newTask: '',
      editableTitle: '',
      config: {
        title: 'Ma Todo',
        tasks: []
      }
    }
  },
  computed: {
    sortedTasks() {
      return [...this.config.tasks].sort((a, b) => a.done - b.done)
    }
  },
  methods: {
    async saveConfig() {
      this.config.title = this.editableTitle
      try {
        await axios.put(`http://localhost:5000/api/widgets/${this.widget.id}`, this.config)
      } catch (e) {
        console.error('Erreur sauvegarde widget:', e)
      }
    },
    toggleDone(index) {
        this.config.tasks[index].done = !this.config.tasks[index].done
        // Réorganise la liste après changement
        this.config.tasks.sort((a, b) => a.done - b.done)
        this.saveConfig()
    },
    addTask() {
        if (!this.newTask.trim()) return
        this.config.tasks.push({
            id: Date.now() + Math.random(),
            text: this.newTask.trim(),
            done: false
        })
        this.newTask = ''
        this.saveConfig()
    },
    deleteTask(index) {
        this.config.tasks.splice(index, 1)
        this.saveConfig()
    },
    loadConfig() {
      if (this.widget.config && this.widget.config.tasks) {
        this.config = JSON.parse(JSON.stringify(this.widget.config))
        this.editableTitle = this.config.title || 'Ma Todo'
      } else {
        this.config = { title: 'Ma Todo', tasks: [] }
        this.editableTitle = this.config.title
        this.saveConfig()
      }
    }
  },
  mounted() {
    this.loadConfig()
  }
}
</script>

<style scoped>
.todo-widget {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.title-input {
  width: 100%;
  font-size: 1.2rem;
  font-weight: bold;
  text-align: center;
  color: #f0f0f0;
  background: transparent;
  border: none;
  border-bottom: 1px solid #555;
  margin-bottom: 1rem;
  padding-bottom: 0.3rem;
  outline: none;
}

.task-input {
  width: 100%;
  padding: 0.6rem;
  margin-bottom: 1rem;
  background: #1f1f1f;
  border: 1px solid #444;
  color: white;
  border-radius: 6px;
}

.task-list {
  width: 100%;
  list-style: none;
  padding: 0;
  margin: 0;
}

.task-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #333;
  padding: 0.5rem 1rem;
  margin-bottom: 0.6rem;
  border-radius: 6px;
  width: 100%;         /* ✅ S'assurer que l'élément occupe toute la largeur */
  box-sizing: border-box;
}

.task-item span {
  flex: 1;
  color: white;
  text-align: left;
  padding-left: 10px;
}

.task-item span.done {
  text-decoration: line-through;
  color: #aaa;
}

.delete-btn {
  background: transparent;
  border: none;
  color: #e74c3c;
  font-size: 1.1rem;
  cursor: pointer;
}
</style>
