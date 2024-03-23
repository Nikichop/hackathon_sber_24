<template>
    <load-form class="mb-12"></load-form>
    <v-row 
      class="row"
    >
      <tasks-container 
        v-for="(value, index) in sortedTasksArray"
        :tasks="value"
        :index-number="index + 1"
      ></tasks-container>
    </v-row>
</template>
<script>
import { mapState } from 'pinia'
import { useMainStore } from '../store/mainStore';
import TaskCard from './TaskCard.vue';
import TasksContainer from './TasksContainer.vue';
import LoadForm from './LoadForm.vue'

export default {
  name: 'MainPage',
  components: {
    TaskCard,
    TasksContainer,
    LoadForm,
  },
  computed: {
    ...mapState(useMainStore, ['sortedTasksArray'])
  },
  methods: {
  }
}

</script>

<style>
.row {
  height: 100%;
  flex-wrap: nowrap;
}
</style>
