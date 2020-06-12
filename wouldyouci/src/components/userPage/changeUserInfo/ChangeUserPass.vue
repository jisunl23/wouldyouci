<template>
  <v-card class="changeUserPass">
    <v-card-text>
      <p>
        아이디
      </p>
      <h3>
        {{ UserName }}
      </h3>
      <v-text-field
        label="New Password"
        prepend-icon="fas fa-lock"
        type="password"
        v-model="userInfo.password"
        :rules="[rules.required]"
      ></v-text-field>
      <v-text-field
        label="Password Confirmation"
        prepend-icon="fas fa-lock"
        type="password"
        v-model="userInfo.passwordConfirm"
        :rules="[rules.required, rules.passwordMatch]"
      ></v-text-field>
    </v-card-text>
    <v-card-actions class="mb-2 pa-0">
      <v-spacer></v-spacer>
        <v-btn text class="mr-0 ml-0" color="lightprimary" @click="change(userInfo)">submit</v-btn>
        <v-btn text class="ml-1 mr-4" color="primary" @click="closeDialog">cancle</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { mapActions } from 'vuex';
export default {
  name: 'changeUserPass',
  props: ["UserName"],
  data() {
    return {
      userInfo: {
        password: null,
        passwordConfirm: null
      },
      rules: {
        required: value => !!value || '필수 항목입니다.',
        passwordMatch: value => value === this.userInfo.password || '비밀번호가 일치하지 않습니다.'
      }
    }
  },
  methods: {
    ...mapActions(['changePassword']),
    closeDialog() {
      this.$emit("changeUserPass");
    },
    change(userInfo) {
      if (userInfo.password) {
        if (userInfo.password === userInfo.passwordConfirm) {
          this.changePassword(userInfo);
          this.$emit("changeUserPass");
        } else {
          alert('비밀번호가 일치하지 않습니다.');
        }
      } else {
        alert('비밀번호를 입력하세요.');
      }
    }
  }
}
</script>

<style src="./ChangeUserPass.css" scoped></style>