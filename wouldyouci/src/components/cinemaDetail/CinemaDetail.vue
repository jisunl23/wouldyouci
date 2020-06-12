<template>
  <div class="body">

    <Title />
    
    <div class="body">
    
      <div class="image">
        <v-img
          v-if="details.img"
          class="media" 
          :src="details.img"
          >
        </v-img>
        <v-img 
          v-else
          class="media"
          aspect-ratio=1.7
          src="../../assets/defaultImg.jpg">
          <template v-slot:placeholder>
            <div>
              이미지 준비중
            </div>
          </template>
        </v-img>
      </div>

      <div class="details">

        <v-list-item two-line>
          <v-list-item-content>
            <v-list-item-title class="headline">{{ details.name }}</v-list-item-title>
            <v-list-item-subtitle>{{ details.address }}</v-list-item-subtitle>
            <v-list-item-subtitle>
              <a 
                class="tel"
                :href="`tel:+${ details.tel }`">
                {{ details.tel }}
              </a>
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>

        <div class="right">
          <v-btn 
            icon 
            :color="(isPicked) ? 'elsepink' : 'lightgrey'"
            @click.prevent="togglePickCinema">
            <v-icon v-show="isPicked">mdi-heart</v-icon>
            <span v-show="!isPicked">찜</span>
            <v-icon v-show="!isPicked">mdi-plus</v-icon>
          </v-btn>
          <v-btn
            icon
            target="_blank"
            :href="details.url" 
            >
            <v-icon>mdi-home</v-icon>
          </v-btn>
          <v-dialog v-model="dialog">
            <template v-slot:activator="{ on }">
              <v-btn
                v-on="on"
                icon 
                color="titleblue"
                >
                <v-icon>mdi-filmstrip</v-icon>
              </v-btn>
            </template>
            <CinemaOnScreens :onscreens="details.onscreens" @close="closeModal" />
          </v-dialog>
        </div>
      </div>

      <div class="tab-card">
        <v-tabs
          v-model="tab"
          background-color="transparent"
          centered
          fixed-tabs
          >
          <v-tab
            v-for="item in items"
            :key="item.tab"
            >
            {{ item.tab }}
          </v-tab>
        </v-tabs>
        <v-tabs-items v-model="tab">
          <v-tab-item
            v-for="item in items"
            :key="item.tab"
            >
            <v-card flat>
              <v-card-text>
                <component 
                  class="tab-item"
                  v-bind:is="item.component" 
                  :details="details"
                  ></component>
              </v-card-text>
            </v-card>
          </v-tab-item>
        </v-tabs-items>
      </div>
    </div>
  </div>

</template>

<script>
import Title from '../nav/Title.vue';
import CinemaInfo from './cinemaInfo/CinemaInfo';
import CinemaRatings from './cinemaRatings/CinemaRatings';
import CinemaOnScreens from './cinemaInfo/CinemaOnScreens';
import Score from '../ratingForm/Score';
import { mapGetters, mapActions } from 'vuex';


export default {
  name: 'CinemaDetail',
  components: {
    Title,
    CinemaInfo,
    CinemaRatings,
    Score,
    CinemaOnScreens,
  },

  data() {
    return {
      tab: null,
      items: [
        {tab: 'Info', component: "CinemaInfo"},
        {tab: 'Reviews', component: "CinemaRatings"}
      ],
      expand: false,
      isPicked: false,
      dialog: false,
    }
  },
  
  async created() {
    await this.fetchCinemaDetail(this.$route.params.id);
    if (this.details.pick_cinemas) {
      this.isPicked = true
    }
  },

  computed: {
    ...mapGetters({
      details: 'getCinemaDetail',
      }),
  },

  methods: {
    ...mapActions(['fetchCinemaDetail', 'togglePick', ]),
    async togglePickCinema() {
      const item = 'cinema'
      const itemId = this.details.id
      await this.togglePick({item, itemId})
      this.isPicked = !this.isPicked
    },
    closeModal() {
      this.dialog = false;
    },

  },

}
</script>


<style src="./CinemaDetail.css" scoped></style>