<template>
  <v-col class="flex_col">
    <h2 class="index_number">{{ indexNumber }}</h2>
    <div class="task_card">
      <task-card 
        v-for="value in tasks"
        :key="value.key"
        :id="value.key"
        :task-title="value.name"
        :cost="value.cost"
        :employee="value.assignee"
        :status="value.status"
        :startDate="value.dateStart"
        :endDate="value.dateEnd"
        :depends-on=value.dependsOn
        :url="value.url"
        :group="value.group"
        :risk="value.risk"
        :progress="value.progress"
        ref="cards"
        @focus-card="onFocus"
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
  },
  methods: {
    onFocus(taskKey) {
      this.$emit('focus-card', taskKey);
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