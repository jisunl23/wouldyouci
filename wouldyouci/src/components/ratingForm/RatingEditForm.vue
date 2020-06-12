<template>
  <div class="ratingForm">
    <v-card>
      <v-card-title>
        <div class="score">
          <v-rating
            v-model="editedRating.score"
            color="blackpink"
            background-color="blackpink"
            half-increments
            hover
            size="18">
            </v-rating>
        </div>
      </v-card-title>

      <v-card-text>
        <div class="comment">
          <v-textarea
            v-model="editedRating.comment"
            clearable
            clear-icon="fas fa-times xsmall"
            label="관람평"
            rows="1"
            auto-grow
            hide-details="auto"
            color="fontgrey"
            dense
          ></v-textarea>
        </div>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="lightgrey" text @click="closeMe">Close</v-btn>
        <v-btn color="blackpink" text @click="submit(editedRating)">Save</v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>


export default {
  name: "RatingEditForm",
  props:["rating", "index"],
  data() {
    return {
      rules: [
        value => !!value || '점수를 입력해주세요.',
        value => ( value <= 5 ) || '최고 점수는 5점입니다.',
        value => ( value < 0.5 ) || '최저 점수는 0.5점입니다.',
      ],
      editedRating: {
        id: this.rating.id,
        score: this.rating.score,
        comment: this.rating.comment,
        user: this.rating.user,
        index: this.index,
      },
    }
  },
  methods: {
    closeMe() {
      this.$emit("close");
    },
    submit(editedRating) {
     this.$emit("editRating", editedRating);
    },    
  },
}
</script>
<style src="./RatingForm.css" scoped></style>