<template>
  <v-card>
    <div @click="changeUserInfo('image')">
      <v-icon color="primary" class="mr-1">fas fa-user-circle</v-icon>
      프로필 사진 변경
    </div>
    <v-divider></v-divider>
    <div @click="changeUserInfo('password')">
      <v-icon color="primary" class="mr-1">fas fa-key</v-icon>
      비밀번호 변경
    </div>
    <v-divider></v-divider>
    <div @click="logout">
      <v-icon color="primary" class="mr-1">fas fa-sign-out-alt</v-icon>
      로그아웃
    </div>
  </v-card>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  name: 'settingCard',
  methods: {
    ...mapActions(["logout"]),
    closeDialog() {
      this.$emit("settingCard", "close")
    },
    changeUserInfo(type) {
      this.$emit("settingCard", type)
    }
  }
}
</script>

<style src="./SettingCard.css" scoped></style>