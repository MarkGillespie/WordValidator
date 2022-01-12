<template>
  <div id="lexicon-input">
    <textarea
      class="lexicon-input"
      :value="customLexicon"
      type="text"
      @input="handleInput"
      placeholder="Enter additional words to consider"
    />
  </div>
</template>

<script>
export default {
  name: "LexiconInput",
  components: {},
  props: [],
  data() {
    return { customLexicon: "" };
  },
  methods: {
    handleInput(evt) {
      this.customLexicon = evt.target.value;
      if (this.customLexicon.length === 0) {
        this.$emit("customLexiconInput", []);
      } else {
        this.$emit(
          "customLexiconInput",
          this.customLexicon.split(/\s+/).map((w) => w.toUpperCase())
        );
      }
    },
  },
};
</script>

<style>
.lexicon-input {
  margin: 1em 0em;
  padding: 0.3em;
  font-size: large;
  width: 100%;
  resize: vertical;
  border-radius: 0.5em;
  border: 0px;
  box-shadow: 0 0.05em 0.25em rgba(0, 0, 0, 0.432);
}
</style>
