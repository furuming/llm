
export const useChatApi = () => {
  /**
   * チャットメッセージを送信する
   * @param content 送信するテキスト
   * @returns バックエンドからのレスポンス（テキスト）
   */
  const sendMessage = async (content: string): Promise<string> => {
    const data = await $fetch<string>('/api/chat', {
      method: 'POST',
      body: {
        content: content,
      },
    })

    return data
  }

  return {
    sendMessage,
  }
}
