<template>
  <div>
    <Title />
    <div class="body">
      <p>Not Found</p>
      <button v-on:click="goBack">돌아가기</button>
    </div>
  </div>
</template>

<script>

import Title from '../nav/Title';

export default {
  name: 'NotFound',
  components: {
    Title,
  },
  methods: {
    goBack: function () {
      this.$router.push('/')
      }
    },

}
</script>
<style src="./NotFound.css" scoped></style>