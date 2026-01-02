<template>
  <div class="toast-notification">
    <div class="icon-circle">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="16"
        height="16"
        viewBox="0 0 24 24"
      >
        <path
          fill="none"
          stroke="currentColor"
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="3"
          d="m5 13l4 4L19 7"
        />
      </svg>
    </div>
    <span>Changes saved successfully.</span>
  </div>
</template>

<style scoped>
.toast-notification {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  height: 52px;
  padding: 0 1.5rem;
  font-size: 0.9rem;
  font-weight: 600;
  color: darkgreen;
  background-color: #e0f2e9;
  border-radius: 40px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.icon-circle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  color: white;
  background-color: green;
  border-radius: 50%;
}
</style>
