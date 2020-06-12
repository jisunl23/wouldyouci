<template>
  <div>
    <div class="label">
      <h4>{{ Label }}</h4>
    </div>
    <v-slide-group
      class="pa-2 pl-4 pb-10"
      active-class="success"
      v-if="TheaterList && TheaterList.length"
    >
      <v-slide-item
        v-for="(theater, idx) in TheaterList"
        :key="idx"
      >
        <div class="theaterinfo">
          <v-card
            class="card"
            height="15vh"
            width="40vw"
            @click="goDetail(theater.id)"
            :style="{backgroundImage:`url(${theater.img})`}"
          >
        </v-card>
        <h5>{{getTheaterName(theater.name)}}</h5>
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
import router from '../../../router';
export default {
  name: 'TheaterMovie',
  props: ['TheaterList', 'Label'],
  methods: {
    goDetail(id) {
      router.push(`/cinema/${id}`)
    },
    getTheaterName(name) {
      if (name.length > 8) {
        return `${name.slice(0, 8)}...`;
      } else {
        return name;
      }
    }
  }
}
</script>

<style src="./TheaterList.css" scoped></style>