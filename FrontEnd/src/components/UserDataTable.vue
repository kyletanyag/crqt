<template>
<div class="col-8">
  <div class="card mt-4" >
    <div class="card-header font-weight-bold">{{ title }}</div>
    <table v-if="anyUsers" class="table m-0">
      <thead>
        <tr>
          <th scope="col">Name</th>
          <th scope="col">Email</th>
          <th scope="col">Role</th>
          <th scope="col" v-if="approve || reject || info">Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.name }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.role }}</td>
          <td>
            <button v-if="approve" @click="ApproveUser(user.id)" class="btn btn-success btn-sm mx-1">Approve</button>
            <button v-if="reject" @click="DeleteUser(user.id)" class="btn btn-danger btn-sm mx-1">Delete</button>
            <button v-if="info" @click="GetUserInfo(user.id)" class="btn btn-info btn-sm mx-1">Info</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-else-if="happyError" class="alert alert-success" role="alert">
      <p>No outstanding user registration requests!</p>
    </div>
    <div v-else class="alert alert-danger" role="alert">
      <p>Error with connecting to user databse! </p>
    </div>
  </div>
</div>
</template>

<script>
import http from '../http-common.js';

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
    },

    happyError: {
      type: Boolean,
      default: false,
    },
  },

  methods: {
    ApproveUser(id) {
      http.get(`approve_user/${id}`).then((r) => {
        console.log(r);
        this.$emit('approve');
      }); 
      
    },

    DeleteUser(id) {
      http.get(`delete_user/${id}`).then((r) => {
        console.log(r);
        this.$emit('delete');
      }); 
      
    },

    GetUserInfo(id) {
      return id;
    },
  },
  
  computed: {
    anyUsers() {
      return this.users && this.users.length > 0;
    }
  }
}
</script>

<style>

</style>