<template>
  <div>
    <Title />
    <div class='userPage mt-0 mr-0 ml-0'>
      <div class="settingIcon ml-3 mr-3">
        <v-icon small color="titlepink" @click="isShow=!isShow">fas fa-cog</v-icon>
        <v-dialog v-model="isShow">
          <SettingCard @settingCard="closeDialog" />
        </v-dialog>
        <v-dialog v-model="isShowChangeImgDialog">
          <ChangeUserImage v-if="isShowChangeImgDialog" @changeUserImage="closeChangeImgDialog" @changeP="changeP"/>
        </v-dialog>
        <v-dialog v-model="isShowChangePassDialog">
          <ChangeUserPass v-if="isShowChangePassDialog" v-bind:UserName="userName" @changeUserPass="closeChangePassDialog"/>
        </v-dialog>
      </div>
      <UserInfo v-bind:UserName="userName" v-bind:UserProfile="profileURL" @deleteP="deleteP"/>
      <div class="tabs">
        <v-tabs
          v-model="tab"
          background-color="rgba(163, 102, 244, 0.13)"
          grow
        >
          <v-tab
            v-for="item in items"
            :key="item"
          >
            {{ item }}
          </v-tab>
        </v-tabs>
      </div>
      <div class="prefer" v-if="tab===0">
        <TheaterList v-bind:Label="'선호하는 영화관'" v-bind:TheaterList="theaterList"/>

        <MovieList v-bind:Label="'내가 좋아하는 영화'" v-bind:CinemaList="pickMovies"/>

        <MovieList v-bind:Label="'찜한 상영예정작'" v-bind:CinemaList="pushMovies" />

        <MovieList v-if="recommendedOnscreen.length" v-bind:Label="'추천 상영작'" v-bind:CinemaList="recommendedOnscreen"/>
        <div v-else>
          <div class="label">
              <h4>추천 상영작</h4>
            </div>
          <v-card class="noReco" >
            
            <div class="exp">
              현재 데이터가 부족해 영화 추천이 불가능 합니다.
            </div>
            <v-btn text @click="goFirstRating">
              영화 평가하러 가기
              <v-icon small style="margin-left:3vw;">fas fa-arrow-right</v-icon>
            </v-btn>
          </v-card>
        </div>
        
        <MovieList v-if="recommendedMovies.length" v-bind:Label="'이런 영화는 어때요?'" v-bind:CinemaList="recommendedMovies"/>
        <div v-else>
          <div class="label">
              <h4>이런 영화는 어때요?</h4>
            </div>
          <v-card class="noReco">
            <div class="exp">
              현재 데이터가 부족해 영화 추천이 불가능 합니다.
            </div>
            <v-btn text @click="goFirstRating">
              영화 평가하러 가기
              <v-icon small style="margin-left:3vw;">fas fa-arrow-right</v-icon>
            </v-btn>
          </v-card>
        </div>
      </div>
      <div class="rating" v-else>
        <RatingMovies v-bind:CinemaList="ratedMovies"/>
      </div>
    </div>
    <v-overlay :value="getLoading">
        <v-progress-circular
          :size="70"
          :width="7"
          color="#4520EA"
          indeterminate
        ></v-progress-circular>
      </v-overlay>
  </div>
</template>

<script>
import Title from '../nav/Title.vue';
import UserInfo from './userInfo/UserInfo.vue';
import MovieList from './movieList/MovieList.vue';
import TheaterList from './movieList/TheaterList.vue';
import SettingCard from './settingCard/SettingCard.vue';
import ChangeUserImage from './changeUserInfo/ChangeUserImage.vue';
import ChangeUserPass from './changeUserInfo/ChangeUserPass.vue';
import RatingMovies from './ratingMovies/RatingMovies.vue';
import router from '../../router';
import { mapGetters, mapMutations, mapActions } from 'vuex';

export default {
  name: 'UserPage',
  components: {
    Title,
    UserInfo,
    MovieList,
    TheaterList,
    SettingCard,
    ChangeUserImage,
    ChangeUserPass,
    RatingMovies
  },
  data() {
    return {
      theaterList: null,
      ratedMovies: null,
      pickMovies: [],
      pushMovies: [],
      recommendedOnscreen: [],
      recommendedMovies: [],
      isShow: false,
      isShowChangeImgDialog: false,
      isShowChangePassDialog: false,
      userName: null,
      profileURL: null,
      tab: 0,
      items: ['선호하는 영화', '평가한 영화']
    }
  },
  computed: {
    ...mapGetters(['getUserInfo', 'getLoading'])
  },
  methods: {
    ...mapMutations(['setLoading', 'setLoginMode']),
    ...mapActions(['bringUserInfo', 'bringRatedMovies']),
    closeDialog(type) {
      if (type === "image") {
        this.isShowChangeImgDialog = true;
      } else if (type === "password") {
        this.isShowChangePassDialog = true;
      }
      this.isShow = false;
    },
    closeChangeImgDialog() {
      this.isShowChangeImgDialog = false;
    },
    closeChangePassDialog() {
      this.isShowChangePassDialog = false;
    },
    goFirstRating() {
      router.push('/firstRating');
    },
    async deleteP() {
      await this.bringUserInfo();
      if (this.getUserInfo.data.user.file.length) {
        const HOST = process.env.VUE_APP_SERVER_HOST;
        this.profileURL = `${HOST}/${this.getUserInfo.data.user.file[0]}`;
      } else {
        this.profileURL = null;
      }
    },
    async changeP() {
      await this.bringUserInfo();
      if (this.getUserInfo.data.user.file.length) {
        const HOST = process.env.VUE_APP_SERVER_HOST;
        this.profileURL = `${HOST}/${this.getUserInfo.data.user.file[0]}`;
      } else {
        this.profileURL = null;
      }
    }
  },
  async mounted() {
    this.setLoginMode(null);
    this.setLoading(true);
    await this.bringUserInfo();
    const HOST = process.env.VUE_APP_SERVER_HOST;
    if (this.getUserInfo.data.user.file.length) {
      this.profileURL = `${HOST}/${this.getUserInfo.data.user.file[0]}`;
    }
    this.userName = this.getUserInfo.data.user.username;
    this.theaterList = this.getUserInfo.data.pick_cinemas;
    // this.pickMovies = this.getUserInfo.data.pick_movies;
    // this.pushMovies = this.getUserInfo.data.push_movies;
    
    for (var i in this.getUserInfo.data.pick_movies) {
      console.log()
      var dayjs = require('dayjs')
      if (dayjs().isBefore(dayjs(this.getUserInfo.data.pick_movies[i].open_date))) {
        this.pushMovies.push(this.getUserInfo.data.pick_movies[i])
      } else {
        this.pickMovies.push(this.getUserInfo.data.pick_movies[i])

      }
    }

    this.recommendedOnscreen = this.getUserInfo.data.recommend_onscreen;
    this.recommendedMovies = this.getUserInfo.data.recommend_movies;
    const res = await this.bringRatedMovies();
    this.ratedMovies = res;
    this.setLoading(false);
  }
}
</script>

<style src="./UserPage.css" scoped></style>