<template>
<div class="col-8">
  <div class="card mt-4" >
    <div class="card-header font-weight-bold">{{ title }}</div>
    <div  v-if="anyUsers" :style="`overflow-y: auto; height: ${height}px;`">
      <table class="table table-hover m-0">
        <thead>
          <tr>
            <th @click="sort('name')"  scope="col">Name<i :class="sortDirection('name')"></i></th>
            <th @click="sort('email')"  scope="col">Email<i :class="sortDirection('email')"></i></th>
            <th @click="sort('role')"  scope="col">Role<i :class="sortDirection('role')"></i></th>
            <th scope="col" v-if="approve || reject || info">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in sortedUsers" :key="user.id">
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
    </div>
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
    
    height: {
      type: Number,
      default: 240,
    }
  },
  
  data() {
    return {
      currentSort: 'name',
      currentSortDir: 'asc',      
    }
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

    sort(s) {
      if (s === this.currentSort) {
        this.currentSortDir = this.currentSortDir ==='asc' ? 'desc':'asc';
      }
      this.currentSort = s;
    },

    sortDirection(s) {
      if (this.currentSortDir === 'asc' && s === this.currentSort)
        return 'fa fa-fw fa-sort-asc';
      else if (this.currentSortDir === 'desc' && s === this.currentSort)
        return 'fa fa-fw fa-sort-desc';
      else
        return 'fa fa-fw fa-sort';
    },
  },
  
  computed: {
    anyUsers() {
      return this.users && this.users.length > 0;
    },

    sortedUsers() {
      if (!this.users) return 0;
      return this.users.slice(0).sort((a,b) => {
        let modifier = 1;
        if(this.currentSortDir === 'desc') modifier = -1;
        if(a[this.currentSort] < b[this.currentSort]) return -1 * modifier;
        if(a[this.currentSort] > b[this.currentSort]) return 1 * modifier;
        return 0;
      });
    }
  }
}
</script>

<style>

</style>