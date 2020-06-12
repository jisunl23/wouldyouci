<template>
  <div>
    <div class="label">
      <h4>{{ Label }}</h4>
    </div>
    <v-slide-group
      class="pa-2"
      active-class="success"
      v-if="pos && TheaterList.length"
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
      v-else-if="pos"
      class="noContent"
      height="20vh"
      width="86vw"
    >
      <div class="noContentExp">
        근처에 영화관이 없습니다.
      </div>
    </v-card>
    <v-card
      v-else
      class="noContent"
      height="20vh"
      width="86vw"
    >
      <div class="noContentExp">
        위치 정보를 허용해주세요.
      </div>
    </v-card>
  </div>
</template>

<script>
import router from '../../../router';
export default {
  name: 'TheaterMovie',
  props: ['TheaterList', 'Label', 'pos'],
  methods: {
    goDetail(id) {
      router.push(`/cinema/${id}`)
    },
    getTheaterName(name) {
      if (name.length > 10) {
        return `${name.slice(0, 10)}...`;
      } else {
        return name;
      }
    }
  }
}
</script>

<style src="./TheaterList.css" scoped></style>