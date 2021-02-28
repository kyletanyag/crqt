<template>
<div class="col d-flex justify-content-center">
  <div class="card mt-4">
    <div class="card-header font-weight-bold">{{ title }}</div>
    <table class="table m-0">
      <thead>
        <tr>
          <th scope="col">Name</th>
          <th scope="col">Username</th>
          <th scope="col">Email</th>
          <th scope="col" v-if="approve || reject || info">Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="{ name, username, email } in users" :key="username">
          <td>{{ name }}</td>
          <td>{{ username }}</td>
          <td>{{ email }}</td>
          <td>
            <button v-if="approve" @click="ApproveUser(username)" class="btn btn-success btn-sm mx-1">Approve</button>
            <button v-if="reject" @click="RejectUser(username)" class="btn btn-danger btn-sm mx-1">Reject</button>
            <button v-if="info" @click="GetUserInfo(username)" class="btn btn-info btn-sm mx-1">Info</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
</template>

<script>
export default {
  name: 'User Data Table',

  props: {
    title: {
      type: String,
      default: undefined,
      required: true,
    },

    users: {
      type: Array,
      default: undefined,
      required: true,
    },

    approve: {
      type: Boolean,
      default: true,
    },

    reject: {
      type: Boolean,
      default: true,
    },

    info: {
      type: Boolean,
      default: true,
    }
  },

  methods: {
    ApproveUser(id) {
      return id;
    },

    RejectUser(id) {
      return id;
    },

    GetUserInfo(id) {
      return id;
    },
  }, 

}
</script>

<style>

</style>