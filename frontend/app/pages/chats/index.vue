<script setup lang="ts">
import PageTitle from '~/components/PageTitle.vue';


const auth = useAuth()
definePageMeta({
  middleware: ['auth'],
})

const chats = ref()


</script>


<template>
    <PageTitle title="チャット"></PageTitle>


</template>