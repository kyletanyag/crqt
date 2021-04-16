<script>
import { defineComponent } from 'vue'
//import { Chart } from 'vue3-chart-v2'
import { Bar } from 'vue3-chart-v2'

export default defineComponent({
    name: 'HistogramAndLine',
    mixins: [Bar],
    data: function () {
        return {
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        }
    },
    mounted () {
        this.renderChart({
            labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
            datasets: [
            {
                type: 'bar',
                label: 'Bar Component',
                data: [10, 20, 30],
            },
            {
                type: 'line',
                label: 'Line Component',
                data: [30, 20, 10],
            }
        ]
        }, this.options)
    }
})
</script>

