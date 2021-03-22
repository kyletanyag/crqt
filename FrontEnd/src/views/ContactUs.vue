<template>
  <div id="app">
    <Multiselect class="multiselect"
      v-model="L1Vendor"
      mode="multiple"
      placeholder="Select your Vulnerabilites"
      :options="L1VendorInput.options"
      label="L1VendorInput[selectedVendor].options"
    >
    <select v-for="option in L1VendorInput[selectedVendor].options" :key="option" :value="option">{{option}}</select>
    </Multiselect>
 
  </div>
  
</template>

<script>
  import Multiselect from '@vueform/multiselect'

  export default {
    components: { Multiselect },
    data() {
      return {
        L1VendorInput:[
      {
        label:"Cisco",
        options:["Cisco1","Cisco2","Cisco3"]
      },
      {
        label:"Juniper",
        options:["Juniper1","Juniper2","Juniper"]
      },
      {
        label:"Microsoft",
        options:["Microsoft1","Microsoft2","Microsoft3"]
      }
    ],
     selectedVendor:"Microsoft", 
     selectedOption:'',
      L1Vendor:[],
      }
    }
    
  }

</script>
<style>
.multiselect{
float: none;
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
  text-align: left;
  widows: 20%;
  }
</style>
