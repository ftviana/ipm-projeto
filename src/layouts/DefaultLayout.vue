<script setup>
import { RouterLink } from 'vue-router'
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const navCenter = ref(null)
const glider = ref(null)
const route = useRoute()
const isGliderVisible = ref(false)

const updateGlider = () => {
  if (!navCenter.value || !glider.value) return

  const activeLink = navCenter.value.querySelector('a.router-link-exact-active')

  if (activeLink) {
    
    if (isGliderVisible.value) {
      glider.value.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
    } else {
      glider.value.style.transition = 'none';
    }

    glider.value.style.opacity = '1';
    isGliderVisible.value = true; 

    const space = 4 
    const navStyle = getComputedStyle(navCenter.value)
    const paddingTop = parseFloat(navStyle.paddingTop) || 0
    
    const offsetLeft = activeLink.offsetLeft
    const offsetWidth = activeLink.offsetWidth
    const offsetHeight = activeLink.offsetHeight

    glider.value.style.width = `${offsetWidth - (space * 2)}px`
    glider.value.style.height = `${offsetHeight - (space * 2)}px`
    glider.value.style.top = `${paddingTop + space}px`
    glider.value.style.transform = `translateX(${offsetLeft + space}px)`

  } else {
    glider.value.style.transition = 'none'; 
    glider.value.style.width = '0px';
    glider.value.style.opacity = '0';
    isGliderVisible.value = false;
  }
}

watch(
  () => route.path,
  () => {
    setTimeout(updateGlider, 0)
  },
  { flush: 'post', immediate: true }
)
</script>

