<template>
  <div>
    <Title />
    <div class='search'>
      <v-container>
          
        <v-radio-group dense v-model="searchType" row>
          <v-radio label="영화" value="movies"></v-radio>
          <v-radio label="영화관" value="theater"></v-radio>
        </v-radio-group>
        <div class="auto">
          
          <v-autocomplete
                  v-if="searchType === 'movies'"
                  :search-input.sync="keyword"
                  label="영화 제목을 검색해보세요!"
                  prepend-icon="fas fa-search"
                  :loading="isloading"
                  :items="items"
                  :rules="rules"
                  @input="changeSearchMode"
                  v-on:keyup.enter="changeSearchMode(keyword)"
          >
          </v-autocomplete>
          <v-autocomplete
                  v-else
                  :search-input.sync="keyword"
                  label="지역명을 검색해보세요!"
                  prepend-icon="fas fa-search"
                  :loading="isloading"
                  :items="items"
                  :rules="rules"
                  @input="changeSearchMode"
                  v-on:keyup.enter="changeSearchMode(keyword)"
          >
          </v-autocomplete>
          
        </div>
      </v-container>
      <div class="now" v-if="getInitSearchInfo">
          <v-btn small text @click="reBringMyPos">
          <v-icon small>fas fa-crosshairs</v-icon>
          {{ nowAddress }}
        </v-btn>
      </div>
      <div v-if="getSearchMode">
        <MainSearch v-if="getSearchMode==='before'" v-bind:pos="pos" v-bind:Commings="commings" v-bind:Populars="populars" v-bind:TheaterList="nearTheater"/>
        <AfterSearch v-else v-bind:KeyWords="keywordProps" v-bind:Type="searchTypeProps" v-bind:ResultList="cards" v-bind:Similar="similar"/>
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
  </div>
</template>

<script>
  import Title from '../nav/Title.vue';
  import MainSearch from './mainSearch/MainSearch.vue';
  import AfterSearch from './afterSearch/AfterSearch.vue';
  import { mapGetters, mapMutations, mapActions } from 'vuex';

  export default {
    name: 'Search',
    components:{
      Title,
      MainSearch,
      AfterSearch
    },
    data() {
      return {
        rules: [
          value => (value || '').length <= 20 || '최대 글자수는 20글자 입니다.'
        ],
        cards: [],
        keyword: null,
        keywordProps: null,
        nowAddress: null,
        similar: [],
        searchType: 'movies',
        searchTypeProps: 'movies',
        pos: null,
        nearTheater: [],
        commings: [],
        populars: [],
        isloading: false,
        items: [],
        label:true,
      }
    },
    computed: {
      ...mapGetters(['getSearchMode', 'getInitSearchInfo', 'getSearchList', 'getSearchSimiList', 'getAddress', 'getLoading'])
    },
    watch: {
      keyword: function(val) {
        const axios = require('axios');
        const HOST = process.env.VUE_APP_SERVER_HOST;
        const params = {
          params: {
            words: val
          }
        }
        this.isloading = true;
        if (this.searchType === 'movies') {
          axios.get(`${HOST}/search/movie/`, params)
                  .then(res => {
                    this.items = res.data;
                    this.isloading = false;
                  })
                  .catch(err => err)
        } else {
          axios.get(`${HOST}/search/cinema/`, params)
                  .then(res => {
                    this.items = res.data;
                    this.isloading = false;
                  })
                  .catch(err => err)
        }
      }
    },
    methods: {
      ...mapMutations(['setSearchMode', 'setLoading', 'setLoginMode']),
      ...mapActions(['bringInitSearchInfo', 'searchMovies', 'bringAddress', 'searchTheater']),
      async changeSearchMode(info) {
        if (info) {
          this.keywordProps = info;
          this.searchTypeProps = this.searchType;
          if (this.searchType === 'movies') {
            await this.searchMovies(info);
          } else {
            await this.searchTheater(info);
          }
          this.cards = this.getSearchList;
          this.similar = this.getSearchSimiList;
          this.keyword = null;
          this.setSearchMode('after');
        }
      },
      reBringMyPos() {
        this.setLoading(true);
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(function(position) {
            const pos = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };
            this.pos = pos;
          }.bind(this))
          if (this.pos) {
            setTimeout(async function() {
              await this.bringAddress(this.pos);
              await this.bringInitSearchInfo(this.pos);
              this.nowAddress = this.getAddress;
              this.nearTheater = this.getInitSearchInfo.near_cinema;
              this.commings = this.getInitSearchInfo.comming_soon;
              this.populars = this.getInitSearchInfo.popular_movies;
              this.setLoading(false);
            }.bind(this), 400)
          }
        } else {
          this.setLoading(false);
          alert('위치 설정을 켜주세요.');
        }
      }
    },
    mounted() {
      this.setLoginMode(null);
      this.setLoading(true);
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
          const pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
          };
          this.pos = pos;
        }.bind(this))
        setTimeout(async function() {
          await this.bringAddress(this.pos);
          await this.bringInitSearchInfo(this.pos);
          this.nowAddress = this.getAddress;
          this.nearTheater = this.getInitSearchInfo.near_cinema;
          this.commings = this.getInitSearchInfo.comming_soon;
          this.populars = this.getInitSearchInfo.popular_movies;
          this.setLoading(false);
        }.bind(this), 400)
      } else {
        this.setLoading(false);
        alert('위치 설정을 켜주세요.');
      }
    }
  }
</script>

<style src="./Search.css" scoped></style>