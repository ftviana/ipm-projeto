<template>
  <div class="toast-notification">
    <div class="icon-circle">
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24">
        <path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="m5 13l4 4L19 7"/>
      </svg>
    </div>
    <span>Changes saved successfully.</span>
  </div>
</template>

<style scoped>

.toast-notification {
  position: absolute;
  background-color: #E0F2E9;
  color: #065F46;
  padding: 1rem 1.5rem;
  border-radius: 9999px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 500;
}

.icon-circle {
  background-color: #34D399;
  color: #ffffff;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-circle svg {
  width: 18px;
  height: 18px;
}

</style>