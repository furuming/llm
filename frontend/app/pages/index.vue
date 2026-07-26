<script lang="ts" setup>

const auth = useAuth()
definePageMeta({
  middleware: ['auth', ],
})


</script>


<template>

  TOP

  <v-container fluid class="fill-height d-flex justify-center align-center">
    <v-card width="400">
      <v-card-title class="py-4">
      </v-card-title>

      <v-card-text>
        
      </v-card-text>
    </v-card>
  </v-container>
</template>