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
    <button v-on:click="generateWord()">New Board</button>
    <button v-on:click="revealAnswer()">Reveal Answer</button>
    <button v-on:click="showDefinition()">What is this word?</button>
    <button v-if="useSimpleWords" v-on:click="setUseSimpleWords(false)">
      Allow weird words
    </button>
    <button v-else v-on:click="setUseSimpleWords(true)">
      Use simple words
    </button>
    <Navigation />
  </div>
</template>

<script>
import InputSection from "../components/InputSection.vue";
import WordleBoard from "../components/WordleBoard.vue";
import WordleValidLetters from "../components/WordleValidLetters.vue";
import Navigation from "../components/Navigation.vue";
import { simple_lexicon } from "../../public/resources/simple_lexicon.js";

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
      full_lex: window.lexicon,
      useSimpleWords: true,
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
    this.init();
  },
  watch: {
    $route: function () {
      this.init();
    },
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
    lex: function () {
      return this.useSimpleWords ? simple_lexicon : this.full_lex;
    },
  },
  methods: {
    init() {
      this.gameName = "W" + this.$route.params.pathMatch + "rdle";
      this.wordLength = this.$route.params.pathMatch.length + 5;
      this.currentGuess = "";
      if (this.$route.params.secretWord) {
        // TODO: what do you do if this.wordLength doesn't match secretWord's length?
        this.reset();
        this.secretWord = this.decode(this.$route.params.secretWord);
        console.log(this.secretWord);
      } else {
        this.reset();
        this.generateWord();
      }
    },
    generateWord() {
      this.secretWord =
        this.validWords[Math.floor(Math.random() * this.validWords.length)];
      while (!this.full_lex.includes(this.secretWord)) {
        this.secretWord =
          this.validWords[Math.floor(Math.random() * this.validWords.length)];
      }
      console.log(this.secretWord);
      this.$router.push(
        "/Games/" + this.gameName + "/" + this.encode(this.secretWord)
      );
    },
    reset() {
      this.pastGuesses = [];
      this.currentGuess = "".padEnd(this.wordLength, " ");
      [..."ABCDEFGHIJKLMNOPQRSTUVWXYZ"].forEach((l) => {
        this.letterStates[l] = "NONE";
      });
    },
    revealAnswer() {
      this.checkGuess(this.secretWord);
    },
    showDefinition() {
      this.$router.push("/" + this.secretWord);
    },
    setUseSimpleWords(arg) {
      this.useSimpleWords = arg;
      this.generateWord();
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
      const valid =
        guess.length == this.wordLength && this.full_lex.includes(guess);

      // eslint-disable-next-line no-constant-condition
      if (valid) {
        const guessResult = {
          hash: this.pastGuesses.length + "#" + guess,
          tiles: [],
        };
        // identify correct letters, mark all others as wrong for now
        const matchedLetter = new Array(guess.length).fill(false);
        for (let iC = 0; iC < guess.length; iC++) {
          if (guess[iC] == this.secretWord[iC]) {
            guessResult.tiles.push({ letter: guess[iC], state: "CORRECT" });
            matchedLetter[iC] = true;
            // Have to set object fields with a special function so that vue will notice
            // this.letterStates[guess[iC]] = "CORRECT";
            this.$set(this.letterStates, guess[iC], "CORRECT");
          } else {
            guessResult.tiles.push({ letter: guess[iC], state: "WRONG" });
            // this.letterStates[guess[iC]] = "WRONG";
            if (this.letterStates[guess[iC]] == "NONE") {
              this.$set(this.letterStates, guess[iC], "WRONG");
            }
          }
        }
        // identify misplaced letters
        for (let iC = 0; iC < guess.length; iC++) {
          if (guessResult.tiles[iC].state != "CORRECT") {
            for (let jC = 0; jC < guess.length; jC++) {
              if (!matchedLetter[jC] && guess[iC] == this.secretWord[jC]) {
                guessResult.tiles[iC].state = "MISPLACED";
                matchedLetter[jC] = true;
                if (this.letterStates[guess[iC]] == "NONE") {
                  this.letterStates[guess[iC]] = "MISPLACED";
                  this.$set(this.letterStates, guess[iC], "MISPLACED");
                }
                break;
              }
            }
          }

          // Set tile hash
          guessResult.tiles[guessResult.tiles.length - 1].hash =
            this.pastGuesses.length +
            "#" +
            guessResult.tiles[guessResult.tiles.length - 1].letter +
            "#" +
            iC +
            "#" +
            guessResult.tiles[guessResult.tiles.length - 1].state;
        }
        console.log(this.letterStates);

        this.pastGuesses.push(guessResult);
      }
    },
    chrAt(text, pos) {
      return text.charCodeAt(pos) - 65;
    },
    encode(text) {
      const key = "WRDLE";
      let result = "";
      for (let i = 0; i < text.length; i++) {
        result += String.fromCharCode(
          65 + ((this.chrAt(text, i) + this.chrAt(key, i % key.length)) % 26)
        );
      }
      return result;
    },
    decode(text) {
      const key = "WRDLE";
      let result = "";
      for (let i = 0; i < text.length; i++) {
        result += String.fromCharCode(
          65 +
            ((this.chrAt(text, i) + (26 - this.chrAt(key, i % key.length))) %
              26)
        );
      }
      return result;
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
