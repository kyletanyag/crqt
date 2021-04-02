<template>
<div> 
    {{node1}} 
    <div> 
    <table width=100% border="0" cellspacing="0">
        <tbody>
            <tr v-for="(row, index) in node1" :key="index" :row="row" width=100%>
                <td width="33%">
                    <p>{{node1[index].vendor}} {{node1[index].product}} is one of your selected nodes from {{layer1}}. Please select which node from {{layer2}} would you would like to connect?</p>
                </td>
                <td>
                    <div v-for="(row, index2) in node2" :key="index2" :row="row" >                         
                            <input type="checkbox" v-model="selectedNode[index2]" :value="node2[index2].product" />
                            {{node2[index].vendor}} {{node2[index].product}}
                        
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
    name: 'edges',

    props:{
        node1: Array,
        node2: Array,
        layer1: Array,
        layer2: Array,
        vertices: Array,
        currNode: Array,
        nextNode: Array
    },
    computed:{
        edges() {
        var nodes = []
            nodes.push({
                // currNode: node1[index],
                nextNode: this.selectedNode
                // vulnerabilities: this.selectedVulnerabilities[i]
            });
            
        return nodes;
        }, 
    },
    data() {
        return{
        selectedNodes:[[]]
        
        };
    },
}
</script>