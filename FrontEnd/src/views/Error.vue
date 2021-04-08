<template>
<div>
  <div v-if="errorCode === 'Flask' && !recheckedFlask" class="alert alert-danger" role="alert">
    <p>
      There is an issue with connecting to the backend <strong>Flask</strong> server at port 5000. Please recheck your connection.
    </p>
  </div>
  <div v-else-if="errorCode === 'CVE-Search' && !recheckedCVESearch" class="alert alert-danger" role="alert">
    There is an issue with connecting to the backend <strong>CVE-Search</strong> server at port 2000. Please recheck your connection.
  </div>
  <div v-else class="alert alert-success">
    <p>
      Issue resolved. You can now return to the <router-link to="/">home page</router-link> to continue using the CRQT.
    </p>
  </div>
  <div>
    <div class="py-2">
      <button class="btn btn-secondary" @click="CheckConnections">
        Recheck connections?
      </button>
    </div>
    <div v-if="responseFlask" :class="GetAlertClass(connectionFlask)">
      <h4>Flask</h4>
      <p v-if="responseFlask.status === 200">
        Status: {{ responseFlask.status }}, {{ responseFlask.statusText }}
      </p>
      <p v-else>
        Status: {{ responseFlask.message }} <br> {{ responseFlask.stack }}
      </p>
    </div>
    <div v-if="responseCVESearch" :class="GetAlertClass(connectionCVESearch)">
      <h4>CVE-Search</h4>
      <p v-if="responseCVESearch.status === 200">
        Status: {{ responseCVESearch.status }}, {{ responseCVESearch.statusText }}
      </p>
      <p v-else>
        Status: {{ responseCVESearch.message }} <br> {{ responseCVESearch.stack }}
      </p>
    </div>
  </div>
</div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'Error',

  props: {
    errorCode: String
  },

  data() {
    return {
      responseFlask: undefined,
      responseCVESearch: undefined,
      connectionFlask: false,
      connectionCVESearch: false,
      rechecked: false,
    }
  },

  methods: {
    CheckConnections() {
      // check connection to Flask server
      axios.get('http://localhost:5000/test_connection')
        .then((r) => {
          console.log(r)
          this.responseFlask = r;
          this.connectionFlask = r.status === 200 ? true : false;
          this.recheckedFlask = r.status === 200 ? true : false;
        })
        .catch((e) => {
          this.responseFlask = e;
          this.connectionFlask = false;
          this.recheckedFlask = false;
        });

      // check connection to CVE-Search server
      axios.get('http://localhost:2000/api/browse/microsoft')
        .then((r) => {
          this.responseCVESearch = r;
          this.connectionCVESearch = r.status === 200 ? true : false;
          this.recheckedCVESearch = r.status === 200 ? true : false;
        })
        .catch((e) => {
          this.responseCVESearch = e;
          this.connectionCVESearch = false;
          this.recheckedCVESearch = false;
        });
    },

    GetAlertClass(x) {
      return x ? 'alert alert-success' : 'alert- alert-danger'
    }
  },
}
</script>