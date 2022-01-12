<template>
  <div>
    <header>
      <h1 class="title">{{ gameName }}</h1>
    </header>

    <div class="wordle-board">
      <div class="wordle-guess" v-for="guess in pastGuesses" :key="guess">
        <span>{{ guess }}</span>
      </div>
    </div>
    <InputSection @textEntered="checkGuess" />
    <Navigation />
  </div>
</template>

<script>
import InputSection from "../components/InputSection.vue";
import Navigation from "../components/Navigation.vue";

export default {
  name: "Wordle",
  props: [],
  components: {
    InputSection,
    Navigation,
  },
  data() {
    return {
      lex: window.lexicon,
      gameName: "",
      wordLength: 0,
      secretWord: "",
      pastGuesses: [],
    };
  },
  mounted: function () {
    this.gameName = "W" + this.$route.params.pathMatch + "rdle";
    this.wordLength = this.$route.params.pathMatch.length + 5;
  },
  computed: {},
  methods: {
    checkGuess(inputText) {
      const guess = inputText.toUpperCase();
      const valid = guess.length == this.wordLength && this.lex.includes(guess);
      if (valid) {
        this.pastGuesses.push(guess);
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
