<template>
<div> 
  <h4>{{layerName1}} to {{layerName2}} Connections:</h4>
  <div class="pb-2"> 
  <p>
    Please define the network connections between nodes from the {{layerName1}} layer to {{layerName2}} layer.
  </p>
  <table class="table table-bordered" style="width: 80%">
    <tbody>
      <tr v-for="(node1, index1) in layerNodes1" :key="index1">
        <td width="40%">
          <h5>Node ID: <strong>{{node1.id}}</strong></h5>
          <p>
            <strong>{{node1.vendor}} {{node1.product}}</strong> is one of your selected nodes from <strong>{{layerName1}}</strong>. 
            Please select which node(s) from <strong>{{layerName2}}</strong> you would like it to connect to.
            </p>
        </td>
        <td>
          <h5>Possible Connecting Nodes:</h5>
          <div v-for="(node2, index2) in layerNodes2" :key="index2" @change='updateCheckall()'>                         
            <input type="checkbox" v-model="selectedNodes[index1]" :value="node2.id" />
            {{node2.vendor}} {{node2.product}} (Node ID: {{node2.id}}) 
          </div>
        </td>
      </tr>
    </tbody>
  </table>
  </div>
</div>   
</template>

<script>
export default {
  name: 'Model Driven Connections',

  props:{
    layerNodes1: Array,
    layerNodes2: Array,
    layerName1: String,
    layerName2: String,
  },
  methods:{
    checkAll() {
      for (let i = 0; i < this.layerNodes1.length; i++) {
        this.selectedNodes[i] = [];
        this.layerNodes2.forEach((n) => {
          this.selectedNodes[i].push(n.id);
        });
      }
    },

    uncheckAll() {
      for (let i = 0; i < this.layerNodes1.length; i++) {
        this.selectedNodes[i] = [];
      }   
    }
  },

  computed:{
    rowData() {
      if (!this.selectedNodes) return;

      var edges = [];
      for (let i = 0; i < this.layerNodes1.length; i++) {
        edges.push({
          currNode: this.layerNodes1[i].id,
          nextNode: this.selectedNodes[i].filter((n) => {return n !== 0;})
        })
      }
      return edges;
    }, 

    checkSelection() {
      if(!this.selectedNodes.length) return false;
      for (let i = 0; i < this.selectedNodes.length; i++) {
        if(!this.selectedNodes[i].filter((n) => {return n !== 0;}).length) return false;
      }   
      return true;
    }
  },

  data() {
    // inits selected nodes array to be multi-dimensional
    // for v-model checkbox selections
    var selectedNodes = [];
    for (let i = 0; i < this.layerNodes1.length; i++) {
      let a = [];
      for (let j = 0; j < this.layerNodes2.length; j++) {
        a.push(0);
      }
      selectedNodes.push(a);
    }

    return {
      selectedNodes,
    };
  },
}
</script>