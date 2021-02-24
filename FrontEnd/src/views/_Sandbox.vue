<template>
<div>
    <qr-code :username="kyle" :secret="abcdefghi"></qr-code>
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
