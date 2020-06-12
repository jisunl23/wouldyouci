<template>
  <div class='signup'>
    <div class='title mb-1'>
      <img class='title' src='../../assets/signup.jpg' />
    </div>
    <LoginForm v-if="getLoginMode === 'login'" />
    <SignupForm v-else-if="getLoginMode === 'signup'" />
    <v-overlay :value="getLoading">
      <v-progress-circular
        :size="70"
        :width="7"
        color="#4520EA"
        indeterminate
      ></v-progress-circular>
    </v-overlay>
    <div class="goMapBtn">
      <v-btn text @click="goMainMap">비회원으로 사용하기<v-icon small>fas fa-arrow-right</v-icon></v-btn>
    </div>
  </div>
</template>

<script>
  import LoginForm from './forms/LoginForm.vue';
  import SignupForm from './forms/SignupForm.vue';
  import { mapGetters, mapMutations } from 'vuex';
  import router from "../../router";

  export default {
    name: 'Signup',
    components: {
      SignupForm,
      LoginForm
    },
    computed: {
      ...mapGetters(['getLoginMode', 'isLoggedIn', 'getLoading'])
    },
    methods: {
      ...mapMutations(['setLoginMode']),
      goMainMap() {
        router.push('/');
      }
    },
    mounted() {
      this.setLoginMode('login');
    },
    created() {
      if (this.isLoggedIn) {
        router.push('/');
      }
    }
  }
</script>

<style src="./Signup.css" scoped></style>