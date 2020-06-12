<template>
  <v-app>
    <div id="app" class="app" data-app>
      <router-view />
    </div>
    <Nav v-if="getLoginMode === null"/>
  </v-app>
</template>

<script>
import Nav from './nav/Nav';
import { mapGetters } from 'vuex';

export default {
  components: {
    Nav
  },
  computed: {
    ...mapGetters(['getLoginMode'])
  },
  created() {
    this.$store.dispatch("initialLogin");
  }
};
</script>

<style>
.app {
  /* font-family: 'Noto Sans KR', monospace, 'Nanum Myeongjo', 'Noto Serif KR', 'NanumBarunGothicOTF' serif; */
  font-family: 'Noto Sans KR', sans-serif;
}
</style>
