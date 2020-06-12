<template>
  <div>
    <div class="label">
      <h4>{{ Label }}</h4>
    </div>
    <v-slide-group
      dark
      class="pa-4 pb-0"
      active-class="success"
      v-if="CinemaList && CinemaList.length"
    >
      <v-slide-item
        v-for="(cinema, idx) in CinemaList"
        :key="idx"
      >
        <div class="cinemaCard">
          <v-card
            class="poster"
            :style="{backgroundImage:`url(${cinema.poster})`}"
            @click="goDetail(cinema.id)"
          >
            
          </v-card>
          <div class="cinemaInfo">
            <h5>{{cinema.name}}</h5>
          </div>
        </div>
      </v-slide-item>
    </v-slide-group>
    <v-card
      v-else
      class="noContent"
      height="20vh"
      width="90vw"
      style="margin-right:2vh; margin-bottom:70px;"
    >
      <div class="noContentExp">
        해당 콘텐츠가 없습니다.
      </div>
    </v-card>
  </div>
</template>

<script>
import router from "@/router";

export default {
  name: 'MovieList',
  props: ["CinemaList",'Label'],
  methods: {
    goDetail(movieId) {
      router.push(`/movie/${movieId}`);
    },
    getMovieName(name) {
      if (name.length > 7) {
        return `${name.slice(0, 7)}...`;
      } else {
        return name;
      }
    }
  }
}
</script>

<style src="./MovieList.css" scoped></style>