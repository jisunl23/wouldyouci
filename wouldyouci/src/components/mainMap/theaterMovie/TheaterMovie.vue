<template>
  <div>
    <v-chip
      class="ml-2 mb-2 mychip"
      color="mypink"
      label
      text-color="white"
      @click="goTheaterDetail(theaterId)"
    >
      <v-icon left>mdi-theater</v-icon>
      <span>{{ theaterName }}</span>
    </v-chip>
    <v-slide-group
      active-class="success"
      v-if="theaterMovieList && theaterMovieList.length"
    >
      <v-slide-item
        v-for="(movie, idx) in theaterMovieList"
        :key="idx"
      >
        <v-card
          class="ml-2 mr-2 mb-1 mycard"
          @click="goSite(movie.url)"
        >
          <v-row>
            <v-col class="col-5">
              <v-img
                :src="movie.movie.poster"
                class="card_image"
              >
              </v-img>
            </v-col>
            <v-col class="pl-1 ml-1">
              <v-list-item>
                <v-list-item-content class="pt-3 pb-4">
                  <v-list-item-title class="mytitle">{{ changeName(movie.movie.name) }}</v-list-item-title>
                  <v-list-item-subtitle v-if="movie.movie.name_eng" class="mysubtitle">{{ changeEngName(movie.movie.name_eng) }}</v-list-item-subtitle>
                  <v-list-item-content v-else class="mysubtitle2">.</v-list-item-content>
                </v-list-item-content>
              </v-list-item>

              <v-card-text class="detail">

                <div class="divseat ma-0">
                  <span class="spanstrong">{{ movie.start_time }}</span>
                  <span class="spanlight"> ~ {{ movie.end_time }}</span>
                </div>

                <div class="divfont dehighlight ma-0">
                  {{ changeCinemaName(movie.info) }}
                </div>

                <div class="divseat ma-0" v-if="theaterType==='기타'">
                  <span class="spanlight">예매가능</span>
                </div>
                <div class="divseat ma-0" v-else>
                  <span class="spancolor">{{ movie.seats }}</span>
                  <span class="spanstrong"> / {{ movie.total_seats }}석</span>
                </div>

                <v-chip x-small v-if="movie.movie.watch_grade==='15세 관람가'"
                        label color="#FCB5C7" class="mb-1"
                >15+</v-chip>
                  <v-chip x-small v-else-if="movie.movie.watch_grade==='12세 관람가'"
                         label color="#E9EA72" class="mb-1"
                  >12+</v-chip>
                  <v-chip x-small v-else-if="movie.movie.watch_grade==='전체 관람가'"
                         label color="#C9EBF4" class="mb-1"
                  >All</v-chip>
                  <v-chip x-small v-else-if="movie.movie.watch_grade==='청소년 관람불가'"
                         label color="#BF3952" text-color="white" class="mb-1"
                  >18+</v-chip>
                  <v-chip x-small v-else
                          label color="lightpink"
                  >{{ movie.movie.watch_grade }}</v-chip>
                <v-chip label class="chipfortime mb-1" x-small color="#86D0EC">{{ movie.movie.running_time }}</v-chip>

              </v-card-text>
            </v-col>
          </v-row>
        </v-card>
      </v-slide-item>
    </v-slide-group>
  <v-card
    class="ml-2 mr-2 mb-3 noItem"
    v-else
  >
    <div class="noMovie">
      <p>예매 가능한 영화가 없습니다.</p>
    </div>
  </v-card>
</div>
</template>

<script>
import router from '../../../router';
import { mapGetters } from 'vuex';

export default {
  name: 'TheaterMovie',
  props: ['theaterMovieList', 'theaterName', 'theaterType', 'theaterId'],
  computed: {
    ...mapGetters(['isLoggedIn'])
  },
  methods: {
    goSite(url) {
      window.open(url, "예매창", "fullscreen=yes");
    },
    changeName(info) {
      if (info.length > 7) {
        return `${info.slice(0, 7)}...`
      } else {
        return info
      }
    },
    changeEngName(info) {
      if (info.length > 19) {
        return `${info.slice(0, 19)}...`
      } else {
        return info
      }
    },
    changeCinemaName(info) {
      if (info.length > 16) {
        return `${info.slice(0, 16)}...`
      } else {
        return info
      }
    },
    goTheaterDetail(id) {
      if (this.isLoggedIn) {
        router.push(`/cinema/${id}`);
      } else {
        router.push('/signup');
      }
    }
  }
}
</script>

<style src="./TheaterMovie.css" scoped></style>