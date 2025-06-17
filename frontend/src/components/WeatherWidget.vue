<template>
  <div class="weather-widget">
    <input
      v-model="city"
      @keyup.enter="fetchWeather"
      placeholder="Ville"
      class="weather-input"
    />
    <button @click="fetchWeather" class="weather-btn">Rechercher</button>

    <div v-if="weather" class="weather-info">
      <h2>{{ weather.city }}</h2>
      <img :src="`http://openweathermap.org/img/wn/${weather.icon}@2x.png`" alt="icon" />
      <p>{{ weather.description }}</p>
      <p>{{ weather.temperature }}°C</p>
    </div>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  props: ['config'],
  data() {
    return {
      city: this.config.city || '',
      weather: null,
      error: ''
    }
  },
  mounted() {
    if (this.config.city) {
      this.city = this.config.city
      this.fetchWeather()
    }
  },
  methods: {
    async fetchWeather() {
      if (!this.city.trim()) return
      try {
        const res = await axios.get(`http://localhost:5000/api/weather?city=${this.city}`)
        this.weather = res.data
        this.config.city = this.city
        this.saveConfig()
      } catch (err) {
        this.error = 'Ville introuvable ou erreur réseau'
        this.weather = null
      }
    },
    saveConfig() {
      this.$emit('update')
    }
  }
}
</script>

<style scoped>
.weather-widget {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.weather-input {
  width: 100%;
  padding: 0.6rem;
  margin-bottom: 1rem;
  background: #1f1f1f;
  border: 1px solid #444;
  color: white;
  border-radius: 6px;
}
.weather-btn {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.5rem 1.2rem;
  border-radius: 6px;
  cursor: pointer;
  margin-bottom: 1rem;
  transition: background 0.2s ease;
}
.weather-btn:hover {
  background: #2980b9;
}
.weather-info {
  text-align: center;
  color: #ecf0f1;
}
.error {
  color: #e74c3c;
}
</style>