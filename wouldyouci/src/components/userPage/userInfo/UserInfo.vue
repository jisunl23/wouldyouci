<template>
  <div class="userInfo pb-1 pt-4">
    <div>
      <img v-if="UserProfile" class="userImage" @click="isShow = !isShow" :src="UserProfile" />
      <img v-else class="userImage" @click="isShow = !isShow" src="../../../assets/astronaut1.png" />
    </div>
    <v-dialog v-model="isShow">
      <v-row justify="center">
        <div v-if="UserProfile">
          <img class="bigUserImage canSee" :src="UserProfile" />
          <v-btn text small class="btnTrash" @click="deleteP"><v-icon>fas fa-trash</v-icon></v-btn>
        </div>
        <img v-else class="bigUserImage" src="../../../assets/astronaut1.png" />
      </v-row>
    </v-dialog>
    <span class="userName">{{ UserName }}</span>
    <p class="userHello mb-2">우주씨, 오늘은 어떤 영화를 볼까요?</p>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  name: 'UserInfo',
  props: ['UserName', 'UserProfile'],
  data() {
    return {
      isShow: false
    }
  },
  methods: {
    ...mapActions(['deleteProfile', 'bringUserInfo']),
    async deleteP() {
      this.isShow = false;
      await this.deleteProfile();
      this.$emit("deleteP");
    }
  },
}
</script>

<style src="./UserInfo.css" scoped></style>