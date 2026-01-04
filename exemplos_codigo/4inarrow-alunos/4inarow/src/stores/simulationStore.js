import { defineStore } from "pinia";

export const useSimulationStore = defineStore('simulation', {
  state: () => {
    return {
      // TODO: declarar startPlayer
      // TODO: declarar plays
    };
  },
  actions: {
    // TODO: implementar setStartPlayer(player)
    // TODO: implementar addPlay(play)
  },
  getters: {
    // TODO: containsSimulation -> true se startPlayer != null e plays não vazio
  }
});