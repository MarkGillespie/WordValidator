<template>
  <div class="wordle-alphabet">
    <div v-for="letter in letterStateList" :key="letter.letter">
      <span v-bind:class="'wordle-letter-data ' + letter.state">
        {{ letter.letter }}</span
      >
    </div>
  </div>
</template>

<script>
export default {
  name: "WordleValidLetters",
  components: {},
  props: ["letterStates"],
  data() {
    return {
      letterStateList: [],
    };
  },
  computed: {},
  mounted: function () {
    this.updateLetterStateList();
  },
  methods: {
    updateLetterStateList() {
      const alphabet = [..."ABCDEFGHIJKLMNOPQRSTUVWXYZ"];
      this.letterStateList = [];
      alphabet.forEach((l) => {
        this.letterStateList.push({
          letter: l,
          state: this.letterStates[l],
          hash: "letter#" + l + "#" + this.letterStates[l],
        });
      });
    },
  },
  watch: {
    letterStates: {
      handler: "updateLetterStateList",
      deep: true,
      initial: true,
    },
  },
};
</script>

<style>
.wordle-alphabet {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 1em;
  margin: 1em 0em;
}

.wordle-letter-data {
  background-color: #888;
  color: white;
  text-shadow: 0px 0px 4px black;

  font-size: 24pt;
  width: 1.5em;
  height: 1.5em;
  border-radius: 0.15em;

  /* center text */
  display: flex;
  align-items: center;
  justify-content: center;
}

.wordle-letter-data.CORRECT {
  background-color: green;
  color: white;
}

.wordle-letter-data.MISPLACED {
  background-color: rgb(200, 175, 50);
  color: white;
}

.wordle-letter-data.WRONG {
  background-color: rgb(200, 50, 50);
  color: white;
}
</style>
