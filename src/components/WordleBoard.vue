<template>
  <div class="wordle-board">
    <div class="wordle-guess" v-for="guess in pastGuesses" :key="guess.hash">
      <div
        v-for="guessTile in guess.tiles"
        v-bind:class="'wordle-tile ' + guessTile.state"
        :key="guessTile.hash"
      >
        {{ guessTile.letter }}
      </div>
    </div>
    <div class="wordle-guess current-guess">
      <div v-for="tile in currentGuess" class="wordle-tile" :key="tile.hash">
        {{ tile.letter }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "WordleBoard",
  components: {},
  props: ["width", "height", "pastGuesses", "currentGuess"],
  data() {
    return {};
  },
  computed: {},
  watch: {},
};
</script>

<style>
.wordle-board {
  display: flex;
  flex-direction: column;
  gap: 1em;
}

.wordle-guess {
  display: flex;
  flex-direction: row;
  gap: 1em;
  justify-content: center;
}

.wordle-tile {
  background-color: #888;
  color: white;
  text-shadow: 0px 0px 4px black;

  font-size: 48pt;
  width: 1.5em;
  height: 1.5em;
  border-radius: 0.15em;

  /* center text */
  display: flex;
  align-items: center;
  justify-content: center;
}

.wordle-tile.CORRECT {
  background-color: green;
  color: white;
}

.wordle-tile.MISPLACED {
  background-color: rgb(200, 175, 50);
  color: white;
}

.wordle-tile.WRONG {
  background-color: rgb(200, 50, 50);
  color: white;
}
</style>