<template>
  <div class="app-layout">
    <header>
      <nav>
        <div class="nav-left">
          <RouterLink to="/" class="logo">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 14 14"><g fill="none"><path fill="black" d="M6.489.872L1.793 9.99a.5.5 0 0 0 .444.729l10.049.003l-5.07-9.85c-.173-.336-.554-.336-.727 0"/><path stroke="black" stroke-linecap="round" stroke-linejoin="round" d="M6.489.872L1.793 9.99a.5.5 0 0 0 .444.729l10.049.003l-5.07-9.85c-.173-.336-.554-.336-.727 0" stroke-width="1"/><path fill="linen" d="M6.852 13.38c3.041 0 5.507-1.01 5.507-2.256S9.893 8.868 6.852 8.868s-5.508 1.01-5.508 2.256S3.81 13.38 6.852 13.38"/><path stroke="black" stroke-linecap="round" stroke-linejoin="round" d="M6.852 13.38c3.041 0 5.507-1.01 5.507-2.256S9.893 8.868 6.852 8.868s-5.508 1.01-5.508 2.256S3.81 13.38 6.852 13.38" stroke-width="1"/></g></svg>
            <span>InsideView</span>
          </RouterLink>
        </div>
        
        <div class="nav-center" ref="navCenter">
          <span class="glider" ref="glider"></span>

          <RouterLink to="/">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24"><path fill="currentColor" d="M6 19h3v-5q0-.425.288-.712T10 13h4q.425 0 .713.288T15 14v5h3v-9l-6-4.5L6 10zm-2 0v-9q0-.475.213-.9t.587-.7l6-4.5q.525-.4 1.2-.4t1.2.4l6 4.5q.375.275.588.7T20 10v9q0 .825-.588 1.413T18 21h-4q-.425 0-.712-.288T13 20v-5h-2v5q0 .425-.288.713T10 21H6q-.825 0-1.412-.587T4 19m8-6.75"/></svg>
            <span>Home</span>
          </RouterLink>

          <RouterLink to="/exploredata">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"><path fill="currentColor" d="m7.5 16.5l7-2l2-7l-7 2zm4.5-3q-.625 0-1.412-.587T10.5 12t.438-1.062T12 10.5t1.063.438T13.5 12t-.437 1.063T12 13.5m0 8.5q-2.075 0-3.9-.788t-3.175-2.137T2.788 15.9T2 12t.788-3.9t2.137-3.175T8.1 2.788T12 2t3.9.788t3.175 2.137T21.213 8.1T22 12t-.788 3.9t-2.137 3.175t-3.175 2.138T12 22m0-2q3.325 0 5.663-2.337T20 12t-2.337-5.663T12 4T6.337 6.338T4 12t2.338 5.663T12 20m0-8"/></svg>
            <span>Explore Data</span>
          </RouterLink>

          <RouterLink to="/compare">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24"><path fill="currentColor" d="m8 20l-1.4-1.425L9.175 16H2v-2h7.175L6.6 11.425L8 10l5 5zm8-6l-5-5l5-5l1.4 1.425L14.825 8H22v2h-7.175l2.575 2.575z"/></svg>
            <span>Compare</span>
          </RouterLink>

          <RouterLink to="/anomalies">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24">
            <g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2">
            <path d="M12 3v2"/>
            <path d="M12 5c-3.31 0 -6 2.69 -6 6l0 6c-1 0 -2 1 -2 2h8M12 5c3.31 0 6 2.69 6 6l0 6c1 0 2 1 2 2h-8"/>
            <path d="M10 20c0 1.1 0.9 2 2 2c1.1 0 2 -0.9 2 -2"/>
            </g>
            </svg>
          <span>Anomalies</span>
          </RouterLink>

          <RouterLink to="/export">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24"><path fill="currentColor" d="m12 16l-5-5l1.4-1.45l2.6 2.6V4h2v8.15l2.6-2.6L17 11zm-6 4q-.825 0-1.412-.587T4 18v-3h2v3h12v-3h2v3q0 .825-.587 1.413T18 20z"/></svg>
            <span>Export</span>
          </RouterLink>

          <RouterLink to="/faq">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24"><g fill="none"><path d="m12.593 23.258l-.011.002l-.071.035l-.02.004l-.014-.004l-.071-.035q-.016-.005-.024.005l-.004.01l-.017.428l.005.02l.01.013l.104.074l.015.004l.012-.004l.104-.074l.012-.016l.004-.017l-.017-.427q-.004-.016-.017-.018m.265-.113l-.013.002l-.185.093l-.01.01l-.003.011l.018.43l.005.012l.008.007l.201.093q.019.005.029-.008l.004-.014l-.034-.614q-.005-.018-.02-.022m-.715.002a.02.02 0 0 0-.027.006l-.006.014l-.034.614q.001.018.017.024l.015-.002l.201-.093l.01-.008l.004-.011l.017-.43l-.003-.012l-.01-.01z"/><path fill="currentColor" d="M12 2c5.523 0 10 4.477 10 10s-4.477 10-10 10S2 17.523 2 12S6.477 2 12 2m0 2a8 8 0 1 0 0 16a8 8 0 0 0 0-16m0 12a1 1 0 1 1 0 2a1 1 0 0 1 0-2m0-9.5a3.625 3.625 0 0 1 1.348 6.99a.8.8 0 0 0-.305.201c-.044.05-.051.114-.05.18L13 14a1 1 0 0 1-1.993.117L11 14v-.25c0-1.153.93-1.845 1.604-2.116a1.626 1.626 0 1 0-2.229-1.509a1 1 0 1 1-2 0A3.625 3.625 0 0 1 12 6.5"/></g></svg>
            <span>FAQ</span>
          </RouterLink>

        </div>
        
        <div class="nav-right">
          <RouterLink to="/settings" class="settings-button">
            <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" viewBox="0 0 16 16"><path fill="black" fill-rule="evenodd" d="M8 5C6.34 5 5 6.34 5 8s1.34 3 3 3s3-1.34 3-3s-1.34-3-3-3M6 8a2 2 0 1 1 4.001-.001A2 2 0 0 1 6 8" clip-rule="evenodd"/><path fill="black" fill-rule="evenodd" d="M8 0C6.9 0 6 .895 6 2v.068a.46.46 0 0 1-.285.423a.45.45 0 0 1-.492-.096a1.924 1.924 0 0 0-2.72 0l-.109.11a1.924 1.924 0 0 0 0 2.72a.45.45 0 0 1 .096.491a.46.46 0 0 1-.424.285h-.068a2 2 0 1 0 0 4h.068c.183 0 .352.112.424.285a.45.45 0 0 1-.096.492a1.924 1.924 0 0 0 0 2.72l.109.11c.751.75 1.97.75 2.72 0a.45.45 0 0 1 .492-.097c.172.072.285.24.285.424v.068a2 2 0 1 0 4 0v-.068c0-.183.112-.352.285-.424a.45.45 0 0 1 .492.096c.751.751 1.97.751 2.72 0l.109-.109a1.924 1.924 0 0 0 0-2.72a.45.45 0 0 1-.096-.492a.46.46 0 0 1 .424-.285H14a2 2 0 1 0 0-4h-.067a.46.46 0 0 1-.424-.285a.45.45 0 0 1 .096-.492a1.924 1.924 0 0 0 0-2.72l-.109-.109a1.924 1.924 0 0 0-2.72 0a.45.45 0 0 1-.492.096a.46.46 0 0 1-.285-.424V2c0-1.1-.895-2-2-2M7 2a1 1 0 0 1 2 0v.068c0 .59.359 1.12.902 1.35c.54.223 1.17.102 1.58-.314a.917.917 0 0 1 1.3 0l.109.11a.93.93 0 0 1 0 1.31a1.45 1.45 0 0 0-.313 1.58c.225.543.756.902 1.35.902h.067a1 1 0 0 1 0 2h-.067a1.47 1.47 0 0 0-1.35.902c-.224.54-.103 1.17.313 1.58c.36.36.36.945 0 1.3l-.109.109a.917.917 0 0 1-1.3 0a1.45 1.45 0 0 0-1.58-.313A1.46 1.46 0 0 0 9 13.934V14a1 1 0 0 1-2 0v-.067a1.47 1.47 0 0 0-.902-1.35a1.45 1.45 0 0 0-1.58.313a.917.917 0 0 1-1.3 0l-.109-.11a.93.93 0 0 1 0-1.31a1.45 1.45 0 0 0 .313-1.58a1.46 1.46 0 0 0-1.35-.901h-.068a1 1 0 0 1 0-2h.068a1.47 1.47 0 0 0 1.35-.902c.224-.54.103-1.17-.313-1.58a.917.917 0 0 1 0-1.3l.109-.11a.93.93 0 0 1 1.31 0a1.45 1.45 0 0 0 1.58.314c.543-.225.902-.756.902-1.35V2z" clip-rule="evenodd"/></svg>
          </RouterLink>
        </div>
      </nav>
    </header>

    <main>
      <RouterView />
    </main>

  </div>
