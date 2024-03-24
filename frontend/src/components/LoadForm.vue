<template>
  <v-form>
    <v-container style="width: 1000px">
      <v-row>
        <v-col cols="6">
          <v-file-input
            ref="file"
            label="Выберите файл"
            show-size
            clearable
            v-model="file"
          ></v-file-input>
        </v-col>
        <v-col cols="6">
          <v-select
            label="Отобразить для"
            :items="groups"
            v-model="selectedGroup"
          ></v-select>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-btn 
              class="mr-4"
              size="large"
              :disabled="!file?.length && isLoading"
              @click="uploadFile(file[0])"
            >
              Загрузить файл
            </v-btn>
        </v-col>
        <v-col>
          <v-btn
            color="green"
            size="large"
            :disabled="!selectedGroup && !isFileLoaded && isLoading"
            @click="updateTasksList"
          >
            Обновить
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </v-form>
</template>

<script>
import { mapActions, mapState, mapWritableState } from 'pinia';
import { useMainStore } from '../store/mainStore'

export default {
  name: 'LoadForm',
  computed: {
    ...mapState(useMainStore, ['groups', 'isFileLoaded', 'isLoading']),
    ...mapWritableState(useMainStore, ['selectedGroup']),
  },
  data() {
    return {
      file: null,
    }
  }, 
  methods: {
    ...mapActions(useMainStore, [
      'uploadFile', 
      'updateTasksList'
    ]),
  }
}

</script>

<style scoped>

</style>