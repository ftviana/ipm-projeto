<template>
  <div class="map-wrapper">
    <l-map
      ref="mapRef"
      v-model:zoom="zoom"
      :center="initialCenter"
      :use-global-leaflet="false"
      :options="{ scrollWheelZoom: false }"
      @ready="onMapReady"
    >
      <l-tile-layer
        url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
        layer-type="base"
        name="CartoDB Voyager"
      ></l-tile-layer>

      <l-circle
        v-for="point in points"
        :key="point.id"
        :lat-lng="[point.lat, point.lng]"
        :radius="120"
        :color="point.color"
        :fill="true"
        :fillColor="point.color"
        :fillOpacity="0.5"
        :stroke="false"
      />
    </l-map>
  </div>
</template>

<script setup>
import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer, LCircle } from "@vue-leaflet/vue-leaflet";
import { ref, computed, watch, nextTick } from "vue";

const props = defineProps({
  listings: { type: Array, default: () => [] },
  center: { type: Array, default: () => [41.1579, -8.6291] },
  mode: { type: String, default: "Price" },
});

const zoom = ref(13);
const mapRef = ref(null);
const initialCenter = ref(props.center);
let leafletObject = null;

const onMapReady = () => {
  leafletObject = mapRef.value?.leafletObject;
};

const parseCoord = (val) => {
  if (typeof val === "number") return val;
  if (typeof val === "string") return parseFloat(val.replace(",", "."));
  return 0;
};

watch(
  () => props.listings,
  async (newListings) => {
    await nextTick();
    if (newListings && newListings.length > 0 && leafletObject) {
      const firstHouse = newListings[0];
      const lat = parseCoord(firstHouse.latitude);
      const lng = parseCoord(firstHouse.longitude);
      if (!isNaN(lat) && !isNaN(lng) && lat !== 0) {
        leafletObject.setView([lat, lng], 13);
      }
    }
  },
  { deep: true }
);

const points = computed(() => {
  if (!props.listings) return [];

  return props.listings
    .slice(0, 2000)
    .map((l) => {
      const lat = parseCoord(l.latitude);
      const lng = parseCoord(l.longitude);

      if (isNaN(lat) || isNaN(lng) || (lat === 0 && lng === 0)) return null;

      let color = "#00A699";

      if (props.mode === "Price") {
        const price = parseFloat(String(l.price).replace(/[$,]/g, ""));
        if (price < 90) {
          color = "#00A699";
        } else if (price >= 90 && price < 160) {
          color = "#FFB400";
        } else {
          color = "#FF5A5F";
        }
      } else {
        const avail = parseInt(l.availability_365) || 0;
        if (avail > 180) {
          color = "#00A699";
        } else if (avail >= 60 && avail <= 180) {
          color = "#FFB400";
        } else {
          color = "#FF5A5F";
        }
      }

      return { id: l.id, lat, lng, color };
    })
    .filter((p) => p !== null);
});
</script>

<style scoped>
.map-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 0;
  width: 100%;
  height: 100%;
  min-height: 100%;
  overflow: hidden;
  background-color: #f0f0f0;
  border-radius: 12px;
}
</style>
