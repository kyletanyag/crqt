<template>
    <div class="home">
        <img alt="CRQT logo" src="../assets/logo.png">
        <HelloWorld msg="Welcome to the Cyber Resilience Quantification Tool (CRQT)"
                    msg2="TestMessage" />
    </div>
</template>

<script>
// @ is an alias to /src
    import HelloWorld from '@/components/HelloWorld.vue'
    export default {
        name: 'Home',
        components: {
            HelloWorld
        }
    }
</script>
