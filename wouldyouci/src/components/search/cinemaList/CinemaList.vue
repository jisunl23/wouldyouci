<template>
  <div>
    <div class="label">
      <h4>{{ Label }}</h4>
    </div>
    <v-slide-group
      class="pa-2 cinemaList"
      active-class="success"
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
  </div>
</template>

<script>
import router from '../../../router';
export default {
  name: 'TheaterMovie',
  props: ['CinemaList', 'Label'],
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

<style src="./CinemaList.css" scoped></style>