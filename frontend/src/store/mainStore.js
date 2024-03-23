import { defineStore } from "pinia";
import axios from 'axios';

export const useMainStore = defineStore('mainStore', {
  state: () => {
    return {
      serverUrl: 'http://localhost:8000/',
      sortedTasksArray: [
        [
          {
            id: 1,
            title: 'Оформить заказ',
            status: 'inWork',
            time: '100д 45ч 50м',
            employee: 'Иванов Иван Иванович',
            startDate: '23.03.2024',
            endDate: '25.03.2024',
            url: 'https://www.prostospb.team/hackathon-sber24',
            team: {
              id: 1,
              name: 'Команда 1',
            }
          },
          {
            id: 2,
            title: 'Просмотреть инструкцию',
            status: 'inWork',
            time: '100д 45ч 50м',
            employee: 'Сергеев Сергей Сергеевич',
            startDate: '23.03.2024',
            endDate: '25.03.2024',
            url: 'https://www.prostospb.team/hackathon-sber24',
            team: {
              id: 2,
              name: 'Команда 2',
            }
          },
        ],
        [
          {
            id: 3,
            title: 'Доставка',
            status: 'inWork',
            time: '100д 45ч 50м',
            employee: 'Как Такович',
            startDate: '25.03.2024',
            endDate: '27.03.2024',
            url: 'https://www.prostospb.team/hackathon-sber24',
            team: {
              id: 2,
              name: 'Команда 2',
            }
          },
          {
            id: 4,
            title: 'Собрать каркас',
            status: 'inWork',
            time: '100д 45ч 50м',
            employee: 'Каркасович',
            startDate: '25.03.2024',
            endDate: '27.03.2024',
            url: 'https://www.prostospb.team/hackathon-sber24',
            team: {
              id: 1,
              name: 'Команда 1',
            }
          },
        ],
        [
          {
            id: 1,
            title: 'Оформить заказ',
            status: 'inWork',
            time: '100д 45ч 50м',
            employee: 'Иванов Иван Иванович',
            startDate: '23.03.2024',
            endDate: '25.03.2024',
            url: 'https://www.prostospb.team/hackathon-sber24',
            team: {
              id: 1,
              name: 'Команда 1',
            }
          },
          {
            id: 2,
            title: 'Просмотреть инструкцию',
            status: 'inWork',
            time: '100д 45ч 50м',
            employee: 'Сергеев Сергей Сергеевич',
            startDate: '23.03.2024',
            endDate: '25.03.2024',
            url: 'https://www.prostospb.team/hackathon-sber24',
            team: {
              id: 2,
              name: 'Команда 2',
            }
          },
        ],
        [
          {
            id: 3,
            title: 'Доставка',
            status: 'inWork',
            time: '100д 45ч 50м',
            employee: 'Как Такович',
            startDate: '25.03.2024',
            endDate: '27.03.2024',
            url: 'https://www.prostospb.team/hackathon-sber24',
            team: {
              id: 2,
              name: 'Команда 2',
            }
          },
          {
            id: 4,
            title: 'Собрать каркас',
            status: 'inWork',
            time: '100д 45ч 50м',
            employee: 'Каркасович',
            startDate: '25.03.2024',
            endDate: '27.03.2024',
            url: 'https://www.prostospb.team/hackathon-sber24',
            team: {
              id: 1,
              name: 'Команда 1',
            }
          },
        ],
      ],
    }
  },
  actions: {
    async updateTasksList() {
      try {
        const response = await axios.get(`${this.serverUrl}upload`);
        console.log(response)
        //this.sortedTasksArray = response.data;
      } catch (error) {
        alert(error)
      }
    },
    async uploadFile(file) {
      try {
        let formData = new FormData();
        formData.append('file', file);
        const response = await axios.post(
          `${this.serverUrl}upload/`, 
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data'
            },
          }
        );
        console.log(response);
      } catch (error) {
        alert(error)
      }
    }
  }
})