<template>
    <v-card
      max-width="600"
      width="400"
      variant="outlined"
      class="ma-12"
      ref="panel"
      :style="isFocused ? 'border-color: orange; border-width: medium' : ''"
    >
      <v-expansion-panels>
        <v-expansion-panel focusable>
          <v-expansion-panel-title style="background-color: aqua;">
            <div style="width: 80%;">
              <h4>{{ group }}</h4>
              <h3>{{ id }}: {{ taskTitle }}</h3>
              <v-progress-linear
                :model-value="progress"
                class="mt-2"
                color="black"
                height="6"
              ></v-progress-linear>
            </div>
          </v-expansion-panel-title>
          <v-expansion-panel-text>
            <v-row 
              v-for="param in getParametrs"
              :key="param.name"
            >
              <v-col>
                <v-card-text>{{ param.name }}:</v-card-text>
              </v-col>
              <v-col cols="6">
                <v-card-text v-if="param.name === 'Статус'">
                  <v-icon
                    :icon="param.value.icon"
                    :color="param.value.color"
                  ></v-icon>
                  {{ param.value.text }}
                </v-card-text>
                <v-card-text v-else-if="param.name === 'Ссылка на задачу'">
                  <a :href="param.value" target="_blank">{{ param.value }}</a>
                </v-card-text>
                <v-card-text v-else-if="param.name === 'Зависит от'">
                  <span
                    v-for="(taskKey, index) in param.value"
                    :key="taskKey"
                  >
                    <a
                      href=""
                      @click.prevent="focusPanel(taskKey)"
                    >
                      {{ taskKey }}
                    </a>{{ index !== param.value.length - 1 ? ', ' : '' }}
                  </span>
                </v-card-text>
                <v-card-text v-else>
                  {{ param.value }}
                </v-card-text>
              </v-col>
            </v-row>
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-card>
</template>

<script>
export default {
  name: 'TaskCard',
  props: {
    id: {
      type: String,
      default: '',
    },
    taskTitle: {
      type: String,
      default: 'Название задачи',
    },
    cost: {
      type: [String, Number],
      default: '99 д 24ч 40м'
    },
    employee: {
      type: String,
      default: 'Иванов Иван Иванович',
    },
    status: {
      type: String,
      default: 'inWork',
    },
    startDate: {
      type: String,
      default: '23.03.2024',
    },
    endDate: {
      type: String,
      default: '24.03.2024',
    },
    dependsOn: {
      type: Array,
      default: [],
    },
    risk: {
      type: Number,
      default: 0,
    },
    url: {
      type: String,
      default: 'https://www.prostospb.team/hackathon-sber24'
    },
    group: {
      type: String,
      default: '',
    },
    progress: {
      type: Number,
      default: 0,
    }
  },
  data() {
    return {
      statuses: {
        inProgress: {
          text: 'В работе',
          icon: 'mdi-timeline-clock-outline',
          color: 'orange',
        },
        done: {
          text: 'Завершен',
          icon: 'mdi-timeline-check-outline',
          color: 'green',
        },
        open: { 
          text: 'Не начато',
          icon: 'mdi-timeline-outline',
          color: 'black',
        },
        needInfo: {
          text: 'Нужна информация',
          icon: 'mdi-information',
          color: 'black',
        }
      },
      isFocused: false,
    }
  },
  computed: {
    getStatus() {
      return this.statuses[this.status];
    },
    getColorTitle() {
      return 
    },
    getDependsOn() {
      return this.dependsOn
    },
    getParametrs() {
      return [
        {
          name: 'Статус',
          value: this.getStatus,
        },
        {
          name: 'Дата начала',
          value: this.startDate,
        },
        {
          name: 'Дата окончания',
          value: this.endDate,
        },
        {
          name: 'Исполнитель',
          value: this.employee,
        },
        {
          name: 'Выделенное время',
          value: this.cost,
        },
        {
          name: 'Ссылка на задачу',
          value: this.url,
        },
        {
          name: 'Зависит от',
          value: this.dependsOn,
        },
        {
          name: 'Риск',
          value: this.risk,
        }
      ]
    }
  },
  methods: {
    focusPanel(taskKey) {
      this.$emit('focus-card', taskKey);
    },
    changeIsFocused() {
      this.isFocused = !this.isFocused;
    }
  }
}
</script>

<style scope>
.v-card-text {
  padding: 0;
}
.v-row {
  margin-top: 0,
}
.v-card {
  border-width: medium
}
</style>