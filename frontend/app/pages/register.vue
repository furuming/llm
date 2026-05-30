<script lang="ts" setup>

const name = ref("")
const email = ref("")
const password = ref("")
const password_confirm = ref("")


const registerUser = () => {
    const ret = $fetch("/api/users/register", {
        method: "POST",
        body: {
            name: name.value,
            email: email.value,
            password: password.value,
        }
    })

}

</script>


<template>
  <v-container fluid class="fill-height d-flex justify-center align-center">
    <v-card width="700">
      <v-card-title class="py-4">
        新規登録
      </v-card-title>

      <v-card-text>
        <v-form>

            <v-text-field label="name" v-model="name">
            </v-text-field>
            <v-text-field label="email" type="email" v-model="email">
            </v-text-field>
            
            <v-text-field label="password" type="password" v-model="password">
            </v-text-field>
            
            <v-text-field label="password_confirmation" type="password" v-model="password_confirm">
            </v-text-field>
            
            <v-row class="py-4">
                <v-col>
                    <v-btn to="/">戻る</v-btn>
                </v-col>
                <v-col class="text-right">
                    <v-btn @click="registerUser" color="primary">登録</v-btn>
                </v-col>
            </v-row>
        </v-form>

      </v-card-text>
    </v-card>
  </v-container>
</template>