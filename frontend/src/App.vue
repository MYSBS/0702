<template>
  <div id="app-container" class="flex flex-col h-screen w-full sm:max-w-screen-xl sm:mx-auto p-4 sm:p-5 bg-kakao-bg">
    <header class="flex justify-between items-center p-3 sm:p-4 md:p-6 bg-kakao-header text-white shadow-md">
      <div class="text-xl sm:text-2xl md:text-3xl cursor-pointer hover:text-gray-300 transition-colors">&#9776;</div>
      <h1 class="text-base sm:text-lg md:text-2xl font-bold">PREVIEW.</h1>
      <div class="text-xl sm:text-2xl md:text-3xl cursor-pointer hover:text-gray-300 transition-colors">&#128269;</div>
    </header>
    <main class="flex-grow p-3 sm:p-4 md:p-6 overflow-y-auto">
      <ChatWindow :car-model="selectedCar" />
    </main>
    <div class="p-3 sm:p-4 md:p-6 bg-kakao-header shadow-inner">
        <select v-model="selectedCar" class="w-full p-2 sm:p-2 md:p-3 text-sm sm:text-base md:text-lg rounded-lg border-none focus:ring-2 focus:ring-kakao-yellow bg-white text-gray-800 shadow-sm">
          <option disabled value="">차종을 선택하세요</option>
          <option>Tesla Model 3</option>
          <option>Hyundai IONIQ 5</option>
          <option>Kia EV6</option>
        </select>
    </div>
  </div>
</template>

<script>
import ChatWindow from './components/ChatWindow.vue';

export default {
  name: 'App',
  components: {
    ChatWindow,
  },
  data() {
    return {
      selectedCar: '',
    };
  },
};
</script>

<style>
/* Tailwind CSS will handle most styling, but you can keep global styles here if needed */
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}
</style>