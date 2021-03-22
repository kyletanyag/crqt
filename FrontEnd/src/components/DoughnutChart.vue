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

  mounted() {

    this.renderChart({
      datasets: [
        {
          labels: ["a","b","c"],
          data: this.data
        }
      ]
    })
  }
})
</script>
