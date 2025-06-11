<template>
  <div class="todo-widget">
    <input v-model="newTask" @keyup.enter="addTask" placeholder="Nouvelle tâche" class="task-input" />
    <ul class="task-list">
      <li v-for="todo in sortedTodos" :key="todo.id" class="task-item">
        <input type="checkbox" v-model="todo.done" @change="updateTask(todo)" />
        <span :class="{ done: todo.done }">{{ todo.text }}</span>
        <button @click="deleteTask(todo.id)" class="delete-btn">✖</button>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios'
import bus from '../eventBus'

export default {
  data() {
    return {
      todos: [],
      newTask: ''
    }
  },
  computed: {
    sortedTodos() {
      return [...this.todos].sort((a, b) => a.done - b.done)
    }
  },
  methods: {
    async fetchTodos() {
      const res = await axios.get('http://localhost:5000/api/todos')
      this.todos = res.data
    },
    async addTask() {
      if (!this.newTask.trim()) return
      await axios.post('http://localhost:5000/api/todos', { text: this.newTask })
      this.newTask = ''
      bus.emit('refresh-todos')
    },
    async updateTask(todo) {
      await axios.put(`http://localhost:5000/api/todos/${todo.id}`, todo)
      bus.emit('refresh-todos')
    },
    async deleteTask(id) {
      await axios.delete(`http://localhost:5000/api/todos/${id}`)
      bus.emit('refresh-todos')
    }
  },
  mounted() {
    this.fetchTodos()
    bus.on('refresh-todos', this.fetchTodos)
  },
  beforeUnmount() {
    bus.off('refresh-todos', this.fetchTodos)
  }
}
</script>

<style scoped>
.todo-widget {
  display: flex;
  flex-direction: column;
  align-items: center;
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
}

.task-item input[type='checkbox'] {
  margin-right: 0.8rem;
  accent-color: #3498db;
}

.task-item span {
  flex: 1;
  color: white;
  text-align: left;
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
