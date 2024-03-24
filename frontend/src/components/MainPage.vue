<template>
    <load-form class="mb-12"></load-form>
    <v-row 
      class="row"
    >
      <tasks-container 
        v-for="(value, index) in sortedTasksArray"
        :tasks="value"
        :index-number="index + 1"
        ref="containers"
        @focus-card="onFocus"
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
    onFocus(taskKey) {
      let element = null;
      this.$refs.containers.forEach(container => {

        if (element) {
          return;
        }

        container.$refs.cards.forEach(c => {
          c.isFocused = false;

          if (c.id === taskKey) {
            element = c;
          }
        });
      })

      element.changeIsFocused();
    }
  }
}

</script>

<style>
.row {
  height: 100%;
  flex-wrap: nowrap;
}
</style>
