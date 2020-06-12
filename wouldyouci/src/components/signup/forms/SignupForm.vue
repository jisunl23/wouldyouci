<template>
  <v-card class="form" outlined>
    <v-card-title class="formtitle">Signup</v-card-title>
    <v-card-text class="pb-0">
      <v-form>
        <div v-if="getErrors.length" class="errors">
          <ul>
            <li v-for="(error, idx) in getErrors" :key="idx">{{ error }}</li>
          </ul>
        </div>
        <v-text-field
          label="Id"
          name="Id"
          prepend-icon="fas fa-user"
          type="text"
          v-model="userInfo.userName"
          :rules="[rules.required]"
        ></v-text-field>
        <v-text-field
          id="email"
          label="E-mail"
          name="email"
          prepend-icon="fas fa-envelope"
          type="email"
          v-model="userInfo.email"
          :rules="[rules.required]"
        ></v-text-field>
        <v-text-field
          id="password"
          label="Password"
          name="password"
          prepend-icon="fas fa-lock"
          type="password"
          v-model="userInfo.password"
          :rules="[rules.required]"
        ></v-text-field>
        <v-text-field
          id="passwordConfirm"
          label="Password Confirmation"
          name="passwordConfirm"
          prepend-icon="fas fa-lock"
          type="password"
          v-model="userInfo.passwordConfirm"
          :rules="[rules.required, rules.passwordMatch]"
        ></v-text-field>
      </v-form>
    </v-card-text>
    <v-card-actions class="mb-2 pa-0">
      <v-spacer></v-spacer>
      <v-btn text class="mr-0 ml-0" color="lightprimary" @click="setLoginMode('login')">Login</v-btn>
      <v-btn text class="ml-1 mr-4" color="primary" @click.prevent="signup(userInfo)">Submit</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
  import { mapGetters, mapMutations, mapActions } from 'vuex';
  export default {
    name: 'SignupForm',
    data() {
      return {
        userInfo: {
          userName: '',
          email: '',
          password: '',
          passwordConfirm: ''
        },
        rules: {
          required: value => !!value || '필수 항목입니다.',
          passwordMatch: value => value === this.userInfo.password || '비밀번호가 일치하지 않습니다.'
        }
      }
    },
    computed: {
      ...mapGetters(['getErrors'])
    },
    methods: {
      ...mapMutations(['setLoginMode', 'clearErrors']),
      ...mapActions(['signup'])
    },
    created() {
      this.clearErrors();
    }
  }
</script>

<style src="./Form.css" scoped></style>