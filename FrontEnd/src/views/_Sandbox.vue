<template>
<div>
    <!-- <qr-code :username="kyle" :secret="abcdefghi"></qr-code> -->
    <data-driven-input></data-driven-input>
</div>
</template>


<script>
import DataDrivenInput from '../components/DataDrivenInput.vue'
// import QRCode from './QRCode.vue'

export default {
    name: 'Sandbox',

    components: {
        // 'qr-code': QRCode,
        DataDrivenInput,
    }
}
</script>
