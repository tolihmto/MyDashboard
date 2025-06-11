<template>
  <div class="calc-widget">
    <input
      v-model="expression"
      @keyup.enter="calculate"
      placeholder="Ex : 3,5 * (2 + 1)"
      class="calc-input"
    />
    <button class="calc-btn" @click="calculate">Calculer</button>
    <p class="calc-result">Résultat : {{ result }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      expression: '',
      result: ''
    }
  },
  methods: {
    calculate() {
      try {
        // Remplace les virgules par des points pour supporter les décimales
        const safeExpr = this.expression.replace(/,/g, '.')
        const evalResult = eval(safeExpr)

        // Si le résultat est un float, arrondi à 6 chiffres max
        this.result = Number.isFinite(evalResult)
          ? Number(evalResult.toFixed(6))
          : 'Erreur'
      } catch {
        this.result = 'Erreur'
      }
    }
  }
}
</script>

<style scoped>
.calc-widget {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.calc-input {
  width: 100%;
  padding: 0.6rem;
  background: #1f1f1f;
  border: 1px solid #444;
  color: white;
  border-radius: 6px;
  margin-bottom: 1rem;
}

.calc-btn {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.5rem 1.2rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  margin-bottom: 1rem;
  transition: background 0.2s ease;
}
.calc-btn:hover {
  background: #2980b9;
}

.calc-result {
  color: #ecf0f1;
  font-size: 1.1rem;
}
</style>
