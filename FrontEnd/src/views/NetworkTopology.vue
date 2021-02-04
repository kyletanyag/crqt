<template>
<body>

<h3 style="padding-left:10px"> Input Settings: Corporate FIrewall, Corporate DMZ and Corporate LAN</h3>
<table width="100%" border="0" cellpadding="px">
  
   <tbody>
     <tr>
       <div style="padding:10px">
       <h4> Corporate Firewall L1 Settings:</h4>
       <p> Please select the poduct vendor, model, and quantity for your Corporate Firewall 1.</p>
       </div>
    </tr>

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
         
         <td width="33%" align="center">
           <div align="center">
            <p>Number of Coporate Firewall 1</p>
            <select>
                <option value="">Option 1</option>
               <option value="">Option 2</option>
            </select>
            </div>
         </td>
      </tr>
      <tr>
        <div style="padding:10px">
       <h4> Corporate DMZ Settings:</h4>
       <p> Please select the poduct vendor, model, and quantity for your Corporate DMZ Network. Use the "Add Server" button to add and "Remove Server" button to remove </p>
       </div>
      </tr>
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
      </tr>
   </tbody>
</table>

</body>
</template>

<script>

</script>
<style>
table, th, td {
  border: 1px solid rgb(255, 255, 255);
  border-collapse: collapse;
}
th, td {
  padding: 5px;
  text-align: left;    
}

.btn-group {
  min-width: 160px;
  height: 40px;
  position: relative;
  margin: 10px 1px;
  display: inline-block;
  vertical-align: middle;
}
.btn-group a:hover {
  text-decoration: none;
}

.dropdown-toggle {
  color: #636b6f;
  min-width: 160px;
  padding: 10px 20px 10px 10px;
  text-transform: none;
  font-weight: 300;
  margin-bottom: 7px;
  border: 0;
  background-image: linear-gradient(#009688, #009688), linear-gradient(#D2D2D2, #D2D2D2);
  background-size: 0 2px, 100% 1px;
  background-repeat: no-repeat;
  background-position: center bottom, center calc(100% - 1px);
  background-color: transparent;
  transition: background 0s ease-out;
  float: none;
  box-shadow: none;
  border-radius: 0;
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
}
.dropdown-toggle:hover {
  background: #e1e1e1;
  cursor: pointer;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  z-index: 1000;
  float: left;
  min-width: 160px;
  padding: 5px 0;
  margin: 2px 0 0;
  list-style: none;
  font-size: 14px;
  text-align: left;
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.175);
  background-clip: padding-box;
}

.dropdown-menu > li > a {
  padding: 10px 30px;
  display: block;
  clear: both;
  font-weight: normal;
  line-height: 1.6;
  color: #333333;
  white-space: nowrap;
  text-decoration: none;
}
.dropdown-menu > li > a:hover {
  background: #efefef;
  color: #409FCB;
}

.dropdown-menu > li {
  overflow: hidden;
  width: 100%;
  position: relative;
  margin: 0;
}

.caret {
  width: 0;
  position: absolute;
  top: 19px;
  height: 0;
  margin-left: -24px;
  vertical-align: middle;
  border-top: 4px dashed;
  border-top: 4px solid \9;
  border-right: 4px solid transparent;
  border-left: 4px solid transparent;
  right: 10px;
}

li {
    list-style: none;
}
</style>