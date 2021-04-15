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
            'rgb(255, 0, 0)',
            'rgb(0, 0, 255)',
            'rgb(242, 117, 0)',
            'rgb(204, 0, 255)',
            'rgb(255, 242, 0)',
            'rgb(3, 206, 237)',
            'rgb(255, 0, 162)',
            'rgb(0, 255, 0)'


          ],
        }
      ],

      labels: this.labels,
    })
  }
})
</script>
