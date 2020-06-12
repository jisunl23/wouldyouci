<template>
  <v-card class="changeUserImage">
    <v-file-input
      class="userImage"
      label="프로필 사진"
      prepend-icon="fas fa-camera"
      @change="onFileChange"
      ref="fileInput"
    >
    </v-file-input>
    <v-img
      class="prev"
      :src="showImage"
      small-chips accept="image/*"
      clearable
    >
    </v-img>
    <v-card-actions class="mb-2 pa-0">
      <v-item-group>
        <v-btn text class="mr-0 ml-0" color="lightprimary" @click="change(image)">submit</v-btn>
        <v-btn text class="ml-1 mr-1" color="primary" @click="closeDialog">cancle</v-btn>
      </v-item-group>
    </v-card-actions>
  </v-card>
</template>

<script>
import { mapActions } from 'vuex';
export default {
  name: 'changeUserImage',
  data() {
    return {
      image: null
    }
  },
  computed: {
    showImage() {
      if (this.image) {
        const url = URL.createObjectURL(this.image)
        return url
      }
      return require("../../../assets/stars.png")
    }
  },
  methods: {
    ...mapActions(['registerProfile']),
    onFileChange(file) {
      this.image = file;
    },
    closeDialog() {
      this.$emit("changeUserImage");
    },
    async change(image) {
      if (image) {
        await this.registerProfile(image);
        this.$emit("changeP");
        this.$emit("changeUserImage");
      } else {
        alert('사진을 등록해주세요.')
      }
    }
  }
}
</script>

<style src="./ChangeUserImage.css" scoped></style>