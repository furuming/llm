<script lang="ts" setup>
    const props = defineProps<{
        title:string
    }>( )

</script>

<template>
    <v-row>
        <v-col>
            <h1 class="text-display-middle">
                {{ props.title }}
            </h1>
        </v-col>
    </v-row>
</template>
