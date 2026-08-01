<script lang="ts" setup>

const auth = useAuth()
definePageMeta({
  middleware: ['auth' ],
})


</script>


<template>

  <h1>
    TOP
  </h1>

  <v-card width="">
    <v-card-title class="py-4">
      メニュー
      </v-card-title>

      <v-card-text>
        <v-container fluid class="fill-height d-flex justify-center align-center">
        <v-row>
          <v-col cols="4">
            <v-btn href="/chats">チャット</v-btn>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="4">
            <v-btn href="/files">ファイル管理</v-btn>
          </v-col>
        </v-row>
      </v-container>
        
      </v-card-text>
    </v-card>
</template>