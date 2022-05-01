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
    <div>
    <label>
    min length:
    <input
      v-model="minLength"
      type="number"
      value="minLength"
      @input="checkWord"
    />
    </label>
    &nbsp;
    &nbsp;
    &nbsp;
    &nbsp;
    <label>
    Use simple words:
    <input
      v-model="useSimpleWords"
      type="checkbox"
      value="useSimpleWords"
      @change="checkWord"
    />
    </label>
    </div>
    <Navigation />
  </div>
</template>

<script>
import DefinitionSection from "../components/DefinitionSection.vue";
import InputSection from "../components/InputSection.vue";
import CompletionSection from "../components/CompletionSection.vue";
import LexiconInput from "../components/LexiconInput.vue";
import Navigation from "../components/Navigation.vue";
import { simple_lexicon } from "../../public/resources/simple_lexicon.js";

export default {
  name: "WordValidator",
  props: [],
  components: {
    DefinitionSection,
    InputSection,
    CompletionSection,
    Navigation,
    LexiconInput,
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
      trie: window.trie,
      full_lex: window.lexicon,
      customLexicon: null,
      customLexiconCompletions: [],
      useSimpleWords: false,
      minLength: 4,
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
      lex: function () {
          return this.useSimpleWords ? simple_lexicon : this.full_lex;
      },
  },
  methods: {
    useCustomLexicon(customLexicon) {
      this.customLexicon = customLexicon;
      this.checkWord();
    },
    checkInputWord(word) {
      this.word = word;
      this.checkWord();
    },
    checkWord() {
      if (!this.word) this.word = "";
      this.upperCaseWord = this.word.toUpperCase();

      this.completions = [];
      this.customLexiconCompletions = [];

      let checkPlainText = /^([A-Z]|\.)*$/;
      if (checkPlainText.test(this.upperCaseWord)) {
        if (this.word.length >= 1) {
          this.completions = this.trie.search(this.upperCaseWord, {
            prefix: true,
            wildcard: ".",
          });
          if (this.usingCustomLexicon) {
            const queryRegexp = new RegExp("^" + this.upperCaseWord);
            this.customLexicon.forEach((word) => {
              if (
                queryRegexp.test(word) ||
                queryRegexp.test(word.toLowerCase())
              ) {
                this.customLexiconCompletions.push(word);
              }
            });
          }
        }
      } else {
        const queryRegexp = new RegExp("^" + this.word + "$");
        if (this.word.length >= 1) {
          this.lex.forEach((word) => {
            if (
              queryRegexp.test(word) ||
              queryRegexp.test(word.toLowerCase())
            ) {
              this.completions.push(word);
            }
          });

          if (this.usingCustomLexicon) {
            this.customLexicon.forEach((word) => {
              if (
                queryRegexp.test(word) ||
                queryRegexp.test(word.toLowerCase())
              ) {
                this.customLexiconCompletions.push(word);
              }
            });
          }
        }
      }
      this.completions = this.completions.filter(s => {return s.length >= this.minLength;});
      this.completions.sort((s,t) => {
          if (s.length < t.length) {return false;} else if (s.length > t.length) {return true} else {return s > t;}
      });
      if (this.usingCustomLexicon) {
        this.customLexiconCompletions.sort((s,t) => {
            if (s.length < t.length) {return false;} else if (s.length > t.length) {return true} else {return s > t;}
        });
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
          this.definition = "";
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

.horizontal-layout {
  display: flex;
  flex-direction: horizontal;
  gap: 1em;
}
</style>
