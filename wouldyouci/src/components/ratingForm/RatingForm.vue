<template>
  <div class="ratingForm">
    <div class="score">
      <v-rating
        v-model="rating.score"
        color="elsepink"
        background-color="pink lighten-4"
        half-increments
        hover
        size="18">
        </v-rating>
    </div>
    <div class="comment">
      <v-textarea
        v-model="rating.comment"
        clearable
        clear-icon="fas fa-times xsmall"
        elsepink
        label="관람평"
        rows="1"
        auto-grow
        hide-details="auto"
        color="fontgrey"
        dense
      ></v-textarea>
      <v-btn 
        class="button"
        color="elsepink" 
        icon
        text 
        @click.prevent="submitForm(rating)"
      >등록</v-btn>
    </div>

  </div>
</template>

<script>


export default {
  name: "RatingForm",
  components: {
    },
  data() {
    return {
      rules: [
        value => !!value || '점수를 입력해주세요.',
        value => ( value <= 5 ) || '최고 점수는 5점입니다.',
        value => ( value < 0.5 ) || '최저 점수는 0.5점입니다.',
      ],
      rating: {
        score: 0.5,
        comment: '',
      },
    }
  },
  methods: {

    async submitForm(rating) {
      await this.$emit("submitRating", rating);
      this.rating.score = 0;
      this.rating.comment = '';
    },    
  },
}
</script>
<style src="./RatingForm.css" scoped></style>