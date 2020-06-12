<template>
  <div>
    <div class="content">
      <TheaterList v-bind:Label="'근처 영화관'" v-bind:pos="pos" v-bind:TheaterList="TheaterList" />
    </div>
    <div class="released">
      <CinemaList v-bind:Label="'상영예정작'" v-bind:CinemaList="Commings" />
    </div>
    <div class="current">
      <CurrentList v-bind:Label="'화제의 상영작 순위'" v-bind:CurrentList="Populars" />
    </div>
  </div>
</template>

<script>
import CinemaList from '../cinemaList/CinemaList.vue';
import TheaterList from '../cinemaList/TheaterList.vue';
import CurrentList from '../cinemaList/CurrentList';

export default {
   name: 'Search',
   components: {
     CinemaList,
     TheaterList,
     CurrentList
   },
   props:['Commings', 'Populars', 'TheaterList', 'pos']


}
</script>

<style src="./MainSearch.css" scoped></style>