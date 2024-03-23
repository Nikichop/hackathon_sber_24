<template>
    <v-card
      max-width="600"
      width="400"
      variant="outlined"
      class="ma-12"
    >
      <v-expansion-panels>
        <v-expansion-panel>
          <v-expansion-panel-title style="background-color: aqua;">
            {{ taskTitle }}
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
                <v-card-text v-if="param.name === 'Ссылка на задачу'">
                  <a :href="param.value">{{ param.value }}</a>
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
    taskTitle: {
      type: String,
      default: 'Название задачи ',
    },
    allocatedTime: {
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
    url: {
      type: String,
      default: 'https://www.prostospb.team/hackathon-sber24'
    }
  },
  data() {
    return {
      statuses: {
        inWork: 'В работе',
        done: 'Сделан',
        open: 'Открыт',
      },
      colors: {

      }
    }
  },
  computed: {
    getStatus() {
      return this.statuses[this.status];
    },
    getColorTitle() {
      return 
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
          value: this.allocatedTime,
        },
        {
          name: 'Ссылка на задачу',
          value: this.url,
        },
      ]
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
</style>