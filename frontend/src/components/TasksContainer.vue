<template>
  <v-col class="flex_col">
    <h2 class="index_number">{{ indexNumber }}</h2>
    <div class="task_card">
      <task-card 
        v-for="value in tasks"
        :key="value.id"
        :task-title="value.title"
        :time="value.time"
        :employee="value.employee"
        :status="value.status"
        :startDate="value.startDate"
        :endDate="value.endDate"
        :url="value.url"
      ></task-card>
    </div>
  </v-col>
</template>

<script>
import TaskCard from './TaskCard.vue';

export default {
  name: 'TasksContainer',
  components: {
    TaskCard,
  },
  props: {
    tasks: {
      type: Array,
      default: [],
    },
    indexNumber: {
      type: Number,
      default: 1,
    }
  }
}
</script>

<style scoped>
.task_card {
  display: flex;
  flex-direction: column;
  justify-content: center;
  flex-grow: 10;
}
.flex_col {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border-right: dotted;
}
</style>