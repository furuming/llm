<script setup lang="ts">
import { useChatApi } from '~/composables/api/useChatApi'
import type { ChatMessage } from '~/types/Chat'



const auth = useAuth()
definePageMeta({
  middleware: ['auth'],
})

// チャット履歴の状態管理
const messages = ref<ChatMessage[]>([])
const newMessage = ref('')
const isLoading = ref(false)

// APIの初期化
const { sendMessage } = useChatApi()

const handleSendMessage = async () => {
  if (!newMessage.value.trim() || isLoading.value) return

  const content = newMessage.value
  newMessage.value = ''

  // ユーザーのメッセージを履歴に追加
  messages.value.push({
    id: Date.now().toString(),
    role: 'user',
    content: content,
    created_at: new Date()
  })

  isLoading.value = true
  try {
    // APIを叩いてAIの回答を取得
    const response = await sendMessage(content)
    
    // AIのメッセージを履歴に追加
    messages.value.push({
      id: (Date.now() + 1).toString(),
      role: 'assistant',
      content: response,
      created_at: new Date()
    })
  } catch (error) {
    console.error('Error sending message:', error)
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <v-container fluid class="fill-height">
    <PageTitle title="チャット"></PageTitle>

    <v-card class="mx-auto overflow-auto" max-width="900" height="calc(90vh - 150px)" elevation="2">
      <v-card-title color="primary" class="bg-primary">
        Chat Session
      </v-card-title>

      <v-card-text class="fill-height  pa-4">
        <div v-for="msg in messages" :key="msg.id" 
             :class="['mb-4 d-flex flex-column', msg.role === 'user' ? 'align-end' : 'align-start']">
          
          <v-chip size="x-small" :color="msg.role === 'user' ? 'blue' : 'grey'" class="mb-1">
            {{ msg.role === 'user' ? 'You' : 'AI' }}
          </v-chip>
          
          <v-card
            :color="msg.role === 'user' ? 'blue-lighten-5' : 'grey-lighten-4'"
            class="pa-3 rounded-lg"
            :width="msg.role === 'user' ? '70%' : '70%'"
            :class="msg.role === 'user' ? 'ml-auto' : 'mr-auto'"
          >
            <div class="text-body-1">{{ msg.content }}</div>
            <div class="text-caption mt-1">{{ msg.created_at.toLocaleTimeString() }}</div>
          </v-card>
        </div>

        <div v-if="isLoading" class="d-flex align-center mt-4">
          <v-progress-circular indeterminate color="primary" size="20" class="mr-2" />
          <span class="text-caption">AIが考えています...</span>
        </div>
      </v-card-text>
      <v-divider></v-divider>

      <v-card-actions class="pa-4">
        <v-text-field
          v-model="newMessage"
          placeholder="メッセージを入力してください..."
          hide-details
          @keydown.enter.prevent="handleSendMessage"
          :loading="isLoading"
          variant="outlined"
          density="compact"
        ></v-text-field>
        <v-btn 
          color="primary" 
          :disabled="isLoading" 
          @click="handleSendMessage"
          :loading="isLoading"
        >
          {{ isLoading ? '送信中...' : '送信' }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>
