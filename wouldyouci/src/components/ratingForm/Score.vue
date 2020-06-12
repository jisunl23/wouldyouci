<template>
   <v-rating
      class="score"
      :value=score
      background-color="amber lighten-3"
      color="amber"
      dense
      half-increments
      readonly
      ></v-rating>
</template>

<script>
export default {
  name: 'Score',
  props: ["score"],

}
</script>
