<template>
  <div class="body">
    <v-row no-gutters>
      <v-col class="item" cols="2">
        <span>
          개봉
        </span>
      </v-col>
      <v-col cols="10">
        <span class="content"
          >
          {{ details.open_date }}
        </span>
      </v-col>
    </v-row>

    <v-row no-gutters>
      <v-col class="item" cols="2">
        <span>
          장르
        </span>
      </v-col>
      <v-col cols="10">
        <span
          class="content"
          v-for="(genre, index) in details.genres"
          :key="index"
          >
          {{ genre }}
        </span>
      </v-col>
    </v-row>

    <v-row no-gutters>
      <v-col class="item" cols="2">
        <span>
          등급
        </span>
      </v-col>
      <v-col cols="10">
        <span
          class="content"
          >
          {{ details.watch_grade }} | {{ details.running_time }}
        </span>
      </v-col>
    </v-row>

    <v-row no-gutters>
      <v-col class="item" cols="2">
        <span>
          감독
        </span>
      </v-col>
      <v-col cols="10">
        <span 
          class="content"
          v-for="(director, index) in details.directors"
          :key="index"
          >
          {{ director }},
        </span>
      </v-col>
    </v-row>

    <v-row no-gutters>
      <v-col class="item" cols="2">
        <span>
          출연
        </span>
      </v-col>
      <v-col cols="10">
        <span 
          class="content"
          v-for="(actor, index) in details.actors"
          :key="index"
          >
          {{ actor }}, 
        </span>
      </v-col>
    </v-row>
    
  
    <v-row no-gutters>
      <v-col class="item" cols="2">
        <span>
          줄거리
        </span>
      </v-col>
      <v-col cols="10">
        <span class="content"
          v-bind:style="lineClamp" 
          @click.prevent="toggleSummaryClamp()"
          >
          {{ details.summary }}
        </span>
      </v-col>
    </v-row>
  </div>

</template>

<script>
export default {
  name: 'MovieInfo',
  props:["details"],
  data() {
    return {
      isHidden: true,
      lineClamp: {
        overflow: 'hidden',
        display: '-webkit-box',
        height: 'auto',
        '-webkit-box-orient': 'vertical',
        '-webkit-line-clamp': 3,
      }
    }
  },
  methods: {
    toggleSummaryClamp() {
      if ( this.isHidden == false) {
        this.isHidden = true;
        this.lineClamp = {
          overflow: 'hidden',
          display: '-webkit-box',
          height: 'auto',
          '-webkit-box-orient': 'vertical',
          '-webkit-line-clamp': 3,
        }
      } else {
        this.isHidden = false;
        this.lineClamp = {
          display: 'block',
          height: 'auto',
          '-webkit-box-orient': 'vertical',
          '-webkit-line-clamp': 'none',
        }
      }
    },
  }
}
</script>

<style src="./MovieInfo.css" scoped></style>