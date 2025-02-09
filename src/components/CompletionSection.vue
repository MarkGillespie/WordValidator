<template>
  <div v-bind:class="'completions-contain ' + width">
    <span v-if="title.length > 0">{{ title }}</span>
    <ul class="completions" v-bind:id="id">
      <li
        class="completion"
        v-for="completion in shownCompletions"
        :key="completion"
      >
        <router-link :to="completion">{{ completion }}</router-link>
      </li>

      <li
        class="completion"
        v-if="completions.length > shownCompletions.length"
      >
        <a
          @click.prevent="
            showAll = true;
            return false;
          "
        >
          +{{ completions.length - shownCompletions.length }} more
        </a>
      </li>
      <li class="completion" v-else-if="completions.length > defaultLength">
        <a
          @click.prevent="
            showAll = false;
            return false;
          "
          >see fewer
        </a>
      </li>
    </ul>
  </div>
</template>

<script>
// Compute width of a string (calibrated to Helvetica)
// https://stackoverflow.com/questions/118241/calculate-text-width-with-javascript
function measureTextWidth(str) {
  const widths = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0.2796875, 0.2765625, 0.3546875, 0.5546875, 0.5546875,
    0.8890625, 0.665625, 0.190625, 0.3328125, 0.3328125, 0.3890625, 0.5828125,
    0.2765625, 0.3328125, 0.2765625, 0.3015625, 0.5546875, 0.5546875, 0.5546875,
    0.5546875, 0.5546875, 0.5546875, 0.5546875, 0.5546875, 0.5546875, 0.5546875,
    0.2765625, 0.2765625, 0.584375, 0.5828125, 0.584375, 0.5546875, 1.0140625,
    0.665625, 0.665625, 0.721875, 0.721875, 0.665625, 0.609375, 0.7765625,
    0.721875, 0.2765625, 0.5, 0.665625, 0.5546875, 0.8328125, 0.721875,
    0.7765625, 0.665625, 0.7765625, 0.721875, 0.665625, 0.609375, 0.721875,
    0.665625, 0.94375, 0.665625, 0.665625, 0.609375, 0.2765625, 0.3546875,
    0.2765625, 0.4765625, 0.5546875, 0.3328125, 0.5546875, 0.5546875, 0.5,
    0.5546875, 0.5546875, 0.2765625, 0.5546875, 0.5546875, 0.221875, 0.240625,
    0.5, 0.221875, 0.8328125, 0.5546875, 0.5546875, 0.5546875, 0.5546875,
    0.3328125, 0.5, 0.2765625, 0.5546875, 0.5, 0.721875, 0.5, 0.5, 0.5,
    0.3546875, 0.259375, 0.353125, 0.5890625,
  ];
  const avg = 0.5279276315789471;
  return str
    .split("")
    .map((c) =>
      c.charCodeAt(0) < widths.length ? widths[c.charCodeAt(0)] : avg
    )
    .reduce((cur, acc) => acc + cur);
}

export default {
  name: "CompletionSection",
  components: {},
  props: ["completions", "id", "width", "title"],
  data() {
    return {
      showAll: false,
      defaultLength: 15,
    };
  },
  computed: {
    shownCompletions: function () {
      return this.showAll
        ? this.completions
        : this.completions.slice(0, this.defaultLength);
    },
  },
  watch: {
    completions: function () {
      this.showAll = false;
      let completionsWidth = measureTextWidth(
        "+" + (this.completions.length - this.shownCompletions.length) + " more"
      );
      this.completions.forEach(
        (completion) =>
          (completionsWidth = Math.max(
            completionsWidth,
            measureTextWidth(completion)
          ))
      );
      document.getElementById(this.id).style["column-width"] =
        completionsWidth + 1 + "em";
    },
  },
};
</script>

<style>
/* Hack to allow vertical scrolling in columnar layout */
/* https://stackoverflow.com/questions/36503329/css-columns-overflow-y-scroll-issue/36503666 */
.completions-contain {
  overflow-y: auto;
  min-height: 10em;
  max-height: 80vh;
  padding: 1em;
  margin: 0em;
  font-size: large;
  background-color: var(--page-background-color-darker);
  border-radius: 0.5em;
  box-shadow: 0 0.05em 0.25em rgba(0, 0, 0, 0.432);
}
.completions-contain.full {
  display: inline-block;
  width: 100%;
}

.completions-contain.half {
  display: inline-block;
  width: 50%;
}

.completions {
  padding: 0;
  margin: 0;
  min-height: 5em;
  list-style-type: none; /* Remove bullets */
}

.completion {
}

.completion > a {
  padding: 0.25em;
  text-decoration: none;
  color: var(--theme-color);
  border-radius: 0.5em;
}

.completion > a:hover {
  background-color: var(--page-background-color);
  /* color: white; */
}
</style>
