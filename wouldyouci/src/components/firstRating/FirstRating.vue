<template>
  <div>
    <Title />
    <div 
      class="firstRating"
      v-infinite-scroll="loadMore" 
      infinite-scroll-disabled="Flag"
      infinite-scroll-distance="50vh"
    >
      <v-card class="explanation">
        <v-card-text>
          아래의 영화 중 본 영화에 대해 평점을 남겨주시면
          당신의 취향에 맞는 영화를 추천해드립니다.
          <h4>단, 최소 10개 이상의 영화를 평가해주셔야 추천이 가능합니다.</h4>
        </v-card-text>
      </v-card>
      <v-container fluid>
        <div class="chip">
          <v-chip
            color="rgba(173, 139, 232, 0.8)"
            text-color="#FFFFFF"
            class="chip"
          >
            <v-avatar tile>
              <v-icon>
                fas fa-film
              </v-icon>
            </v-avatar>
            현재까지 평가한 영화 - {{ beforeCnt + cnt }} 편
          </v-chip>
        </div>
        <v-row justify="end">
          <v-btn color="rgba(173, 139, 232, 0.9)" class="next"  text @click="goMap">
            다음에 하기<v-icon small>fas fa-arrow-right</v-icon>
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn class="save" color="rgba(173, 139, 232, 0.9)" @click="submitRating" text>저 장</v-btn>
        </v-row>
        <v-row dense justify="center">
          <v-col
            v-for="card in cards"
            :key="card.name"
            cols="6"
            xs="6"
            sm="3"
            md="3"
          >


          <v-hover v-slot:default="{ hover }">
            
            <v-card
              class="movieCard"
            >

              <v-img
                :src="card.poster"
                class="white--text align-end"
                height="35vmin 40vmax"
                width="35vmin 40vmax"
                contain
              >
              </v-img>

              <v-expand-transition>
                <div
                  v-if="hover || card.rating >0"
                  class="d-flex transition-fast-in-fast-out v-card--reveal"
                >
                  <div class="rating">
                    {{card.name}}
                    <v-divider></v-divider>
                      <v-rating
                    @input="addRating({'id': card.id, 'rating': card.rating})"
                    v-model="card.rating"
                    color="#FDD835"
                    background-color="#757575"
                    half-increments
                    small
                    hover
                  ></v-rating>
                  </div>
                </div>
              </v-expand-transition>

              
            </v-card>
            </v-hover>
          </v-col>
        </v-row>
        <v-btn
          text
          large
          rounded
          fab
          retain-focus-on-click 
          class="upBtn"
          @click="goTop"
        >
          <v-icon large>fas fa-arrow-circle-up</v-icon>
        </v-btn>
      </v-container>
    </div>
    <div class="progress" v-if="getLoading">
      <v-progress-circular
        :size="70"
        :width="7"
        color="#4520EA"
        indeterminate
      ></v-progress-circular>
    </div>
  </div>
</template>

<script>
import Title from '../nav/Title.vue';
import router from '../../router';
import { mapGetters, mapMutations, mapActions } from 'vuex';

export default {
  name: 'UserPage',
  components: {
    Title
  },
  data() {
    return {
      cards: [],
      next: 1,
      Flag: false,
      check: {},
      ratedId: {},
      cnt: 0,
      beforeCnt: 0
    }
  },
  computed: {
    ...mapGetters(['getLoading'])
  },
  methods: {
    ...mapMutations(['setLoading', 'setLoginMode']),
    ...mapActions(['bringRatingMovies', 'submitRatings', 'checkRating']),
    goMap() {
      router.push('/');
    },
    async loadMore() {
      this.Flag = true;
      this.setLoading(true);
      const res = await this.bringRatingMovies(this.next);
      this.Flag = false;
      this.setLoading(false);
      this.next += 1;
      this.cards = this.cards.concat(res.results);
    },
    submitRating() {
      this.submitRatings(this.ratedId);
    },
    goTop() {
      window.scrollTo(0, 0);
    },
    addRating(cardInfo) {
      if (!this.ratedId[cardInfo.id]) {
        this.cnt += 1;
        this.ratedId[cardInfo.id] = cardInfo.rating;
      } else {
        this.ratedId[cardInfo.id] = cardInfo.rating;
      }
    }
  },
  async mounted() {
    this.setLoginMode(null);
    const res = await this.checkRating('notLogin');
    this.beforeCnt = res;
  }
}
</script>

<style src="./FirstRating.css" scoped></style>