<script>
/*eslint-disable */
import { defineComponent } from 'vue'
import { Bar } from 'vue3-chart-v2'

export default defineComponent({
  name: 'Histogram',
  extends: Bar,

  options: {
    responsive: true,
    maintainAspectRatio: true,
    legend: {
      display: false
    },
    tooltips: {
      enabled: false
    },
  },

  props: {
    data: Array,
    binNames: {
      type: Array,
      default: function() {return ['automatic'] }
    },
    numBins: Number, //Vue was giving me an error in SimulationResults.vue, saying that it expected a number but I was passing a string.
    binLimits: {
      type: Array, // Assume the input is always in ascending order.
      default: function() {return [-1] } //assume a user will never enter a bin limit set of "-1". That doesnt make sense.
    },
    range: {
      type: Array, // Assume the range is given from lowest to highest
      default: function() {return [0,1] } // most of the time, we want a range from 0 to 1.
    },
    name: String,
    xAxis: {
      type: String,
      default: 'X-Axis'
    },
    yAxis: {
      type: String,
      default: 'Y-Axis'
    },
    barColor: String,

    // Line-chart Props:
    usingLineChart: {
      type: Boolean,
      default: false
    },
    lineData: {
      type: Array,
      default: function() {return [] }
    },
    // lineName: {   /// Line name isnt displayed anymore
    //   type: String,
    //   default: ''
    // },
    lineColor: {
      type: String,
      default: '#7979f8'
    },
  },

  watch: {
    name() {   
      this.state.chartObj.destroy()
      this.renderHistogram();
    },

    numBins() {
      // this.state.chartObj.destroy();
      // this.renderHistogram();  

      // just reassign data and options then call update
      this.state.chartObj.data = this.parseData();
      this.state.chartObj.update();
    },
  },

  methods: {
    renderHistogram() {

      var rangeSize = this.range[1]-this.range[0];

      // Bin the data
      let numInEachBin = new Array(this.numBins); for (let i=0; i<this.numBins; ++i) numInEachBin[i] = 0;
      if (this.binLimits == -1){ //if its the default value, automatically definine bins
        var binSize = rangeSize/this.numBins; // divide the range by the number of bins
        for (var k = 0; k < this.data.length; k++) { // for each data point
          numInEachBin[this.data[k] !== +this.range[1] ? Math.floor(this.data[k]/binSize) : this.numBins - 1]++; // determine which bin it is in, then add one to the total number in that bin.
        }
      }
      else{ // if the user is using custom bin sizes
        //this.binLimits.sort()// sort in ascending order - This introduces an error, so we are just always assuming its in ascendeding order.
        for (var m = 0; m < this.data.length; m++){ // for each data point
          for (var l = 0; l < this.binLimits.length; l++){ // for each possible bin where the data could lie
            if (this.data[m] <= this.binLimits[l]){ // if the data belongs in this bin
              numInEachBin[l]++; // increment the number of datapoints in that bin
              break; // dont check any more bins for this particular data point
            }
          }
        }
      }

      var labelArray = new Array(this.numBins);
      if (this.binNames == "automatic"){
        // Generate bin labels
        labelArray[0] = "[" + this.range[0].toFixed(2).toString() + ", " + ((rangeSize/this.numBins)+this.range[0]).toFixed(2).toString() + ")";
        for (var j = 1; j < this.numBins-1; j++){
          labelArray[j] = "[" + (((rangeSize/this.numBins)*j)+this.range[0]).toFixed(2).toString() + ", " + (((rangeSize/this.numBins) * (j+1))+this.range[0]).toFixed(2).toString() + ")"; // Again, we've hard-coded the domain max as 1
        }
        //the last bin should range from [x, 1], notice the use of brackets for the end of the domain.
        labelArray[j] = "[" + (((rangeSize/this.numBins)*j)+this.range[0]).toFixed(2).toString() + ", " + this.range[1].toFixed(2).toString() + "]";
      }
      else{
        labelArray = this.binNames;
      }

      this.renderChart(
        { // data
          labels: labelArray,
          datasets: [
            { // Line dataset comes first so that it's drawn on top of the histogram.
              type: 'line',
              //label: this.lineName,
              borderColor: this.lineColor,
              data: this.lineData,
              fill: false, // we never want to fill in the space beneath the line. It looks awful
              hidden: !this.usingLineChart
            },
            {
              type: 'bar',
              label: this.name,
              backgroundColor: this.barColor,
              data: numInEachBin
            }
          ],
        },
        { // options
          scales: {
            yAxes: [{
              scaleLabel: {
                display: true,
                labelString: this.yAxis
              },
              ticks: {
                beginAtZero: true
              }
            }],
            xAxes: [{
              scaleLabel: {
                display: true,
                labelString: this.xAxis
              }
            }]
          },
          legend: {
            display: false
          },
          tooltips: {
            enabled: false
          },
          title: {
            display: true,
            text: this.name
          }
        }
      );
    },

    parseData() {
      var rangeSize = this.range[1]-this.range[0];

      // Bin the data
      let numInEachBin = new Array(this.numBins); for (let i=0; i<this.numBins; ++i) numInEachBin[i] = 0;
      if (this.binLimits == -1){ //if its the default value, automatically definine bins
        var binSize = rangeSize/this.numBins; // divide the range by the number of bins
        for (var k = 0; k < this.data.length; k++) { // for each data point
          numInEachBin[this.data[k] !== +this.range[1] ? Math.floor(this.data[k]/binSize) : this.numBins - 1]++; // determine which bin it is in, then add one to the total number in that bin.
        }
      }
      else{ // if the user is using custom bin sizes
        //this.binLimits.sort()// sort in ascending order - This introduces an error, so we are just always assuming its in ascendeding order.
        for (var m = 0; m < this.data.length; m++){ // for each data point
          for (var l = 0; l < this.binLimits.length; l++){ // for each possible bin where the data could lie
            if (this.data[m] <= this.binLimits[l]){ // if the data belongs in this bin
              numInEachBin[l]++; // increment the number of datapoints in that bin
              break; // dont check any more bins for this particular data point
            }
          }
        }
      }

      var labelArray = new Array(this.numBins);
      if (this.binNames == "automatic"){
        // Generate bin labels
        labelArray[0] = "[" + this.range[0].toFixed(2).toString() + ", " + ((rangeSize/this.numBins)+this.range[0]).toFixed(2).toString() + ")";
        for (var j = 1; j < this.numBins-1; j++){
          labelArray[j] = "[" + (((rangeSize/this.numBins)*j)+this.range[0]).toFixed(2).toString() + ", " + (((rangeSize/this.numBins) * (j+1))+this.range[0]).toFixed(2).toString() + ")"; // Again, we've hard-coded the domain max as 1
        }
        //the last bin should range from [x, 1], notice the use of brackets for the end of the domain.
        labelArray[j] = "[" + (((rangeSize/this.numBins)*j)+this.range[0]).toFixed(2).toString() + ", " + this.range[1].toFixed(2).toString() + "]";
      }
      else{
        labelArray = this.binNames;
      }

      return {
          labels: labelArray,
          datasets: [
            {
              label: this.name,
              backgroundColor: this.barColor,
              data: numInEachBin
            }
          ],
        };
    }
  },

  mounted() {
    this.renderHistogram();
  },
})
</script>

