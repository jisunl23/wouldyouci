<template>
  <div class="afterSearch">
    <div v-if="ResultList.length || Similar.length">
      <div v-if="ResultList.length">
        <div class="keyword">
          "{{ KeyWords }}" 에 대한 검색 결과입니다.
        </div>
        <CinemaList v-if="Type==='movies'" v-bind:CinemaList="ResultList" />
        <TheaterList v-else v-bind:pos="true" v-bind:TheaterList="ResultList" />
      </div>
      <div v-if="ResultList.length && Similar.length">
        <v-divider
          style="margin-bottom:2vh;"
        ></v-divider>
      </div>
      <div v-if="Similar.length">
        <div class="keyword">
          "{{ KeyWords }}" 에 대한 유사 검색 결과입니다.
        </div>
        <CinemaList v-if="Type==='movies'" v-bind:CinemaList="Similar" />
        <TheaterList v-else v-bind:TheaterList="Similar" />
      </div>
    </div>
    <div v-else>
      <div class="keyword" style="margin-bottom: 3vh;">
        "{{ KeyWords }}" 에 대한 검색 결과과 없습니다.
      </div>
    </div>
  </div>
</template>

<script>
import CinemaList from '../cinemaList/CinemaList.vue';
import TheaterList from '../cinemaList/TheaterList.vue';

export default {
   name: 'AfterSearch',
   props: ['KeyWords', 'ResultList', 'Similar', 'Type'],
   components: {
     CinemaList,
     TheaterList
   }
}
</script>

<style src="./AfterSearch.css" scoped></style>