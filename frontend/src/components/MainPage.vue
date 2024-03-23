<template>
  <task-card></task-card>
</template>
<script>
import { mapState } from 'pinia'
import { useMainStore } from '../store/mainStore';
import TaskCard from './TaskCard.vue';

export default {
  name: 'MainPage',
  components: {
    TaskCard,
  },
  computed: {
    ...mapState(useMainStore, ['count'])
  },
  methods: {
  }
}

</script>

<style>
</style>
