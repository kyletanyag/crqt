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
    binNames: {
      type: Array(),
      default: ['automatic']
    },
    numBins: String, //Vue was giving me an error in SimulationResults.vue, saying that it expected a number but I was passing a string.
    name: String,
    barColor: String
  },

  watch: {
    name() {
      this.state.chartObj.destroy()
      this.renderHistogram();
    }
  },

  methods: {
    renderHistogram() {

      // Bin the data
      var histGenerator = d3.histogram();
      histGenerator.domain([0,1]); // Every histogram in this project should range from 0-1, so I've hard-coded it.
      histGenerator.thresholds(this.numBins-1);
      var binnedData = histGenerator(this.data);
      var binSizes = new Array(this.numBins);
      console.log("binnedData = " + binnedData);
      for (var i = 0; i < this.numBins; i++){
        console.log("Bin " + i + " = " + binnedData[i]);
        binSizes[i] = binnedData[i].length;
      }

      var labelArray = new Array(this.numBins);
      if (this.binNames == "automatic"){
        // Generate bin labels
        labelArray[0] = "[0, " + (1/this.numBins).toFixed(2).toString() + ")";
        for (var j = 1; j < this.numBins; j++){
          labelArray[j] = "[" + ((1/this.numBins)*j).toFixed(2).toString() + ", " + ((1/this.numBins) * (j+1)).toFixed(2).toString() + ")"; // Again, we've hard-coded the domain max as 1
        }
      }
      else{
        labelArray = this.binNames;
      }

      this.renderChart({
        //labels: new Array(this.data.length),
        labels: labelArray,
        datasets: [
          {
            label: this.name,
            backgroundColor: this.barColor,
            data: binSizes
          }
        ]
      });
    }
  },

  mounted() {
    this.renderHistogram();
  },
})
</script>
