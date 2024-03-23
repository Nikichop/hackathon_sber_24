<template>
  <v-form>
    <v-container>
      <v-row>
        <v-col cols="6">
          <v-file-input
            ref="file"
            label="Выберите файл"
            show-size
            clearable
            v-model="file"
          ></v-file-input>
          <v-btn 
            class="mr-4"
            size="large"
            :disabled="!file?.length"
            @click="uploadFile(file[0])"
          >
            Загрузить файл
          </v-btn>
          <v-btn
            color="green"
            size="large"
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
import { mapActions } from 'pinia';
import { useMainStore } from '../store/mainStore'

export default {
  name: 'LoadForm',
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