<script lang="ts" setup>

</script>


<template>
  <v-container fluid class="fill-height d-flex justify-center align-center">
    <v-card width="400">
      <v-card-title class="py-4">
        ログイン
      </v-card-title>

      <v-card-text>
        <v-text-field label="ID">
        </v-text-field>
        <v-text-field label="password" type="password">
        </v-text-field>

        <v-row>
            <v-col>
                <v-btn to="/register">新規登録</v-btn>
            </v-col>
            <v-col class="text-right">
                <v-btn>ログイン</v-btn>
            </v-col>
        </v-row>

      </v-card-text>
    </v-card>
  </v-container>
</template>