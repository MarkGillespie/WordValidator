<template>
  <div>
    <header>
      <h1 class="title">Anagrammer</h1>
    </header>
    <InputSection @textInput="checkInputWord" />
    <div class="horizontal-layout">
      <CompletionSection
        :completions="completions"
        :id="'standardCompletions'"
        :title="usingCustomLexicon ? 'Standard Words' : ''"
        :width="usingCustomLexicon ? 'half' : 'full'"
      />
      <CompletionSection
        v-if="usingCustomLexicon"
        :completions="customLexiconCompletions"
        :id="'customCompletions'"
        :title="'Custom Words'"
        :width="'half'"
      />
    </div>
    <LexiconInput @customLexiconInput="useCustomLexicon" />
    <Navigation />
  </div>
</template>

<script>
import InputSection from "../components/InputSection.vue";
import CompletionSection from "../components/CompletionSection.vue";
import LexiconInput from "../components/LexiconInput.vue";
import Navigation from "../components/Navigation.vue";

export default {
  name: "Anagrammer",
  props: [],
  components: {
    InputSection,
    CompletionSection,
    Navigation,
    LexiconInput,
  },
  data() {
    return {
      lex: window.lexicon,
      completions: [],
      word: "",
      upperCaseWord: "",
      customLexicon: null,
      customLexiconCompletions: [],
    };
  },
  mounted: function () {
    if (this.$route.params.queryWord) {
      this.word = this.$route.params.queryWord;
      this.checkWord();
    }
  },
  computed: {
    usingCustomLexicon: function () {
      return this.customLexicon && this.customLexicon.length > 0;
    },
  },
  methods: {
    useCustomLexicon(customLexicon) {
      this.customLexicon = customLexicon;
      this.checkWord();
      console.log(this.customLexicon);
    },
    checkInputWord(word) {
      this.word = word;
      this.checkWord();
    },
    checkWord() {
      this.upperCaseWord = this.word.toUpperCase();
      this.completions = [];
      this.customLexiconCompletions = [];

      let checkPlainText = /^([A-Z]|\.)*$/;
      if (checkPlainText.test(this.upperCaseWord)) {
        const wordLen = this.upperCaseWord.length;
        const sortedChars = this.upperCaseWord.split("").sort();
        let queryRegexp;
        if (sortedChars[0] === ".") {
          while (sortedChars[0] === ".") {
            sortedChars.shift();
          }
          const sortedWord = sortedChars.join(".*");
          queryRegexp = new RegExp("^.*" + sortedWord + ".*$");
        } else {
          const sortedWord = sortedChars.join("");
          queryRegexp = new RegExp("^" + sortedWord + "$");
        }

        this.lex.forEach((word) => {
          if (
            word.length === wordLen &&
            queryRegexp.test(word.split("").sort().join(""))
          ) {
            this.completions.push(word);
          }
        });
        if (this.usingCustomLexicon) {
          this.customLexicon.forEach((word) => {
            if (
              word.length === wordLen &&
              queryRegexp.test(word.split("").sort().join(""))
            ) {
              this.customLexiconCompletions.push(word);
            }
          });
        }
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
