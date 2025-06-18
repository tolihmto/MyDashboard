<template>
  <div class="todo-widget">
    <h2
      class="todo-title"
      contenteditable
      @blur="saveTitle"
      :data-placeholder="'Titre de la todo'"
      v-html="editableTitle || ''"
    ></h2>
    <input
      v-model="newTask"
      @keyup.enter="addTask"
      placeholder="Nouvelle tâche"
      class="task-input"
    />
    <ul class="task-list">
      <li
        v-for="todo in sortedTasks"
        :key="todo.id"
        class="task-item"
      >
        <input type="checkbox" v-model="todo.done" @change="saveConfig" />
        <span :class="{ done: todo.done }">{{ todo.text }}</span>
        <button @click="deleteTask(todo.id)" class="delete-btn">✖</button>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  props: ['config'],
  data() {
    return {
      newTask: '',
      editableTitle: this.config.title || ''
    }
  },
  computed: {
    sortedTasks() {
      return [...(this.config.tasks || [])].sort((a, b) => a.done - b.done)
    }
  },
  watch: {
    editableTitle(newTitle) {
      this.config.title = newTitle
      this.saveConfig()
    }
  },
  methods: {
    addTask() {
      if (!this.newTask.trim()) return
      this.config.tasks = this.config.tasks || []
      this.config.tasks.push({
        id: Date.now() + Math.random(),
        text: this.newTask.trim(),
        done: false
      })
      this.newTask = ''
      this.saveConfig()
    },
    onChange(index) {
      this.config.tasks[index].done = !this.config.tasks[index].done
      this.config.tasks.sort((a, b) => a.done - b.done)
      this.saveConfig()
    },
    deleteTask(id) {
      this.config.tasks = this.config.tasks.filter(t => t.id !== id)
      this.saveConfig()
    },
    saveConfig() {
      this.$emit('update')
    },
    saveTitle(event) {
      this.editableTitle = event.target.innerText.trim()
      this.config.title = this.editableTitle
      this.saveConfig()
    }
  }
}
</script>

<style scoped>
.todo-widget {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.todo-title {
  font-size: 1.4rem;
  font-weight: bold;
  color: white;
  text-align: center;
  margin-bottom: 1rem;
  outline: none;
  user-select: text;
  min-height: 1.5em;
  position: relative;

  white-space: normal; /* ✅ wrap automatiquement */
  word-break: break-word; /* ✅ coupe les très longs mots */
}


/* Pseudo-placeholder visible si vide */
.todo-title:empty:before {
  content: attr(data-placeholder);
  color: #888;
  position: absolute;
  left: 0;
  right: 0;
  text-align: center;
  pointer-events: none;
  white-space: nowrap;
}


.title-input,
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