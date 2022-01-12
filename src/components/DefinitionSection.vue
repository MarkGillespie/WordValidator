<template>
  <div class="definition-section">
    <div class="word">
      {{ word }}
    </div>
    <div class="def" v-if="isWord && hasDefinition">
      {{ definition }}
    </div>
    <div class="def" v-else-if="isWord">
      <span>loading definition</span>
      <div class="lds-ripple">
        <div></div>
        <div></div>
      </div>
    </div>
    <div class="def" id="notword" v-else-if="word.length > 0">
      not a word :(
    </div>
  </div>
</template>

<script>
export default {
  name: "DefinitionSection",
  props: ["word", "isWord", "definition"],
  data() {
    return {};
  },
  computed: {
    hasDefinition: function () {
      return this.definition.length > 0;
    },
  },
};
// display: inline-block;
</script>

<style>
.definition-section {
  padding: 1em;
  font-size: large;
  background-color: var(--box-background-color);
  border-radius: 0.5em;
  box-shadow: 0 0.05em 0.25em rgba(0, 0, 0, 0.432);
  min-height: 10em;
}

.word {
  font-size: x-large;
  font-weight: bold;
  color: rgb(146, 32, 32);
}

.def {
  color: black;
}

.lds-ripple {
  position: relative;
  width: 80px;
  height: 80px;
}

.lds-ripple div {
  position: absolute;
  border: 4px solid rgba(175, 144, 130);
  opacity: 1;
  border-radius: 50%;
  animation: lds-ripple 1s cubic-bezier(0, 0.2, 0.8, 1) infinite;
}

.lds-ripple div:nth-child(2) {
  animation-delay: -0.5s;
}

@keyframes lds-ripple {
  0% {
    top: 36px;
    left: 36px;
    width: 0;
    height: 0;
    opacity: 1;
  }
  100% {
    top: 0px;
    left: 0px;
    width: 72px;
    height: 72px;
    opacity: 0;
  }
}
</style>
