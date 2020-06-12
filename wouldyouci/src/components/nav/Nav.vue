<template>
<v-bottom-navigation
  color="secondary"
  height="7vh"
  app
  fixed
  grow
  shift
  align="center"
  >
    <v-btn @click="goMap">
      <v-icon class="pt-1">mdi-map-outline</v-icon>
      <span class="pt-1">Nearby</span>
    </v-btn>

    <v-btn @click="goSearch">
      <v-icon class="pt-1">mdi-magnify</v-icon>
      <span class="pt-1">Search</span>
    </v-btn>

    <v-btn @click="goUserPage">
      <v-icon class="pt-1">mdi-account-outline</v-icon>
      <span class="pt-1">My Page</span>
    </v-btn>
  </v-bottom-navigation>
</template>

<script>
import router from "@/router";
import { mapGetters, mapMutations } from 'vuex';

export default {
  name: 'Nav',
  data() {
    return {
      bottomNav: 0,
    }
  },
  computed: {
    ...mapGetters(['getSearchMode', 'isLoggedIn']),
  },
  methods: {
    ...mapMutations(['setSearchMode', 'setLoginMode']),
    goMap() {
      this.bottomNav = 0
      const link = document.location.href.split("/");
      if (link[link.length - 1]) {
        router.push('/');
      }
    },
    goSearch() {
      //실제 출시용 코드
      if (this.isLoggedIn) {
        const link = document.location.href.split("/");
        if (link[link.length - 1] !== "search") {
          router.push('/search');
        } else {
          location.reload();
        }
        if (this.getSearchMode === 'after') {
          this.setSearchMode('before');
        }
      } else {
        this.setLoginMode('login');
        router.push('/signup');
      }
    },
    goUserPage() {
      // 실제 출시용 코드
      if (this.isLoggedIn) {
        const link = document.location.href.split("/");
        if (link[link.length - 1] !== "userPage") {
          router.push('/userPage');
        } else {
          location.reload();
        }
      } else {
        this.setLoginMode('login');
        router.push('/signup');
      }
    }
  }
}
</script>
<!--<style src="./Nav.css" scoped></style>-->
<style>
  /*v-btn {*/
  /*  padding: 0;*/
  /*}*/

  /*v-icon {*/
  /*  size: x-small;*/
  /*}*/

  span {
    font-size: 1.5vh;
    /*bottom: 0;*/
    align-items: center;
    /*top: 0.5vh;*/
  }
</style>