<template>
  <div>
    <div class="label">
      <h4>{{ Label }}</h4>
    </div>
    <v-container class="ranklist" fluid grid-list-xl>
      <v-layout justify-center row wrap x12 md8>
        <v-flex>
          <v-row dense>
            <v-col v-for="(movie, idx) in CurrentList" :key="idx" :cols="12">
              <v-card
              @click="goDetail(movie.id)"
          class="mycard"
          elevation="0">
          <v-row>
            <v-col class="col-4">
              <v-img
                :src="movie.poster"
                class="card_image"
              >
              </v-img>
            </v-col>
            <v-col class="pl-0 pr-0 pb-1 pt-2 mr-0 col-6">
              <v-list-item>
                <v-list-item-content class="pt-3 pb-2">
                  <v-list-item-title class="mytitle">{{ movie.name }}</v-list-item-title>
                  <v-list-item-subtitle v-if="movie.name_eng" class="mysubtitle">{{ movie.name_eng }}</v-list-item-subtitle>
                  <v-list-item-content v-else class="mysubtitle2">.</v-list-item-content>
                </v-list-item-content>
              </v-list-item>

              <v-card-text class="movieInfo">
                  
                <div class="rating">
                  <v-rating
                :value="movie.score"
                color="#FDD835"
                background-color="white"
                half-increments
                readonly
                dense
                x-small
                ></v-rating>
                </div>
                <span v-for="(genre, idx) in movie.genres" :key="idx">
                      <span v-if="idx != movie.genres.length-1" class="genre" >
                        {{genre +" |"}}
                        </span>
                        <span v-else class="genre" > 
                          {{genre}}
                        </span>
                  </span>
                <div>
                <v-chip x-small v-if="movie.watch_grade==='15세 관람가'"
                        label color="#FCB5C7" class="mb-1"
                >15+</v-chip>
                  <v-chip x-small v-else-if="movie.watch_grade==='12세 관람가'"
                         label color="#E9EA72" class="mb-1"
                  >12+</v-chip>
                  <v-chip x-small v-else-if="movie.watch_grade==='전체 관람가'"
                         label color="#C9EBF4" class="mb-1"
                  >All</v-chip>
                  <v-chip x-small v-else-if="movie.watch_grade==='청소년 관람불가'"
                         label color="#BF3952" text-color="white" class="mb-1"
                  >18+</v-chip>
                  <v-chip x-small v-else
                          label color="lightpink"
                  >{{ movie.watch_grade }}</v-chip>
                  <v-chip label class="mb-1 ml-1" x-small color="#86D0EC">{{ movie.running_time }}</v-chip>
                  </div>
                  
                  <!-- <span> | {{movie.}}</span> -->
              </v-card-text>
            </v-col>
            <v-col class="reviewCount">
              리뷰
              {{movie.ratings_count}}
            </v-col>
          </v-row>
        </v-card>
            </v-col>
          </v-row>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
import router from '../../../router';
export default {
  name: 'TheaterMovie',
  props: ['CurrentList', 'Label'],
  methods: {
    goDetail(movieId) {
      router.push(`/movie/${movieId}`);
    },
    getMovieName(name) {
      if (name.length > 8) {
        return `${name.slice(0, 8)}...`;
      } else {
        return name;
      }
    }
  }
}
</script>

<style src="./CurrentList.css" scoped></style>