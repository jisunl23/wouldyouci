<template>
  <div 
    class="ratings"      
    v-infinite-scroll="loadMore"
    infinite-scroll-disabled="busy"
    infinite-scroll-distance="2"
    >
    
    <RatingForm class="rating-form" v-if="!scored" @submitRating="addRating"/>
    <div v-else>
      <div class="notification">
        리뷰를 작성한 영화입니다.
      </div>
    </div>

    <div class="avg-score">
      <div>{{ getAvgScore }} </div>
      <v-rating
        class="score"
        :value="getAvgScore"
        background-color="amber lighten-2"
        color="amber lighten-1"
        half-increments
        readonly
        size=20
        ></v-rating>
    </div>

    <v-list 
      v-show="isRatings"
      >
      <v-list-item
        v-for="(rating, index) in ratings"
        :key="index"
        class="rating"
        >
        <v-list-item-avatar
          color="lightgrey" 
          x-small
          >
          
          <img 
            v-if="rating.user.file"
            :src="getUserProfile(rating.user)"
            />
          <v-img 
            v-else
            src="../../../assets/astronaut1.png"
            />
        </v-list-item-avatar>
        <v-list-item-content>
          <div class="infos">
            <div class="user">
              {{ rating.user.username }} | {{ formatDate(rating.updated_at) }}
            </div>
            <div class="score">
              <v-rating
                class="score"
                :value="rating.score"
                background-color="amber lighten-4"
                color="amber lighten-3"
                dense
                half-increments
                readonly
                size=14
                ></v-rating>
            </div>
          </div>
          <div class="content">
            <div class="comment">{{ rating.comment}}</div>
            <div v-if="rating.user.username == currentUser.username" class="button">
              <v-dialog v-model="dialog">
                <template v-slot:activator="{ on }">
                  <v-btn
                    v-on="on"
                    icon 
                    color="lightgrey"
                    x-small
                    >
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                </template>
                <RatingEditForm :rating="rating" :index="index" @close="closeModal" @editRating="editRating"/>
              </v-dialog>

              <v-btn 
                icon
                color="lightgrey"
                x-small
                @click.prevent="deleteRating(index, rating, details.id)"
                >
                <v-icon>mdi-close</v-icon>
              </v-btn>
            </div>
          </div>
        </v-list-item-content>
      </v-list-item>
      <v-btn
        v-show="ratings.length > 5"
        class="upbutton"
        color="titleblue"
        small
        bottom
        fixed
        right
        fab
        @click="goTop"
        ><v-icon color="white">mdi-arrow-up</v-icon></v-btn>
    </v-list>

    <div v-show="!isRatings">
      <div class="notification">
        첫번째 리뷰를 남겨주세요 :)
      </div>
    </div>
  </div>
</template>

<script>
import RatingForm from '../../ratingForm/RatingForm';
import RatingEditForm from '../../ratingForm/RatingEditForm';
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'MovieRatings',
  props:["details", ],
  components: {
    RatingForm,
    RatingEditForm,
  },

  data() {
    return {
      currentUser: '',
      busy: false,
      nextPage: 1,
      dialog: false,

      scored: false,
      isRatings: false,
      ratings: [],
    }
  },
  
  async created() {
    var jwt = require('jsonwebtoken');
    const token = sessionStorage.getItem('jwt');
    var decoded = jwt.decode(token, {complete: true});
    this.currentUser = decoded.payload
    if (this.details.has_score) {
      this.scored = true
    }
  },

  computed: {
    ...mapGetters(['getMovieRatings', 'getAvgScore']),
 
  },

  methods: {
    ...mapActions(['fetchScore', 'fetchRatings', 'postRating', 'delRating', 'patchRating' ]),

    async loadMore() {
      this.busy = true;
      if ( this.nextPage > 0 ) {
        const item = 'movie'
        const params = { 
          movie: this.details.id, 
          page: this.nextPage++,
          };
        const resData = await this.fetchRatings({item, params})
        
        const itemId = this.details.id
        await this.fetchScore({item, itemId});
        if ( resData.count > 0 ) {
          this.isRatings = true;
          for ( const rating of resData.results) {
            this.ratings.push(rating);
          }
        }
        if ( resData.next == null ) {
          this.nextPage = 0
        }
      }
      this.busy = false;
    },

    formatDate(date) {
      var dayjs = require('dayjs')
      return dayjs(date).format('YYYY.MM.DD')
    },
    
    closeModal() {
      this.dialog = false;
    },

    getUserProfile(user) {
      const HOST = process.env.VUE_APP_SERVER_HOST;
      const profileURL = `${HOST}/${user.file[0]}`;
      return profileURL
    },

    async deleteRating(index, rating) {
      const item = 'movie'
      const ratingId = rating.id;
      if (confirm('삭제하시겠습니까?')) {
        await this.delRating({item, ratingId});
        const itemId = this.details.id
        await this.fetchScore({item, itemId});
        this.$delete(this.ratings, index)
        if ( index === 0 ) {
          this.isRatings = false
          }
        }
      this.scored = false
      },
    
    async addRating(rating){
      const item = 'movie'
      rating[item] = this.details.id;
      const res = await this.postRating({item, rating});
      res.data["user"] = this.currentUser;
      if ( this.isRatings ) {
        this.ratings.unshift(res.data)
      } else {
        this.isRatings = true
        this.ratings.push(res.data)
      }
      const itemId = this.details.id
      await this.fetchScore({item, itemId});
      this.scored = true
    },
    
    async editRating(editedRating) {
      this.dialog = false;
      const item = 'movie';
      editedRating[item] = this.details.id;
      await this.patchRating({item, editedRating});
      const itemId = this.details.id
      await this.fetchScore({item, itemId});
      this.ratings = [];
      this.nextPage = 1;
      this.loadMore();
    },

    goTop() {
      window.scrollTo(0, 0);
    },
    
    }
  }
</script>

<style src="./MovieRatings.css" scoped></style>