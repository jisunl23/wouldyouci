<template>
  <div >
    <v-img v-if="!details.poster"
      class="poster"
      src="../../../assets/defaultImg.jpg" />

    <div v-else>
      <div class="poster-container"
        >
        <v-img
          @click.stop="dialog = true"
          class="poster"
          :src="details.poster">
          <v-icon
            v-show="details.trailer"
            class="play-button"
            color="primary"
            x-large 
            >
            mdi-play-circle-outline
          </v-icon>
        </v-img>
      </div>
      <v-dialog v-if="details.trailer"
        v-model="dialog"
        min-width="290"
        >
        <v-card class="trailer-container">
          <iframe 
            class="trailer"
            :src="details.trailer"
            allowfullscreen
            frameborder="0"
            ></iframe>
          <v-btn
            color="primary"
            icon
            @click="dialog = false"
            >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card>
      </v-dialog>
    </div>
  </div>
</template>

<script>

export default {
  name: "MovieTrailer",
  props: ["details"],
  data() {
    return {
      dialog: false,
      trailerLoaded: false,
    }
  },

  methods: {
  },

}
</script>

<style src="./MovieTrailer.css" scoped></style>