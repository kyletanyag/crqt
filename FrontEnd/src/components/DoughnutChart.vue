<script>
import { defineComponent } from 'vue'
import { Doughnut } from 'vue3-chart-v2'


export default defineComponent({
  name: 'DoughnutChart',
  extends: Doughnut,

  props: {
    data: Array,
    name: String,
    labels: Array
  },

  options: {
    responsive: true,
    maintainAspectRatio: true
  },

  mounted() {
    this.renderChart({
      datasets: [
        {
          data: this.data,
          label: this.name,
          backgroundColor: [  // add more background colors !!!
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)',
            'rgb(255, 205, 86)'
          ],
        }
      ],

      labels: this.labels,
    })
  }
})
</script>
