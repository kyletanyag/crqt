<script>
/*global d3*/
/*eslint no-undef: "error"*/
import { defineComponent } from 'vue'
import { Bar } from 'vue3-chart-v2'


export default defineComponent({
  name: 'Histogram',
  extends: Bar,

  options: {
    responsive: true,
    maintainAspectRatio: true
  },

  props: {
    data: Array,
    numBins: Number,
    name: String,
    barColor: String
  },

  mounted() {

    var histGenerator = d3.histogram();
    histGenerator.domain([0,1]); // Every histogram in this project should range from 0-1, so I've hard-coded it.
    histGenerator.thresholds(this.numBins-1);
    var binnedData = histGenerator(this.data);
    var binSizes = new Array(this.numBins);
    for (var i = 0; i < this.numBins; i++){
      binSizes[i] = binnedData[i].length;
    }
    console.log(binSizes);
    this.renderChart({
      //labels: new Array(this.data.length),
      labels: ["0.1","0.2","0.3","0.4","0.5","0.6","0.7","0.8","0.9","1.0"],
      datasets: [
        {
          label: this.name,
          backgroundColor: this.barColor,
          data: binSizes
        }
      ]
    })
  }
})
</script>
