<template>
  <div class="loading-wrap">
    <div class="balls">
      <div></div>
      <div></div>
      <div></div>
    </div>
  </div>
</template>

<script setup lang="ts">

</script>

<style scoped>
.loading-wrap {
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  bottom: 8px;
  left: 7px;
}

.balls {
  width: 4em;
  display: flex;
  flex-flow: row nowrap;
  align-items: center;
  justify-content: space-between;
}

.balls div {
  width: 0.8em;
  height: 0.8em;
  border-radius: 50%;
  background-color: #4b9e5f;
}

.balls div:nth-of-type(1) {
  transform: translateX(-100%);
  animation: left-swing 0.5s ease-in alternate infinite;
}

.balls div:nth-of-type(3) {
  transform: translateX(-95%);
  animation: right-swing 0.5s ease-out alternate infinite;
}

@keyframes left-swing {
  
  50%,
  100% {
    transform: translateX(95%);
  }
}

@keyframes right-swing {
  50% {
    transform: translateX(-95%);
  }
  
  100% {
    transform: translateX(100%);
  }
}

@media (prefers-color-scheme: dark) {
  body {
    background: #121212;
  }
}
</style>
