<template>
<div>
  <div class="d-flex flex-row">
    <button class="btn btn-secondary btn-sm"
      v-if="defaultRouteName"
      @click="this.$router.push({name: defaultRouteName})"
    >
      Table of Contents
    </button>
  </div>
  <div class="d-flex justify-content-between pb-2">
    <div class="col">
      <button class="btn btn-primary" 
        v-if="prevRouteName"
        @click="this.$router.push({name: prevRouteName})"
      >
        Previous &nbsp;<i class="fa fa-arrow-left"></i>
      </button>
    </div>
    <div class="col">
      <h2 class="pb-1">{{ title }}</h2>
    </div>
    <div class="col">
      <button class="btn btn-primary" 
        v-if="nextRouteName"
        @click="this.$router.push({name: nextRouteName})"
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
    prevRouteName: String,
    nextRouteName: String,
    defaultRouteName: String,
  }
}
</script>
<style>
</style>