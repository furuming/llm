<script lang="ts" setup>

const email = ref("")
const password = ref("")


const login = async () => {
    
    try{

        const ret = await $fetch("/api/login", {
            method: "POST",
            body: {
                email: email.value,
                password: password.value,
            }
        })
        await navigateTo("/")
    } catch( e ){
        alert(e)
    }

}

</script>


<template>
  <v-container fluid class="fill-height d-flex justify-center align-center">
    <v-card width="400">
      <v-card-title class="py-4">
        ログイン
      </v-card-title>

      <v-card-text>
        <v-text-field label="email" v-model="email">
        </v-text-field>
        <v-text-field label="password" type="password" v-model="password">
        </v-text-field>

        <v-row>
            <v-col>
                <v-btn to="/register">新規登録</v-btn>
            </v-col>
            <v-col class="text-right" @click="login">
                <v-btn>ログイン</v-btn>
            </v-col>
        </v-row>

      </v-card-text>
    </v-card>
  </v-container>
</template>