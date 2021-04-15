<template>
<div>
  <div class="d-flex flex-row pb-2">
    <button class="btn btn-secondary"
      v-if="defaultPage"
      @click="this.$router.push({name: defaultPage})"
    >
      Table of Contents
    </button>
  </div>
  <div class="d-flex justify-content-between pb-2">
    <div class="col-2">
      <button class="btn btn-primary btn-lg" 
        v-if="prevPage"
        @click="this.$router.push({name: prevPage})"
      >
        <i class="fa fa-arrow-left"></i>&nbsp; Previous 
      </button>
    </div>
    <div class="col">
      <h1 class="pb-1">{{ title }}</h1>
    </div>
    <div class="col-2">
      <button class="btn btn-primary btn-lg" 
        v-if="nextPage"
        @click="this.$router.push({name: nextPage})"
      >
        Next &nbsp;<i class="fa fa-arrow-right"></i>
      </button>
    </div>
  </div>
</div>

</template>
<script>
export default {
  name: 'Result Header',

  props: {
    title: String,
    prevPage: String,
    nextPage: String,
    defaultPage: String,
  },

  mounted() {
    const btns = document.getElementsByTagName('button');
      btns.forEach((b) => {
        b.disabled = true;
      });
    setTimeout(() => {
        btns.forEach((b) => {
          b.disabled = false;
        });
      }, 1500)
  },
}
</script>
<style>
</style>