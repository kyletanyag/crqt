<template>
<div>
    <qr-code :username="'ktany001'"></qr-code>
    <data-driven-input></data-driven-input>
    <!-- <user-data-table title="Unregistered Users" :users="d"></user-data-table> -->
    <!-- <user-data-table title="All Users" :users="d" :approve="false"></user-data-table> -->
</div> 
</template>


<script>
import QRCode from './QRCode.vue'

export default {
    name: 'Sandbox',

    components: {
        'qr-code': QRCode
    }
}
</script>
