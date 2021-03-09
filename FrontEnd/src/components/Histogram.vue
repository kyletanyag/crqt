<script>
import { defineComponent } from 'vue'
import { Bar } from 'vue3-chart-v2'

export default defineComponent({
  name: 'Histogram',
  extends: Bar,
  mounted() {
    // Overwriting base render method with actual data.
    this.renderChart({
      labels: ['Bin1,','Bin2','Bin3','etc'],
      datasets: [
        {
          label: 'Dataset Label',
          backgroundColor: '#f87979',
          data: [1,2,3,9]
        }
      ]
    })
  }
})
</script>
