import { defineStore } from "pinia";
import axios from 'axios';
import mapData from "./mapData";

export const useMainStore = defineStore('mainStore', {
  state: () => {
    return {
      serverUrl: 'http://localhost:8000/',
      sortedTasksArray: [],
      groups: ['Аля', 'Даля'],
      selectedGroup: '',
      isFileLoaded: false,
    }
  },
  actions: {
    async updateTasksList() {
      try {
        const response = await axios.post(`${this.serverUrl}upload`);
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
        );
        console.log(response);
        this.isFileLoaded = true;
      } catch (error) {
        alert(error)
      }
    }
  }
})