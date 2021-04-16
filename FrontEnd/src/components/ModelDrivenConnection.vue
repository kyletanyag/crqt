<template>
<div> 
  <h3>{{layerName1}} to {{layerName2}}</h3>
  <div> 
  <table width=100% border="0" cellspacing="0">
    <tbody>
      <tr v-for="(node1, index1) in layerNodes1" :key="index1" width=100%>
        <td width="33%">
          <p>
            <strong>Node ID: {{node1.id}}</strong>
            <br>
            <strong>{{node1.vendor}} {{node1.product}}</strong> is one of your selected nodes from <strong>{{layerName1}}</strong>. 
            Please select which node(s) from <strong>{{layerName2}}</strong> you would like to connect.
            </p>
        </td>
        <td>
          <!-- <input type='checkbox' @click='checkAll()' v-model='isCheckAll' @change='updateCheckall()'> Check All -->
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
          nextNode: this.selectedNodes[i]
        })
      }
      return edges;
    }, 

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
      selectedNodes.push([]);
    }

    return {
      selectedNodes,
      isCheckAll: false,
    };
  },
}
</script>