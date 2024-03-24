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
      isLoading: false,
    }
  },
  actions: {
    async updateTasksList() {
      try {
        this.isLoading = true;
        const response = await axios.post(`${this.serverUrl}light_weight_baby/${this.selectedGroup}`);
        this.sortedTasksArray = response.data.data;
        this.groups = response.data.groups;
      } catch (error) {
        alert(error)
      } finally {
        this.isLoading = false;
      }
    },
    async uploadFile(file) {
      try {
        this.isLoading = true;
        let formData = new FormData();
        formData.append('file', file);
        const response = await axios.post(
          `${this.serverUrl}upload/`, 
          formData,
        );
        this.sortedTasksArray = response.data.data;
        this.groups = response.data.groups;
        this.isFileLoaded = true;
      } catch (error) {
        alert(error)
      } finally {
        this.isLoading = false;
      }
    }
  }
})