<template>
  <div>
    <div v-if="CinemaList">
      <v-spacer></v-spacer>
      
      <div>
        <span class="mod">
          평점을 수정할 수 있어요
        </span>
        <span 
            class="goReview"
        >
          <v-chip 
            color="rgba(173, 139, 232, 0.8)"
            text-color="#FFFFFF"
             text @click="goFirstRating">
            영화 평가하기 
            <v-icon small>fas fa-arrow-right</v-icon>
          </v-chip>
        </span>
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
            현재까지 평가한 영화 - {{ CinemaList.length }} 편
          </v-chip>
        </div>
      <v-container class="ranklist" fluid grid-list-xl>
      <v-layout justify-center row wrap x12 md8>
        <v-flex>
          <v-row dense>
            <v-col v-for="(movie, idx) in CinemaList" :key="idx" :cols="12">
                  <v-card
              class="mycard">
              <v-row>
                <v-col class="col-4">
                  <v-img
                    :src="movie.movie.poster"
                    class="card_image"
                  @click="goDetail(movie.movie.id)"

                  >
                  </v-img>
                </v-col>
                <v-col class="col-8">
                  <v-list-item>
                    <v-list-item-content class="list">
                      <v-list-item-title class="mytitle">{{ movie.movie.name }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>

                  <v-card-text class="movieInfo">
                      
                      <v-card-actions class="pt-0">
                        <v-rating
                          v-model="movie.score"
                          color="#FDD835"
                          background-color="#c5c2c2"
                          size="5.5vw"
                          dense
                          half-increments
                          @input="changeRating({'ratingId': movie.id,'movieId': movie.movie.id, 'rating':movie.score})">
                        </v-rating>
                      </v-card-actions>
                    <div style="text-align:center">
                      <v-spacer></v-spacer>
                    </div>
                  </v-card-text>
                </v-col>
                  <v-divider></v-divider>
              </v-row>
            </v-card>
            </v-col>
            <v-divider></v-divider>
          </v-row>
        </v-flex>
      </v-layout>
    </v-container>
    </div>
    <div class="noReco" v-else>
      아직 평가한 영화가 없습니다.
    </div>
  </div>
</template>

<script>
import router from "../../../router";

export default {
  name: 'RatingMovies',
  props: ["CinemaList"],
  methods: {
    goDetail(movieId) {
      router.push(`/movie/${movieId}`);
    },
    goFirstRating() {
      router.push('/firstRating');
    },
    changeRating(info) {
      const axios = require("axios");
      const HOST = process.env.VUE_APP_SERVER_HOST;
      const token = sessionStorage.getItem('jwt');
      const options = {
        headers: {
          Authorization: `JWT ${token}`
        }
      }
      const data = {
        score: info.rating,
        movie: info.movieId
      }
      axios.patch(`${HOST}/movie/rating/${info.ratingId}/`, data, options)
        .then(res => res)
        .catch(err => err)
    }
  }
}
</script>

<style src="./RatingMovies.css" scoped></style>