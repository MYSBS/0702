<template>
  <div class="flex flex-col h-full bg-kakao-bg rounded-lg shadow-lg">
    <div class="flex-grow overflow-y-auto p-3 sm:p-4 space-y-4" ref="messagesContainer">
      <div v-for="(msg, index) in messages" :key="index" :class="[
        'p-3 sm:p-4 rounded-xl shadow-md max-w-[90%] sm:max-w-[80%] break-words',
        msg.sender === 'user' ? 'ml-auto bg-kakao-yellow text-gray-800' : 'mr-auto bg-kakao-grey text-gray-800',
      ]">
        <div class="flex justify-between text-xs mb-1"
             :class="msg.sender === 'user' ? 'text-gray-600' : 'text-gray-500'">
          <span v-if="msg.sender === 'user'">You</span>
          <span v-else>{{ carModel || 'Bot' }}</span>
          <span>{{ new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }}</span>
        </div>
        <div class="text-sm sm:text-base">
          {{ msg.text }}
        </div>
      </div>
      <div v-if="isLoading || typingMessage" :class="[
        'p-3 sm:p-4 rounded-xl shadow-md max-w-[90%] sm:max-w-[80%] break-words mr-auto bg-kakao-grey text-gray-800',
        'italic text-gray-500',
      ]">
        <div class="text-sm sm:text-base">
          <span v-if="isLoading && !typingMessage">... 생각 중 ...</span>
          <span v-else-if="typingMessage">{{ typingMessage }}<span class="typing-cursor">|</span></span>
        </div>
      </div>
    </div>
    <form @submit.prevent="sendMessage" class="flex p-3 sm:p-4 bg-white border-t border-gray-200 rounded-b-lg">
      <input
        v-model="newMessage"
        placeholder="메시지를 입력하세요..."
        :disabled="!carModel || isLoading"
        class="flex-grow p-2 sm:p-3 border border-gray-300 rounded-full mr-2 focus:outline-none focus:ring-2 focus:ring-kakao-yellow bg-white text-gray-800 shadow-sm text-sm sm:text-base"
      />
      <button
        type="submit"
        :disabled="!newMessage || !carModel || isLoading"
        class="px-4 py-2 sm:px-6 sm:py-3 bg-kakao-yellow text-gray-800 rounded-full font-semibold hover:bg-yellow-400 disabled:bg-gray-400 transition-colors text-sm sm:text-base"
      >
        전송
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue';
import { sendMessage as sendChatMessage } from '../api/chat';

const props = defineProps({
  carModel: {
    type: String,
    required: true,
  },
});

const messages = ref([]);
const newMessage = ref('');
const messagesContainer = ref(null);
const isLoading = ref(false);
const typingMessage = ref('');

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    }
  });
};

const typeMessage = (fullMessage) => {
  let i = 0;
  typingMessage.value = '';
  const typingInterval = setInterval(() => {
    if (i < fullMessage.length) {
      typingMessage.value += fullMessage.charAt(i);
      i++;
      scrollToBottom();
    } else {
      clearInterval(typingInterval);
      messages.value.push({ sender: 'bot', text: fullMessage });
      typingMessage.value = '';
      isLoading.value = false;
      scrollToBottom();
    }
  }, 50);
};

const sendMessage = async () => {
  if (newMessage.value.trim() === '' || !props.carModel || isLoading.value) return;

  messages.value.push({ sender: 'user', text: newMessage.value });
  newMessage.value = '';
  scrollToBottom();

  isLoading.value = true;
  typingMessage.value = '';

  try {
    const response = await sendChatMessage(messages.value[messages.value.length - 1].text, props.carModel);
    typeMessage(response.response);
  } catch (error) {
    messages.value.push({ sender: 'bot', text: '오류가 발생했습니다.' });
    isLoading.value = false;
    scrollToBottom();
  }
};

watch(() => props.carModel, (newVal, oldVal) => {
  if (newVal !== oldVal) {
    messages.value = [];
    typingMessage.value = '';
    isLoading.value = false;
    if (newVal) {
      messages.value.push({ sender: 'bot', text: `이제 ${newVal}에 대해 질문할 수 있습니다.` });
    }
    scrollToBottom();
  }
});
</script>

<style scoped>
/* Tailwind handles most styling, but you can add custom animations or specific overrides here */
.typing-cursor {
  display: inline-block;
  animation: blink 1s step-end infinite;
}

@keyframes blink {
  from, to { opacity: 1; }
  50% { opacity: 0; }
}
</style>