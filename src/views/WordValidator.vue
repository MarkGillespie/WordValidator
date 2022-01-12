<template>
  <div>
    <header>
      <h1 class="title">Word Validator</h1>
    </header>
    <DefinitionSection
      :word="upperCaseWord"
      :isWord="isWord"
      :definition="definition"
    />
    <InputSection @textInput="checkInputWord" />
    <CompletionSection :completions="completions" />
    <Navigation />
  </div>
</template>

<script>
import DefinitionSection from "../components/DefinitionSection.vue";
import InputSection from "../components/InputSection.vue";
import CompletionSection from "../components/CompletionSection.vue";
import Navigation from "../components/Navigation.vue";
import { PackedTrie } from "../../public/resources/packed-trie.js";

export default {
  name: "WordValidator",
  props: [],
  components: {
    DefinitionSection,
    InputSection,
    CompletionSection,
    Navigation,
  },
  data() {
    return {
      dictionary: window.dictionary,
      completions: [],
      word: "",
      upperCaseWord: "",
      isWord: false,
      definition: "",
      log: "",
      lex: new PackedTrie(window.packed_lexicon),
      completionsPreview: [],
    };
  },
  mounted: function () {
    if (this.$route.params.queryWord) {
      this.word = this.$route.params.queryWord;
      this.checkWord();
    }
  },
  methods: {
    checkInputWord(word) {
      this.word = word;
      this.checkWord();
    },
    checkWord() {
      this.upperCaseWord = this.word.toUpperCase();

      let checkPlainText = /^([A-Z]|\.)*$/;
      if (checkPlainText.test(this.upperCaseWord)) {
        this.completions =
          this.word.length > 0
            ? this.lex.search(this.upperCaseWord, {
                prefix: true,
                wildcard: ".",
              })
            : [];
      } else {
        this.completions = [];
        let queryRegexp = new RegExp("^" + this.word + "$");
        for (const key in this.dictionary) {
          if (queryRegexp.test(key) || queryRegexp.test(key.toLowerCase())) {
            this.completions.push(key);
          }
        }
      }

      if (this.completions.length > 0) {
        if (this.completions[0] === this.upperCaseWord) {
          this.isWord = true;
          this.completions.shift(); // drop word from completions list
        } else {
          this.isWord = false;
        }
      } else {
        this.isWord = false;
      }

      if (this.isWord) {
        if (this.dictionary && this.dictionary[this.upperCaseWord]) {
          this.definition = this.dictionary[this.upperCaseWord];
        } else {
          this.definition = "unknown definition";
          for (let iB = 1; iB < window.definition_buckets.length; iB++) {
            const bucket = window.definition_buckets[iB];
            const l = this.word.length;
            if (bucket.start <= l && l <= bucket.end) {
              if (bucket.loaded) {
                console.log("Oops, bucket is supposed to have loaded");
              } else {
                this.loadDefinitions(iB);
              }
              break;
            }
          }
        }
      }
    },
    loadDefinitions(iB) {
      const bucket = window.definition_buckets[iB];
      var s = document.createElement("script");
      s.type = "text/javascript";
      s.src =
        process.env.BASE_URL +
        "resources/definitions_" +
        bucket.start +
        "-" +
        bucket.end +
        ".js";
      const validator = this;
      s.onload = function () {
        // add new definitions into list
        validator.dictionary = {
          ...validator.dictionary,
          ...window["definitions_" + bucket.start + "_" + bucket.end],
        };
        if (validator.dictionary[validator.upperCaseWord]) {
          validator.definition = validator.dictionary[validator.upperCaseWord];
        }
        window.definition_buckets[iB].loaded = true;
      };
      document.getElementsByTagName("head")[0].appendChild(s);
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
