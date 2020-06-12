<template>
  <v-card class="timeCard">
    <v-container fluid class="mb-0 pb-0">
      <v-card-subtitle class="mysubtitle">
        설정한 시간 이후의 영화를 조회합니다.
      </v-card-subtitle>
      <v-row>
          <v-select class="mt-3 ml-4 mr-4" dense v-model="targetType" :items="type" outlined label="오전/오후"/>
          <v-select class="ml-4 mr-4" dense v-model="targetHours" :items="hours" outlined label="시간"/>
          <v-select class="ml-4 mr-4" dense v-model="targetMins" :items="mins" outlined label="분"/>
      </v-row>
    </v-container>
    <v-card-actions>
      <v-spacer/>
      <v-btn class="pt-0 pb-4 pr-4" text color="deep-purple accent-4" @click="closeTimeSelector(`${targetType} ${targetHours}:${targetMins}:00`)">SUBMIT</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
// import { mapActions } from 'vuex';

export default {
  name: 'settingCard',
  props: ['nowTime'],
  data() {
    return{
      type: [
        '오전',
        '오후'
      ],
      hours: [
        '1',
        '2',
        '3', 
        '4',
        '5', 
        '6',
        '7',
        '8',
        '9',
        '10',
        '11',
        '12'
      ],
      mins: [
        '00', 
        '10', 
        '20',
        '30',
        '40',
        '50'
      ],
      targetType: null,
      targetHours: null,
      targetMins: null
    }
  },
  methods: {
    closeTimeSelector(targetTime) {
      this.$emit('targetTime', targetTime);
      this.targetType = null;
      this.targetHours = null;
      this.targetMins = null;
    },
  }
}
</script>

<style src="./TimeSelector.css" scoped></style>