</template>

<style scoped>

.app-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

header, footer {
  background-color: linen;
  padding: 1rem;
  border-bottom: 1px solid linen;
}

main {
  flex: 1;
  display: flex;
  justify-content: center;
}

footer {
  border-top: 1px solid linen;
}

nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
}

.nav-left .logo {
  display: flex;
  align-items: center;
  font-weight: bold;
  font-size: 1.2rem;
  text-decoration: none;
  color: black;
  gap: 0.5rem
}

.logo svg {
  width: 1.5rem;
  height: 1.5rem;
  rotate: 180deg;
}

.nav-center {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  background-color: white;
  border-radius: 40px;
  overflow: hidden;
}

.glider {
  position: absolute;
  /* COR ALTERADA */
  background-color: #FF5A5F;
  border-radius: 40px; 
  z-index: 1;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.nav-center a {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;

  white-space: nowrap;

  position: relative;
  z-index: 2;
  padding: 0.9rem 1.5rem; 
  text-decoration: none;
  color: dimgrey;
  transition: color 0.3s ease;
}

.nav-center a svg {
  fill: currentColor;
  width: 20px;
  height: 20px;
}

.nav-center a.router-link-exact-active {
  color: white;
}

.nav-center a:not(.router-link-exact-active):hover {
  color: black;
}

.nav-right .settings-button {
  display: flex;
  align-items: center;
  justify-content: center;

  padding: 0.5rem;
  border-radius: 50%;

  border: none;
  background-color: lightgrey;
  cursor: pointer;
}
</style>