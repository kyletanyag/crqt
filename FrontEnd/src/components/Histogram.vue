<script>

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
      let numInEachBin = new Array(this.numBins); for (let i=0; i<this.numBins; ++i) numInEachBin[i] = 0;
      var binSize = 1/this.numBins; // Assuming the range is 0-1
      // console.log("Started binning the array: " + this.data);
      // console.log(this.data.length);
      for (var k = 0; k < this.data.length; k++){ // for each data point
        numInEachBin[Math.floor(this.data[k]/binSize)] += 1; // determine which bin it is in, then add one to the total number in that bin.
        // console.log("  Binned " + this.data[k] + " into bin index " + Math.floor(this.data[k]/binSize));
        // console.log("  Current numInEachBin: " + numInEachBin);
        // console.log("");
      }
      //console.log(numInEachBin)

      var labelArray = new Array(this.numBins);
      if (this.binNames == "automatic"){
        // Generate bin labels
        labelArray[0] = "[0, " + (1/this.numBins).toFixed(2).toString() + ")";
        for (var j = 1; j < this.numBins-1; j++){
          labelArray[j] = "[" + ((1/this.numBins)*j).toFixed(2).toString() + ", " + ((1/this.numBins) * (j+1)).toFixed(2).toString() + ")"; // Again, we've hard-coded the domain max as 1
        }
        //the last bin should range from [x, 1], notice the use of brackets for the end of the domain.
        labelArray[j] = "[" + ((1/this.numBins)*j).toFixed(2).toString() + ", 1]";
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
            data: numInEachBin
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
