<template>
  <div id="input-section">
    <input
      class="input"
      :value="word"
      type="text"
      @input="handleInput"
      v-on:keyup.enter="handleEnter"
      placeholder="Please enter your word..."
    />
  </div>
</template>

<script>
export default {
  name: "InputSection",
  components: {},
  props: { clearOnEnter: { default: false } },
  data() {
    return { word: "" };
  },
  mounted: function () {
    if (this.$route.params.queryWord) {
      this.word = this.$route.params.queryWord;
      this.$emit("textInput", this.word);
    }
  },
  methods: {
    handleInput(evt) {
      this.word = evt.target.value;
      this.$emit("textInput", this.word);
    },
    handleEnter(evt) {
      this.word = evt.target.value;
      this.$emit("textEntered", this.word);
      if (this.clearOnEnter) {
        this.word = "";
      }
    },
  },
  watch: {
    "$route.params.queryWord": function (queryWord) {
      this.word = queryWord;
      this.$emit("textInput", this.word);
    },
  },
};
</script>

<style>
.input {
  margin: 1em 0em;
  padding: 0.3em;
  font-size: large;
  width: 100%;
  border-radius: 0.5em;
  border: 0px;
  box-shadow: 0 0.05em 0.25em rgba(0, 0, 0, 0.432);
}
</style>
