<template>
   <body>
      
      <h3 style="padding-left:10px"> Input Settings: Corporate Firewall, Corporate DMZ and Corporate LAN</h3>
      <h4 style="padding-left:10px"> If you would like to upload a CSV file, click the button below.</h4>
      <form class="form-inline my-2 my-lg-0" action="/Sandbox" style="padding-left:10px">
                        <button type="submit">CSV File Upload</button>
                    </form>
      <h4> Corporate Firewall L1 Settings:</h4>
      <p> Please select the poduct vendor, model, and quantity for your Corporate Firewall 1.</p>
      <table width=100% border="0" cellspacing="0" >
         <tbody>
            <tr>
               <td width="33%">
                  <div align="center">
                     <p align="center">Corporate Firewall L1 Vendor</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
               <td align="center" width="33%">
                  <div align="center">
                     <p>Corporate Firewall L1 Product</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
               <td width="33%">
                  <div align="center">
                     <p>Number of Coporate Firewall 1</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
            </tr>
         </tbody>
      </table>
      <h4> Corporate DMZ Settings:</h4>
      <p> Please select the poduct vendor, model, and quantity for your Corporate DMZ Network. Use the "Add Server" button to add and "Remove Server" button to remove </p>
      <form>
         <input type="button" @click="addRow(row)" value="Add Server">
         <input type="button" class="add-row" value="Remove Server">
      </form>
      <table id="AddServer" width="100%" border="0" cellspacing="0">
         <tbody>
            <tr>
               <td width="25%">
                  <div align="center">
                     <p align="center">Corporate Firewall L1 Vendor</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
               <td width="25%">
                  <div align="center">
                     <p>Corporate Firewall L1 Product</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
               <td width="25%">
                  <div align="center">
                     <p>Number of Coporate Firewall 1</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
               <td width="25%">
                  <div align="center">
                     <p>Number of Coporate Firewall 1</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
            </tr>
         </tbody>
      </table>
      <h4> Corporate Firewall L2 Settings:</h4>
      <p> Please select the poduct vendor, model, and quantity for your Corporate Firewall L2.</p>
      <table width=100% border="0" cellspacing="0" >
         <tbody>
            <tr>
               <td width="33%">
                  <div align="center">
                     <p align="center">Corporate Firewall L2 Vendor</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
               <td align="center" width="33%">
                  <div align="center">
                     <p>Corporate Firewall L2 Product</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
               <td width="33%">
                  <div align="center">
                     <p>Number of Coporate Firewall L2</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
            </tr>
         </tbody>
      </table>
      <h4> Corporate LAN Settings</h4>
      <p> Please select the poduct vendor, model, and quantity for your Corporate LAN Network.  Use the "Add Server" button to add and "Remove Server" button to remove </p>
      <form>
         <input type="button" class="add-row" value="Add Server">
         <input type="button" class="add-row" value="Remove Server">
      </form>
      <table id="AddServer" width="100%" border="0" cellspacing="0">
         <tbody>
            <tr>
               <td width="25%">
                  <div align="center">
                     <p align="center">Corporate Firewall L1 Vendor</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
               <td width="25%">
                  <div align="center">
                     <p>Corporate Firewall L1 Product</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
               <td width="25%">
                  <div align="center">
                     <p>Number of Coporate Firewall 1</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
               <td width="25%">
                  <div align="center">
                     <p>Number of Coporate Firewall 1</p>
                     <select>
                        <option value="">Option 1</option>
                        <option value="">Option 2</option>
                     </select>
                  </div>
               </td>
            </tr>
         </tbody>
      </table>
 
    <DynamicRow msg="Add / Edit / Clone / Delete row in vue.js"/>
  
   </body>
</template>

<script>

export default {

  data() {
    return {
      output: "",
      flowers: []
    };
  },
    methods:{
    addRow: function(){
      this.rows.push({});
    },
    removeRow: function(row){
      //console.log(row);
      this.rows.$remove(row);
    }
  }
};
</script>
<style>
   table, th, td {
   border: 1px solid rgb(5, 5, 5);
   border-collapse: collapse;
   }
   th, td {
   padding: 5px;
   text-align: left;    
   }
   h4{
   padding-left: 10px;
   padding-top: 30px;
   }
   p{
   padding-left: 10px;
   padding-bottom:10px;
   }
</style>