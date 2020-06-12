
<template>
  <div class="body">

    <div class="trailer">
      <MovieTrailer :details="details" />
    </div>


    <div class="details">

      <v-list-item two-line>
        <v-list-item-content>
          <v-list-item-title>{{ details.name }}</v-list-item-title>
          <v-list-item-subtitle>{{ details.name_eng }}</v-list-item-subtitle>
          <v-list-item-subtitle>{{ details.watch_grade }}</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>


      <div class="container">
        <div class="left">
          {{ details.predicted_score }} % 일치  
        </div>

        <div class="right">

          <v-btn v-show="!isPicked"
            color='grey'
            text
            @click.prevent="togglePickMovie">
            <span>찜</span>
            <v-icon>mdi-plus</v-icon>
          </v-btn>

          <v-btn v-show="toBeReleased && isPicked"
            color="elsepink"
            icon
            @click.prevent="togglePickMovie">
            <v-icon>mdi-bell</v-icon>
          </v-btn>

          <v-btn v-show="!toBeReleased && isPicked"
            color="elsepink"
            icon
            @click.prevent="togglePickMovie">
            <v-icon>mdi-heart</v-icon>
          </v-btn>
      
          <v-dialog 
            v-if="details.is_showing"
            v-model="dialog">
            <template v-slot:activator="{ on }">
              <v-btn
                v-on="on"
                color="titleblue"
                text
                >
                <span>예매</span>
                <v-icon>mdi-video-vintage</v-icon>
              </v-btn>
            </template>
            <MovieShowingCinemas @close="closeModal" />
          </v-dialog>
        </div>
      </div>
    </div>


    <div class="tab-card">
      <v-tabs
        v-model="tab"
        background-color="transparent"
        centered
        fixed-tabs
        >
        <v-tab
          v-for="item in items"
          :key="item.tab"
          >
          {{ item.tab }}
        </v-tab>
      </v-tabs>
      <v-tabs-items v-model="tab">
        <v-tab-item
          v-for="item in items"
          :key="item.tab"
          >
          <v-card flat>
            <v-card-text>
              <component 
                class="tab-item"
                v-bind:is="item.component" 
                :details="details"
                ></component>
            </v-card-text>
          </v-card>
        </v-tab-item>
      </v-tabs-items>
    </div>
  
  </div>
</template>

<script>
import Title from '../nav/Title.vue';
import MovieTrailer from './movieTrailer/MovieTrailer';
import MovieShowingCinemas from './movieInfo/MovieShowingCinemas';
import MovieInfo from './movieInfo/MovieInfo';
import MovieRatings from './movieRatings/MovieRatings';
import Score from '../ratingForm/Score';
import { mapGetters, mapActions } from 'vuex';


export default {
  name: 'MovieDetail',
  components: {
    Title,
    MovieTrailer,
    MovieShowingCinemas,
    MovieInfo,
    MovieRatings,
    Score,
  },

  async created() {
    await this.fetchMovieDetail(this.$route.params.id);
    this.isPicked = this.details.pick_movies
    // 개봉영화일까 아닐까
    var dayjs = require('dayjs')
    if ( dayjs().isBefore(dayjs(this.details.open_date))) {
      this.toBeReleased = true
    }
  },

  data() {
    return {
      tab: null,
      items: [
        {tab: 'Info', component: "MovieInfo"},
        {tab: 'Reviews', component: "MovieRatings"}
      ],
      expand: false,
      isPicked: false,
      dialog: false,
      toBeReleased: false,
    }
  },

  computed: {
    ...mapGetters({
      details: 'getMovieDetail',
      }),
  },

  methods: {
    ...mapActions(['fetchMovieDetail', 'togglePick', ]),
    closeModal() {
      this.dialog = false;
    },
    async togglePickMovie() {
      const item = 'movie'
      const itemId = this.details.id
      await this.togglePick({item, itemId})
      if ( this.isPicked ){
        this.isPicked = false
      } else {
        this.isPicked = true
        if ( this.toBeReleased ) {
          alert('영화 개봉시 알려줄게~')
        } else {
          alert('나도 이 영화 좋아해~')
        }
      }
    },
  },
}
</script>


<style src="./MovieDetail.css" scoped></style>