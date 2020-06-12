<template>
  <v-card>
    <v-tabs
      v-model="tab"
      background-color="white"
      color="primary"
      light
      right
      >
      <v-tab
        v-show="item.content.length"
        v-for="(item, idx) in items"
        :key="idx"
        >
        {{ item.tab }}
      </v-tab>
    </v-tabs>

    <v-tabs-items v-model="tab">
      <v-tab-item
        v-for="(item, idx) in items"
        :key="idx"
        >
        <v-timeline
          dense
          clipped
          >
          <v-timeline-item
            v-for="(movie, idx) in item.content"
            :key="idx"
            small
          >
          <template v-slot:icon>
            <router-link :to="{ name: 'MovieDetail', params: {id: movie.movie.id}}">
            <v-avatar
              >
              <v-img
                :src="movie.movie.poster"
              ></v-img>
            </v-avatar>
          </router-link>
          </template>
            <v-row 
              no-gutters
              align="center"
              justify="center"
              >
              <v-col 
                class="time" 
                cols="4">
                <strong>{{ formatTime(movie.start_time)}}</strong>
                  ~{{ formatTime(movie.end_time) }}
              </v-col>
              <v-col>
                <strong>{{ movie.movie.name }}</strong>
                <div class="caption mb-2">
                  <p class="content">
                    {{ movie.info }}
                  </p>
                  <p class="content">
                    {{ movie.seats }} / {{movie.total_seats}}석
                  </p>
                </div>
              </v-col>
            </v-row>
          </v-timeline-item>
        </v-timeline>
      </v-tab-item>
    </v-tabs-items>
    <v-row>
      <v-spacer></v-spacer>
      <v-btn color="blue darken-1" text @click="closeMe">Close</v-btn>
    </v-row>
  </v-card>
</template>


<script>
import { mapGetters, } from 'vuex';

  export default {
    name: 'CinemaOnScreens',
    props: ["onscreens"],
    data () {
      return {
        tab: null,
        items: [],
      }
    },

    created() {
      var dayjs = require('dayjs')
      var dates = this.onscreens.map(function(movie) {
        return dayjs(movie.date)
      });

      var minMax = require('dayjs/plugin/minMax')
      dayjs.extend(minMax)
      var recentDate = dayjs.min(dates);
      var latestDate = dayjs.max(dates);

      var j = 0;
      var newDate = dayjs(recentDate).clone().add(j, 'days');
      var isSameOrBefore = require('dayjs/plugin/isSameOrBefore')
      dayjs.extend(isSameOrBefore)
      while ( newDate.isSameOrBefore(latestDate)) {
        this.items.push({tab: dayjs(newDate).format('YYYY.MM.DD'), content: []});
        j++;
        newDate = recentDate.clone().add(j, 'd');
      }

      for ( var i in this.items ) {
        const item = this.items[i]
        const date = dayjs(item.tab).format('YYYY-MM-DD')
        item.content = this .onscreens.filter(movie => movie.date == date)
      }
    },


    computed: {
      ...mapGetters({
      details: 'getCinemaDetail',
      }),
      
      
    },

    methods: {
      closeMe() {
      this.$emit("close");
      },
      formatDate(date) {
      var moment = require('moment');
      return moment(date).format('YYYY.MM.DD')
      },
      formatTime(time) {
      var moment = require('moment');
      return moment(time, 'kk:mm:ss').format('hh:mm')
      },

      getMoviesByDate(date) {
        var moviesOnTheDay = []
        for ( var movie in this.onscreens ) {
          if (movie.date == date) {
            moviesOnTheDay.push(movie)
          }
        }
        return moviesOnTheDay
      },
    },
  }
</script>


<style src="./CinemaInfo.css" scoped></style>