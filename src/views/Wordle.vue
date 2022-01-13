<template>
  <div class="page">
    <header>
      <h1 class="title">{{ gameName }}</h1>
    </header>

    <WordleBoard
      :width="wordLength"
      :height="gameLength"
      :pastGuesses="pastGuesses"
      :currentGuess="currentGuessTiles"
    />
    <WordleValidLetters :letterStates="letterStates" />
    <InputSection
      @textEntered="checkGuess"
      @textInput="displayNewInput"
      :clearOnEnter="true"
    />
    <Navigation />
  </div>
</template>

<script>
import InputSection from "../components/InputSection.vue";
import WordleBoard from "../components/WordleBoard.vue";
import WordleValidLetters from "../components/WordleValidLetters.vue";
import Navigation from "../components/Navigation.vue";

export default {
  name: "Wordle",
  props: [],
  components: {
    InputSection,
    WordleBoard,
    WordleValidLetters,
    Navigation,
  },
  data() {
    return {
      lex: window.lexicon,
      gameName: "",
      wordLength: 0,
      secretWord: "",
      pastGuesses: [],
      currentGuess: "",
      letterStates: {
        A: "NONE",
        B: "NONE",
        C: "NONE",
        D: "NONE",
        E: "NONE",
        F: "NONE",
        G: "NONE",
        H: "NONE",
        I: "NONE",
        J: "NONE",
        K: "NONE",
        L: "NONE",
        M: "NONE",
        N: "NONE",
        O: "NONE",
        P: "NONE",
        Q: "NONE",
        R: "NONE",
        S: "NONE",
        T: "NONE",
        U: "NONE",
        V: "NONE",
        W: "NONE",
        X: "NONE",
        Y: "NONE",
        Z: "NONE",
      },
    };
  },
  mounted: function () {
    this.gameName = "W" + this.$route.params.pathMatch + "rdle";
    this.wordLength = this.$route.params.pathMatch.length + 5;
    this.reset();
  },
  computed: {
    gameLength: function () {
      return this.wordLength;
    },
    validWords: function () {
      return this.lex.filter((word) => word.length == this.wordLength);
    },
    currentGuessTiles: function () {
      const guessTiles = [];

      for (let iC = 0; iC < this.currentGuess.length; iC++) {
        guessTiles.push({
          letter: this.currentGuess[iC],
          hash: iC + "#" + this.currentGuess[iC],
        });
      }
      return guessTiles;
    },
  },
  methods: {
    reset() {
      this.pastGuesses = [];
      this.currentGuess = "".padEnd(this.wordLength, " ");
      this.secretWord =
        this.validWords[Math.floor(Math.random() * this.validWords.length)];
      console.log(this.secretWord);
      [..."ABCDEFGHIJKLMNOPQRSTUVWXYZ"].forEach((l) => {
        this.letterStates[l] = "NONE";
      });
    },
    displayNewInput(inputText) {
      this.currentGuess = inputText
        .toUpperCase()
        .slice(0, this.wordLength)
        .padEnd(this.wordLength, " ");
    },
    checkGuess(inputText) {
      this.currentGuess = "";
      this.displayNewInput("");
      const guess = inputText.toUpperCase().slice(0, this.wordLength);
      const valid = guess.length == this.wordLength && this.lex.includes(guess);
      if (valid) {
        const guessResult = {
          hash: this.pastGuesses.length + "#" + guess,
          tiles: [],
        };
        for (let iC = 0; iC < guess.length; iC++) {
          if (guess[iC] == this.secretWord[iC]) {
            guessResult.tiles.push({ letter: guess[iC], state: "CORRECT" });
            // this.letterStates[guess[iC]] = "CORRECT";
            // Have to set object fields with a special function so that vue will notice
            this.$set(this.letterStates, guess[iC], "CORRECT");
          } else if (this.secretWord.includes(guess[iC])) {
            guessResult.tiles.push({ letter: guess[iC], state: "MISPLACED" });
            if (this.letterStates[guess[iC]] != "CORRECT") {
              // this.letterStates[guess[iC]] = "MISPLACED";
              this.$set(this.letterStates, guess[iC], "MISPLACED");
            }
          } else {
            guessResult.tiles.push({ letter: guess[iC], state: "WRONG" });
            // this.letterStates[guess[iC]] = "WRONG";
            this.$set(this.letterStates, guess[iC], "WRONG");
          }
          guessResult.tiles[guessResult.tiles.length - 1].hash =
            this.pastGuesses.length +
            "#" +
            guessResult.tiles[guessResult.tiles.length - 1].letter +
            "#" +
            iC +
            "#" +
            guessResult.tiles[guessResult.tiles.length - 1].state;
        }

        this.pastGuesses.push(guessResult);
      }
    },
  },
};
</script>

<style>
@media screen and (max-width: 500px) {
  .title {
    display: none;
  }
}
</style>
